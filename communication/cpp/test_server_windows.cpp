#include "tcp_protocol_server_windows.h"
#include <string>
#include <iostream>
using namespace std;

const string host = "0.0.0.0";
const int port = 9999;

int main()
{
    tcp_server tccp = tcp_server(host, port);

    tccp.Send<int>(60207);

    int i = tccp.Recv<int>();
    cout << "recv : " << i << endl;


    tccp.Send<double>(60.207);

    double f = tccp.Recv<double>();
    cout << "recv : " << f << endl;

    
    tccp.Send<string>("60-207");

    string s = tccp.Recv<string>();
    cout << "recv : " << s << endl;
}