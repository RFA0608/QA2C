package tpc

import (
	"bytes"
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
)

const byte_size = 1024
const print_flag = false

func InitTCP(HOST string, PORT string) net.Conn {
	conn, err := net.Dial("tcp", HOST+":"+PORT)
	if err != nil {
		if print_flag {
			fmt.Println("def: InitTCP | error | connection false")
		}
		os.Exit(-1)
	}

	tcp, ack := conn.(*net.TCPConn)
	if !ack {
		if print_flag {
			fmt.Println("def: InitTCP | error | tcp connect false")
		}
		os.Exit(-1)
	}

	if err := tcp.SetNoDelay(true); err != nil {
		if print_flag {
			fmt.Println("def: InitTCP | error | no delay set false")
		}
		os.Exit(-1)
	}

	if print_flag {
		fmt.Println("def: InitTCP | alert | connect")
	}

	return conn
}

func ExitTCP(conn net.Conn) {
	conn.Close()
}

func Send[T any](conn net.Conn, data T) {
	val := any(data)

	switch val.(type) {
	case int64:
		send_data := "<INT>" + fmt.Sprintf("%d", val) + "<END>"
		send_data_byte := []byte(send_data)
		_, err := conn.Write(send_data_byte)
		if err != nil {
			if print_flag {
				fmt.Println("def: Send | error | communication false")
			}
			os.Exit(-1)
		}

		buffer := make([]byte, byte_size)
		var read_data_byte []byte

		for {
			n, err := conn.Read(buffer)

			if err != nil {
				if n != 0 {
					if print_flag {
						fmt.Println("def: Send | error | communication false")
					}
					os.Exit(-1)
				}
			}

			for i := 0; i < n; i++ {
				read_data_byte = append(read_data_byte, buffer[i])
			}

			if bytes.Contains(read_data_byte, []byte("<END>")) {
				break
			}
		}

		if bytes.Contains(read_data_byte, []byte("<CHK>")) {
			if print_flag {
				fmt.Println("def: Send | alert | communication complete")
			}
		} else {
			if print_flag {
				fmt.Println("def: send | error | communication false")
			}
			os.Exit(-1)
		}
	case float64:
		send_data := "<FLOAT>" + fmt.Sprintf("%f", val) + "<END>"
		send_data_byte := []byte(send_data)
		_, err := conn.Write(send_data_byte)
		if err != nil {
			if print_flag {
				fmt.Println("def: Send | error | communication false")
			}
			os.Exit(-1)
		}

		buffer := make([]byte, byte_size)
		var read_data_byte []byte

		for {
			n, err := conn.Read(buffer)

			if err != nil {
				if n != 0 {
					if print_flag {
						fmt.Println("def: Send | error | communication false")
					}
					os.Exit(-1)
				}
			}

			for i := 0; i < n; i++ {
				read_data_byte = append(read_data_byte, buffer[i])
			}

			if bytes.Contains(read_data_byte, []byte("<END>")) {
				break
			}
		}

		if bytes.Contains(read_data_byte, []byte("<CHK>")) {
			if print_flag {
				fmt.Println("def: Send | alert | communication complete")
			}
		} else {
			if print_flag {
				fmt.Println("def: send | error | communication false")
			}
			os.Exit(-1)
		}
	case string:
		send_data := "<STR>" + fmt.Sprintf("%s", val) + "<END>"
		send_data_byte := []byte(send_data)
		_, err := conn.Write(send_data_byte)
		if err != nil {
			if print_flag {
				fmt.Println("def: Send | error | communication false")
			}
			os.Exit(-1)
		}

		buffer := make([]byte, byte_size)
		var read_data_byte []byte

		for {
			n, err := conn.Read(buffer)

			if err != nil {
				if n != 0 {
					if print_flag {
						fmt.Println("def: Send | error | communication false")
					}
					os.Exit(-1)
				}
			}

			for i := 0; i < n; i++ {
				read_data_byte = append(read_data_byte, buffer[i])
			}

			if bytes.Contains(read_data_byte, []byte("<END>")) {
				break
			}
		}

		if bytes.Contains(read_data_byte, []byte("<CHK>")) {
			if print_flag {
				fmt.Println("def: Send | alert | communication complete")
			}
		} else {
			if print_flag {
				fmt.Println("def: send | error | communication false")
			}
			os.Exit(-1)
		}
	default:
		if print_flag {
			fmt.Println("def: send | error | type false")
		}
		os.Exit(-1)
	}
}

func Recv(conn net.Conn) (string, any) {
	send_data := "<RED><END>"
	send_data_byte := []byte(send_data)
	_, err := conn.Write(send_data_byte)
	if err != nil {
		if print_flag {
			fmt.Println("def: Send | error | communication false")
		}
		os.Exit(-1)
	}

	buffer := make([]byte, byte_size)
	var read_data_byte []byte

	for {
		n, err := conn.Read(buffer)

		if err != nil {
			if n != 0 {
				if print_flag {
					fmt.Println("def: Send | error | communication false")
				}
				os.Exit(-1)
			}
		}

		for i := 0; i < n; i++ {
			read_data_byte = append(read_data_byte, buffer[i])
		}

		if bytes.Contains(read_data_byte, []byte("<END>")) {
			break
		}
	}

	data_type := ""
	var data any

	if bytes.Contains(read_data_byte, []byte("<INT>")) {
		data_type = "INT"
		read_data := strings.ReplaceAll(string(read_data_byte), "<END>", "")
		read_data = strings.ReplaceAll(read_data, "<INT>", "")
		data, _ = strconv.ParseInt(read_data, 10, 64)

	} else if bytes.Contains(read_data_byte, []byte("<FLOAT>")) {
		data_type = "FLOAT"
		read_data := strings.ReplaceAll(string(read_data_byte), "<END>", "")
		read_data = strings.ReplaceAll(read_data, "<FLOAT>", "")
		data, _ = strconv.ParseFloat(read_data, 64)

	} else if bytes.Contains(read_data_byte, []byte("<STR>")) {
		data_type = "STR"
		read_data := strings.ReplaceAll(string(read_data_byte), "<END>", "")
		read_data = strings.ReplaceAll(read_data, "<STR>", "")
		data = read_data

	} else {
		if print_flag {
			fmt.Println("def: send | error | communication false")
		}
		os.Exit(-1)
	}

	return data_type, data
}
