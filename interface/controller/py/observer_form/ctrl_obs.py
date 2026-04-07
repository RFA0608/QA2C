import tcp_protocol_client as tcc

# init tcp host and port
HOST = 'localhost'
PORT = 9999

# get model description
import model

# get other tools
import numpy as np

def observer_based_controller():
    # set simulation(this section have to set same with plant)
    sampling_time = 0.02
    run_signal = True

    # get model from model description file
    obs = model.obs(sampling_time)

    # input/output initialization
    y = np.array([[0],
                  [0]], dtype=float)
    u = np.array([[0],
                  [0]], dtype=float)
    
    # reference
    ref_list = np.array([[np.deg2rad(15), np.deg2rad(-15), 5000],
                        [np.deg2rad(40), np.deg2rad(20), 5000],
                        [np.deg2rad(-10), np.deg2rad(30), 5000],
                        [np.deg2rad(-20), np.deg2rad(-30), 5000],
                        [np.deg2rad(0), np.deg2rad(15), 5000]], dtype=float)
    
    ref = np.array([[ref_list[0, 0]],
                    [ref_list[0, 1]]], dtype=float)
    
    # step
    step = 0
    mode = 0

    with tcc.tcp_client(HOST, PORT) as tccp:
        while run_signal:
            # running signal send for controller
            _, signal = tccp.recv()

            if signal == "run":
                # get plant output
                _, y0 = tccp.recv()
                _, y1 = tccp.recv()
                _, _ = tccp.recv()
                _, _ = tccp.recv()
                y[0, 0] = y0
                y[1, 0] = y1

                # send control input data
                tccp.send(u[0, 0]) 
                tccp.send(u[1, 0])

                # ref_change
                step = step + 1
                if(step == ref_list[mode, 2]):
                    step = 0
                    if(mode < (ref_list.shape[0] - 1)):
                        mode = mode + 1
                    ref[0, 0] = ref_list[mode, 0]
                    ref[1, 0] = ref_list[mode, 1]
                
                # send ref date
                tccp.send(ref[0, 0])
                tccp.send(ref[1, 0])

                # state update and generate output
                obs.state_update(y, u)
                u = obs.get_output(ref)
            elif signal == "end":
                # end of loop signal get
                run_signal = False
                break

def main():
    observer_based_controller()

if __name__ == "__main__":
    main()
