#ifndef TPS_H
#define TPS_H

#include <iostream>
#include <string>
#include <sstream>
#include <vector>

#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")
// !!! Above linker code only can be used in Windows Visual Studio C++17 (not VS code)
// If you want to use VS code environment, then you can use g++ and with option "-lws2_32" at compile time.

using namespace std;

class tcp_server
{
    private:
        WSADATA wsa_data;
        sockaddr_in server;
        sockaddr_in client;
        
        string addr = "localhost";
        int port = 9999;
        
        int byte_size = 1024;

        int time_out = 10;

        SOCKET socket_instance[2];
        
        bool print_flag = false;

    public:
        tcp_server(string host, int port)
        {
            DWORD timeout = this->time_out * 1000;
            
            this->addr = host;
            this->port = port;

            this->server.sin_family = AF_INET;
            inet_pton(AF_INET, host.c_str(), &this->server.sin_addr);
            // this->server.sin_addr.s_addr = inet_addr(host.c_str());
            this->server.sin_port = htons(port);

            if(WSAStartup(MAKEWORD(2, 2), &this->wsa_data) != 0)
            {
                if(this->print_flag)
                {   
                    cout << "def: _construct | error | WSA start up false" << endl;
                    exit(-1);
                }
            }

            SOCKET server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
            if(server_socket == -1)
            {
                if(this->print_flag)
                {
                    cout << "def: _construct | error | socket create false" << endl;
                }
                exit(-1);
            }
            else
            {
                this->socket_instance[0] = server_socket;
            }

            int opt = 1;
            setsockopt(this->socket_instance[0], SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));
            setsockopt(this->socket_instance[0], IPPROTO_TCP, TCP_NODELAY, (const char*)&opt, sizeof(opt));

            bind(this->socket_instance[0], (struct sockaddr*)&this->server, sizeof(this->server));
            listen(this->socket_instance[0], 1);

            setsockopt(this->socket_instance[0], SOL_SOCKET, SO_RCVTIMEO, (const char*)&timeout, sizeof(timeout));

            int client_len = sizeof(this->client);
            this->socket_instance[1] = accept(this->socket_instance[0], (struct sockaddr*)&this->client, &client_len);
            
