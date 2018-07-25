#!/usr/bin/env python
#
# Sign a multisig transaction proposed by a Coinkite user. Require plaintext extended private
# key that was used when creating the account (ie. the co-signer's key).
#
import click, simplejson, requests, tempfile, time
from simplejson import JSONDecodeError
from pycoin import ecdsa
from pycoin.key.msg_signing import verify_message
from pycoin.key.BIP32Node import BIP32Node
from pycoin.tx.script import der

from pprint import pprint


def check_sig_and_unwrap(ext_json):
    # unwrap
    try:
        content = str(ext_json['contents'])
        signed_by = str(ext_json['signed_by'])
        msg_signature = str(ext_json['signature'])
    except KeyError, e:
        raise click.BadParameter("Proposal should contain certain JSON key values: %s" % e)

    ok = verify_message(content, signed_by, msg_signature, netcode='BTC')
    if not ok:
        raise ValueError("Wrapper signature check failed; suspect tampering.")

    return simplejson.loads(content)

def show_page(proposal):
    # Present the details. In the real deal, this is presented even nicely, but trying
    # to keep this simple... and yet I cannot resist bootstrap for styling.
    template = u'''<html><head>
        <meta charset="utf-8">
        <link rel="stylesheet" 
            href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        </head><body>
        <div class="container">
          <h1>{proposal_title}</h1>
          {proposal_html}
          <hr>
          {super_tech_html}
        </div>'''

    rendered = template.format(**proposal)

    with tempfile.NamedTemporaryFile(suffix='.html', prefix='proposed-transaction') as tmp:
        tmp.write(rendered.encode('utf8'))
        click.launch(tmp.name)
        click.echo("Proposed transaction details are in HTML file:\n\n  %s\n\n" % tmp.name)
        click.confirm("Ready to approve?")

def do_signing(wallet, req_keys, inputs):
    # Do the actual signing. We are trusting the sighash values.

    # Make the right subkey for each inputs
    wallets = {}
    for sp, (addr_check, ppair) in req_keys.items():
        w = wallet.subkey_for_path(sp)
        assert w.bitcoin_address() == addr_check
        assert w.public_pair() == tuple(ppair)
        wallets[sp] = w

    # Generate a signature for each input required
    sigs = []
    SIGHASH_ALL = 1
    order = ecdsa.generator_secp256k1.order()
    for sp, sighash in inputs:
        sighash_int = int(sighash, 16)
        r,s = ecdsa.sign(ecdsa.generator_secp256k1, wallets[sp].secret_exponent(), sighash_int)
        if s + s > order:
            s = order - s
        sig = der.sigencode_der(r, s) + chr(SIGHASH_ALL)
        sigs.append((sig.encode('hex'), sighash, sp))

    return sigs

def package_for_ck(wallet, proposal, sigs):
    # build JSON package expected back at Coinkite.
    content = dict(
            cosigner = proposal['cosigner'],
            request = proposal['request'],
            signatures = sigs)

    # Hack: server expects signature to alwasy be using BTC network, but when
    # experimenting on testnet, the wallet will be XTN.
    if wallet._netcode != 'BTC':
        wallet._netcode = 'BTC'

    # serialize that and wrap in more JSON, with a signature.
    resp = dict(content = simplejson.dumps(content),
                    _humans = 'I used python',
                    signed_by = wallet.bitcoin_address())

    resp['signature'] = wallet.sign_message(resp['content'])

    return simplejson.dumps(resp, indent=2)

def upload_to_ck(package):
    # Send the signed data back to Coinkite. If it's the last required signature,
    # the transaction will be sent at this point. User could also upload via form
    # on site.
    #
    UPLOAD_URL = 'https://coinkite.com/co-sign/done-signature'
    r = requests.put(UPLOAD_URL, data=package)

    click.echo("Coinkite server says:\n\t%s" % r.content)


@click.command()
@click.option('--proposal', '-i', type=click.File('rb'),
                    help="JSON file downloaded from CK already")
@click.option('--url', '-u', metavar='URL',
                    help="https://coinkite.com/co-sign/json/<req>:<cos>:<pin_check>")
@click.option('--html/--no-html', default=True,
                    help="Show details of proposed transaction?")
@click.option('--key', '-k', type=click.File('r'), required=True,
                    help="Extended private key (base58)")
@click.option('--upload/--no-upload', default=True,
                    help="Auto upload signed results file to CK?")
@click.option('--output', '-o', type=click.File('w'),
                    help="Write signed response to this file")
def olsign(key, proposal, url, upload, html, output):

    if not url and not proposal:
        raise click.BadParameter(
            "Need a URL to fetch proposal from (--url), or the file itself (-i file.json)")


    # get the proposal JSON
    try:
        if url:
            proposal = requests.get(url).json()
        else:
            proposal = simplejson.load(proposal)
    except JSONDecodeError:
        raise click.UsageError("Does not contain valid JSON")

    # unwrap signature, checking it as we go
    proposal = check_sig_and_unwrap(proposal)

    click.echo('''
   Co-signing as: {cosigner}
Required xpubkey: ...{xpubkey_check}
'''.format(**proposal))

    # unpack their private key (to test if suitable)
    wallet = BIP32Node.from_wallet_key(key.read().strip())
    check = wallet.hwif(as_private = False)[-8:]
    if check != proposal['xpubkey_check']:
        raise click.UsageError('This private key is not the one we need as this co-signer.')
    
    #pprint(proposal.keys())

    # present a summary of what will happen
    if html: show_page(proposal)

    sigs = do_signing(wallet, proposal['req_keys'], proposal['inputs'])

    package = package_for_ck(wallet, proposal, sigs)

    if output:
        output.write(package)
        click.echo("Wrote result to: %s" % output.name)

    if upload:
        upload_to_ck(package)

    if not output and not upload:
        click.echo("JSON response:\n\n%s" % package)

if __name__ == '__main__':
    olsign()

# EOF
