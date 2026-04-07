import tcp_protocol_server as tcs

HOST = 'localhost'
PORT = 9999

with tcs.tcp_server(HOST, PORT) as tcsp:
    tcsp.set_metric(True, 6)
    tcsp.set_sampleconst(False, 10)

    tcsp.send(60207)
    typ, dat = tcsp.recv()
    print(f"recv : {typ}, {dat}")

    tcsp.send(60.207)
    typ, dat = tcsp.recv()
    print(f"recv : {typ}, {dat}")

    tcsp.send("60-207")
    typ, dat = tcsp.recv()
    print(f"recv : {typ}, {dat}")

    tcsp.diagnostic_metric()