            if(this->socket_instance[1] < 0)
            {
                int error_code = WSAGetLastError();
                if(error_code == WSAEWOULDBLOCK || error_code == WSAETIMEDOUT)
                {
                    if(this->print_flag)
                    {   
                        cout << "def: _construct | error | bind set false or timeout " << this->time_out << " second" << endl;
                    }
                    exit(-1);
                }
                else
                {
                    if(this->print_flag)
                    {   
                        cout << "def: _construct | error | accept error" << endl;
                    }
                    exit(-1);
                }
            }
            else
            {
                if(this->print_flag)
                {
                    cout << "def: _constuct | alert | connect" << endl;
                }
            }
        }

        ~tcp_server()
        {
            closesocket(this->socket_instance[0]);
            closesocket(this->socket_instance[1]);
            WSACleanup();
            if(this->print_flag)
            {
                cout << "def: _destruct | alert | close server" << endl;
            }
        }

        void set_byte(int byte)
        {
            this->byte_size = byte;
        };

        template <typename T>
        void Send(T data)
        {
            if constexpr (is_same_v<T, int>)
            {
                vector<char> buffer(this->byte_size);
                string read_data;
                int byte_read;
                while(true)
                {
                    byte_read = recv(this->socket_instance[1], buffer.data(), buffer.size(), 0);
                    if (byte_read <= 0)
                    {
                        if(this->print_flag)
                        {
                            cout <<"def: send | error | communication false" << endl;
                        }
                        exit(-1);
                    }

                    read_data.append(buffer.data(), byte_read);

                    if(read_data.find("<END>") != string::npos)
                    {
                        read_data.erase(read_data.find("<END>"), read_data.find("<END>") + 5);
                        break;
                    }
                }

                if (read_data.find("<RED>") != string::npos)
                {
                    stringstream data_stearm;
                    data_stearm << "<INT>" << data << "<END>";
                    string send_data = data_stearm.str();

                    int err = send(this->socket_instance[1], send_data.data(), send_data.length(), 0);
                    if(err == -1)
                    {
                        if(this->print_flag)
                        {
                            cout << "def: send | error | communication false" << endl;
                        }
                        exit(-1);
                    }
                    if(this->print_flag)
                    {
                        cout << "def: send | alert | communication complete" << endl;
                    }
                }
                else
                {
                    if(this->print_flag)
                    {
                        cout << "def: send | error | communication false" << endl;
                    }
                    exit(-1);
                }
            }
            else if constexpr (is_same_v<T, double>)
            {
                vector<char> buffer(this->byte_size);
                string read_data;
                int byte_read;
                while(true)
                {
                    byte_read = recv(this->socket_instance[1], buffer.data(), buffer.size(), 0);
                    if (byte_read <= 0)
                    {
                        if(this->print_flag)
                        {
                            cout <<"def: send | error | communication false" << endl;
                        }
                        exit(-1);
                    }

                    read_data.append(buffer.data(), byte_read);

                    if(read_data.find("<END>") != string::npos)
                    {
                        read_data.erase(read_data.find("<END>"), read_data.find("<END>") + 5);
                        break;
                    }
                }

                if (read_data.find("<RED>") != string::npos)
                {
                    stringstream data_stearm;
                    data_stearm << "<FLOAT>" << data << "<END>";
                    string send_data = data_stearm.str();

                    int err = send(this->socket_instance[1], send_data.data(), send_data.length(), 0);
                    if(err == -1)
                    {
                        if(this->print_flag)
                        {
                            cout << "def: send | error | communication false" << endl;
                        }
                        exit(-1);
                    }
                    if(this->print_flag)
                    {
                        cout << "def: send | alert | communication complete" << endl;
                    }
                }
                else
                {
                    if(this->print_flag)
                    {
                        cout << "def: send | error | communication false" << endl;
                    }
                    exit(-1);
                }
            }
            else if constexpr (is_same_v<T, string>)
            {
                vector<char> buffer(this->byte_size);
                string read_data;
                int byte_read;
                while(true)
                {
                    byte_read = recv(this->socket_instance[1], buffer.data(), buffer.size(), 0);
                    if (byte_read <= 0)
                    {
                        if(this->print_flag)
                        {
                            cout <<"def: send | error | communication false" << endl;
                        }
                        exit(-1);
                    }

                    read_data.append(buffer.data(), byte_read);

                    if(read_data.find("<END>") != string::npos)
                    {
                        read_data.erase(read_data.find("<END>"), read_data.find("<END>") + 5);
                        break;
                    }
                }

                if (read_data.find("<RED>") != string::npos)
                {
                    stringstream data_stearm;
                    data_stearm << "<STR>" << data << "<END>";
                    string send_data = data_stearm.str();

                    int err = send(this->socket_instance[1], send_data.data(), send_data.length(), 0);
                    if(err == -1)
                    {
                        if(this->print_flag)
                        {
                            cout << "def: send | error | communication false" << endl;
                        }
                        exit(-1);
                    }
                    if(this->print_flag)
                    {
                        cout << "def: send | alert | communication complete" << endl;
                    }
                }
                else
                {
                    if(this->print_flag)
                    {
                        cout << "def: send | error | communication false" << endl;
                    }
                    exit(-1);
                }
            }
            else 
            {
                if(this->print_flag)
                {
                    cout << "def: send | error | type false" << endl;
                }
                exit(-1);
            }
        }

        template <typename T>
        T Recv()
        {
            vector<char> buffer(this->byte_size);
            string read_data;
            int byte_read;
            while(true)
            {
                byte_read = recv(this->socket_instance[1], buffer.data(), buffer.size(), 0);
                if (byte_read <= 0)
                {
                    if(this->print_flag)
                    {
                        cout <<"def: send | error | communication false" << endl;
                    }
                }

                read_data.append(buffer.data(), byte_read);

                if(read_data.find("<END>") != string::npos)
                {
                    read_data.erase(read_data.find("<END>"), read_data.find("<END>") + 5);
                    break;
                }
            }

            T return_value;
            if constexpr (is_same_v<T, int>)
            {
                if(read_data.find("<INT>") != string::npos)
                {
                    read_data.erase(read_data.find("<INT>"), read_data.find("<INT>") + 5);
                    return_value = stoi(read_data);
                }
                else
                {
                    if(this->print_flag)
                    {
                        cout << "def: recv | error | type false" << endl;
                    }
                    exit(-1);
                }
            }
            else if constexpr (is_same_v<T, double>)
            {
                if(read_data.find("<FLOAT>") != string::npos)
                {
                    read_data.erase(read_data.find("<FLOAT>"), read_data.find("<FLOAT>") + 7);
                    return_value = stod(read_data);
                }
                else
                {
                    if(this->print_flag)
                    {
                        cout << "def: recv | error | type false" << endl;
                    }
                    exit(-1);
                }
            }
            else if constexpr (is_same_v<T, string>)
            {
                if(read_data.find("<STR>") != string::npos)
                {
                    read_data.erase(read_data.find("<STR>"), read_data.find("<STR>") + 5);
                    return_value = read_data;
                }
                else
                {
                    if(this->print_flag)
                    {
                        cout << "def: recv | error | type false" << endl;
                    }
                    exit(-1);
                }
            }
            else
            {
                if(this->print_flag)
                {
                    cout << "def: recv | error | type false" << endl;
                }
                exit(-1);
            }

            string send_data = "<CHK><END>";

            int err = send(this->socket_instance[1], send_data.data(), send_data.length(), 0);
            if(err == -1)
            {
                if(this->print_flag)
                {
                    cout << "def: send | error | communication false" << endl;
                }
                exit(-1);
            }

            return return_value;
        }
};

#endif
