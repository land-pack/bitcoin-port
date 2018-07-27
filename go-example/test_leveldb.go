package main

import (
	"fmt"
	"github.com/syndtr/goleveldb/leveldb"
)

func main() {

	db, err := leveldb.OpenFile("./godb", nil)
	if err != nil {
        fmt.Println("see me")
		panic(err)
	}
	data, err := db.Get([]byte("hello"), nil)
	if err != nil {
		panic(err)
	}
	fmt.Println(data)
	fmt.Println("Connection levelDB successful")
	defer db.Close()
}
