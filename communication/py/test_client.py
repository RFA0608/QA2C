import tcp_protocol_client as tcc

HOST = 'localhost'
PORT = 9999

with tcc.tcp_client(HOST, PORT) as tccp:
    typ, dat = tccp.recv()
    print(f"recv : {typ}, {dat}")
    tccp.send(dat)

    typ, dat = tccp.recv()
    print(f"recv : {typ}, {dat}")
    tccp.send(dat)

    typ, dat = tccp.recv()
    print(f"recv : {typ}, {dat}")
    tccp.send(dat)
    