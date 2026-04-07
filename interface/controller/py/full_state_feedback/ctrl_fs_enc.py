import tcp_protocol_client as tcc

# init tcp host and port
HOST = 'localhost'
PORT = 9999

# get model description
import model
import model_enc

# get other tools
import numpy as np
import time

def fs_encrypted():
    # set simulation(this section have to set same with plant)
    sampling_time = 0.02
    run_signal = True

    # get model from model description file
    fs = model.fs(sampling_time)
    fs_q = model.fs_q(fs.K, fs.N_bar)

    # set quantized level and quantize matrix
    fs_q.set_level(1000, 1000)
    fs_q.quantize()

    # get crypto model from model_enc
    crypto_cl = model_enc.crypto()
    enc_4_fs = model_enc.enc_for_fs(crypto_cl, fs_q.H_q, fs_q.N_bar_q)
    enc_4_fs.set_level(fs_q.r, fs_q.s)
    fs_enc = model_enc.fs_enc(crypto_cl.crypto_context, enc_4_fs.H_enc, enc_4_fs.N_bar_enc)

    # input/output initialization
    x = np.array([[0],
                  [0],
                  [0],
                  [0]], dtype=float)
    u = np.array([[0],
                  [0]], dtype=float)
    
    # reference
    # ref_list = np.array([[np.deg2rad(15), np.deg2rad(-15), 5000],
    #                     [np.deg2rad(40), np.deg2rad(20), 5000],
    #                     [np.deg2rad(-10), np.deg2rad(30), 5000],
    #                     [np.deg2rad(-20), np.deg2rad(-30), 5000],
    #                     [np.deg2rad(0), np.deg2rad(15), 5000]], dtype=float)
    # ref = np.array([[ref_list[0, 0]],
    #                 [ref_list[0, 1]]], dtype=float)

    ref = np.array([[np.deg2rad(15)],
                    [np.deg2rad(-15)]], dtype=float)
    
    # # step
    # step = 0
    # mode = 0

    with tcc.tcp_client(HOST, PORT) as tccp:
        while run_signal:
            # running signal send for controller
            _, signal = tccp.recv()

            if signal == "run":
                # start clock set
                stc = time.perf_counter_ns()

                # get plant output
                _, x0 = tccp.recv()
                _, x1 = tccp.recv()
                _, x2 = tccp.recv()
                _, x3 = tccp.recv()
                x[0, 0] = x0
                x[1, 0] = x1
                x[2, 0] = x2
                x[3, 0] = x3

                # send control input data
                tccp.send(u[0, 0]) 
                tccp.send(u[1, 0])

                # # ref_change
                # step = step + 1
                # if(step == ref_list[mode, 2]):
                #     step = 0
                #     if(mode < (ref_list.shape[0] - 1)):
                #         mode = mode + 1
                #     ref[0, 0] = ref_list[mode, 0]
                #     ref[1, 0] = ref_list[mode, 1]
                
                # send ref date
                tccp.send(ref[0, 0])
                tccp.send(ref[1, 0])

                # state estimation on plant and encryption
                # fs.state_update(x)
                x_enc, ref_enc = enc_4_fs.enc_signal(x, ref)

                ## controller description ##
                # ------------------------------------------------ #
                # get control input on ciphertext space
                enc_u0, enc_u1 = fs_enc.get_output(x_enc, ref_enc)
                # ------------------------------------------------ #

                int_u0 = enc_4_fs.dec_signal(enc_u0)
                int_u1 = enc_4_fs.dec_signal(enc_u1)

                u[0, 0] = float(int_u0) / enc_4_fs.r / enc_4_fs.s
                u[1, 0] = float(int_u1) / enc_4_fs.r / enc_4_fs.s

                # end clock set
                edc = time.perf_counter_ns()
                duration = (edc - stc) / 1000000
                print(f"loop time: {duration}ms")

            elif signal == "end":
                # end of loop signal get
                run_signal = False
                break

def main():
    fs_encrypted()

if __name__ == "__main__":
    main()
