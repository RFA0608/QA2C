import sys
# sys.path.append(r"C:\Quanser\0_libraries\python")
from pal.products.aero2 import Aero2
from pal.utilities.scope import MultiScope

import tcp_protocol_server as tcs

# init tcp host and port
HOST = '0.0.0.0'
PORT = 9999

# get other tools
from threading import Thread
import signal
import time
import math
import numpy as np

# Thread hanlder initialization
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)

# simulation time and plotting set
simulationTime = 30 # will run for 30 seconds
color = np.array([0, 1, 0], dtype=np.float64)

Scope = MultiScope(rows=3, cols=2, title='Aero2', fps=30)

Scope.addAxis(row=0, col=0, timeWindow=12, yLabel='Pitch (deg)')
Scope.axes[0].attachSignal(name='theta_p')
Scope.axes[0].attachSignal(name='ref_p')

Scope.addAxis(row=0, col=1, timeWindow=12, yLabel='Yaw (deg)')
Scope.axes[1].attachSignal(name='theta_y')
Scope.axes[1].attachSignal(name='ref_y')

Scope.addAxis(row=1, col=0, timeWindow=12, yLabel='Pitch Rate (deg/s)')
Scope.axes[2].attachSignal(name='dp')

Scope.addAxis(row=1, col=1, timeWindow=12, yLabel='Yaw Rate (deg/s)')
Scope.axes[3].attachSignal(name='dy')

Scope.addAxis(row=2, col=0, timeWindow=12, xLabel='Time (s)', yLabel='V_main (V)')
Scope.axes[4].attachSignal(name='V_main')

Scope.addAxis(row=2, col=1, timeWindow=12, xLabel='Time (s)', yLabel='V_tail (V)')
Scope.axes[5].attachSignal(name='V_tail')

# control-system scenario
def control_loop():
    # interface setting #
    # ------------------------------------------------ #
    # using hardware
    id = 0
    
    # if you want to use Ouanser Interactive Labs, you will change to 0
    hardware = 0
    
    readMode = 0

    # frequency of system holder and sampler
    frequency = 50 # hz

    # for scope sampling rate
    countMax = frequency / 50
    count = 0

    # class initialization
    AeroClass = Aero2

    # describe #
    # ------------------------------------------------ #
    # instance of hardware model 
    with AeroClass(id, hardware=hardware, readMode=readMode, frequency=frequency) as myAero:
        # instance of tcp layer
        with tcs.tcp_server(HOST, PORT) as tcsp:
            startTime = 0
            timeStamp = 0
            def elapsed_time():
                return time.time() - startTime
            startTime = time.time()

            while timeStamp < simulationTime and not KILL_THREAD:
                # running signal send for controller
                tcsp.send("run")

                # read sensor information
                myAero.read_analog_encoder_other_channels()

                # calc output
                theta_pitch = myAero.pitchAngle
                theta_yaw = myAero.yawAngle
                rate_pitch = myAero.pitchRate
                rate_yaw = myAero.yawRate

                # send plant output
                tcsp.send(theta_pitch)
                tcsp.send(theta_yaw)
                tcsp.send(rate_pitch)
                tcsp.send(rate_yaw)

                # get control input
                _, u_motr_1 = tcsp.recv()
                _, u_motr_2 = tcsp.recv()

                # get ref value
                _, ref_pitch = tcsp.recv()
                _, ref_yaw = tcsp.recv()

                # running range set
                if abs(np.rad2deg(theta_pitch)) > 40:
                    voltage_motr_1, voltage_motr_2 = 0.0, 0.0
                else:
                    voltage_motr_1, voltage_motr_2 = u_motr_1, u_motr_2

                # write commands
                # voltage = np.clip(voltage, -15, 15)
                myAero.write_voltage(voltage_motr_1, voltage_motr_2)

                # plot to scopes
                count += 1
                if count >= countMax:
                    Scope.axes[0].sample(timeStamp, [np.rad2deg(theta_pitch), np.rad2deg(ref_pitch)])
                    Scope.axes[1].sample(timeStamp, [np.rad2deg(theta_yaw), np.rad2deg(ref_yaw)])
                    Scope.axes[2].sample(timeStamp, [np.rad2deg(rate_pitch)])
                    Scope.axes[3].sample(timeStamp, [np.rad2deg(rate_yaw)])
                    Scope.axes[4].sample(timeStamp, [u_motr_1])
                    Scope.axes[5].sample(timeStamp, [u_motr_2])
                    count = 0

                timeStamp = elapsed_time()

            tcsp.send("end")

def main():
    thread = Thread(target=control_loop)
    thread.start()

    while thread.is_alive() and (not KILL_THREAD):

        # This must be called regularly or the scope windows will freeze
        # Must be called in the main thread.
        MultiScope.refreshAll()
        time.sleep(0.01)

    input('Press the enter key to exit.')

if __name__ == "__main__":
    main()
