// The folder with go.mod must have the file "tcp_protocol_client.go" with the same package name
package main

import (
	"fmt"
	"tcp/tpc"
)

const host = "localhost"
const port = "9999"

func main() {
	conn := tpc.InitTCP(host, port)

	_, data := tpc.Recv(conn)
	fmt.Print("recv : ")
	fmt.Println(data)
	tpc.Send(conn, data.(int64))

	_, data = tpc.Recv(conn)
	fmt.Print("recv : ")
	fmt.Println(data)
	tpc.Send(conn, data.(float64))

	_, data = tpc.Recv(conn)
	fmt.Print("recv : ")
	fmt.Println(data)
	tpc.Send(conn, data.(string))

	tpc.ExitTCP(conn)
}
