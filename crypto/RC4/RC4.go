package main

import (
    "crypto/rc4"
    "encoding/base64"
    "fmt"
)


func main() {
    fmt.Println("base64+RC4 -> ", base64.StdEncoding.EncodeToString( RC4encode([]byte("key"), []byte("test")) ) )
    fmt.Println("RC4 encode -> ", RC4encode([]byte("key"), []byte("test")) )
    fmt.Println("RC4 decode -> ", RC4decode([]byte("key"), []byte("test")) )
}

func RC4(key []byte, src []byte) ([]byte) {
    c, err := rc4.NewCipher(key)
    if err != nil {
        return nil
    }
    c.XORKeyStream(src, src)
    return src
}

func RC4encode(key []byte, src []byte) ([]byte) {
    return RC4(key, src)
}

func RC4decode(key []byte, src []byte) ([]byte) {
    return RC4(key, src)
}




