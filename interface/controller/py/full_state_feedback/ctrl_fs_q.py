import tcp_protocol_client as tcc

# init tcp host and port
HOST = 'localhost'
PORT = 9999

# get model description
import model

# get other tools
import numpy as np

def fs_quantized():
    # set simulation(this section have to set same with plant)
    sampling_time = 0.1
    run_signal = True

    # get model from model description file
    fs = model.fs(sampling_time)
    fs_q = model.fs_q(fs.K, fs.N_bar)

    # set quantized level and quantize matrix
    fs_q.set_level(1000, 1000)
    fs_q.quantize()

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

                # state update and generate output
                # fs.state_update(x)
                u = fs_q.get_output(x, ref)
            elif signal == "end":
                # end of loop signal get
                run_signal = False
                break

def main():
    fs_quantized()

if __name__ == "__main__":
    main()
