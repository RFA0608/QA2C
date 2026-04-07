// The folder with go.mod must have the file "tcp_protocol_client.go" with the same package name
package main

import (
	"fmt"
	"tcp/tps"
)

const host = "localhost"
const port = "9999"

func main() {
	conn := tps.InitTCP(host, port)

	var i int64 = 60207
	tps.Send(conn, i)
	_, data := tps.Recv(conn)
	fmt.Print("recv : ")
	fmt.Println(data)

	var f float64 = 60.207
	tps.Send(conn, f)
	_, data = tps.Recv(conn)
	fmt.Print("recv : ")
	fmt.Println(data)

	var l string = "60-207"
	tps.Send(conn, l)
	_, data = tps.Recv(conn)
	fmt.Print("recv : ")
	fmt.Println(data)

	tps.ExitTCP(conn)
}
