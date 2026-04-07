#include "tcp_protocol_client.h"
#include <string>
#include <iostream>
using namespace std;

const string host = "127.0.0.1";
const int port = 9999;

int main()
{
    tcp_client tccp = tcp_client(host, port);

    int i = tccp.Recv<int>();
    cout << "recv : " << i << endl;

    tccp.Send<int>(i);

    double f = tccp.Recv<double>();
    cout << "recv : " << f << endl;

    tccp.Send<double>(f);

    string s = tccp.Recv<string>();
    cout << "recv : " << s << endl;

    tccp.Send<string>(s);
}