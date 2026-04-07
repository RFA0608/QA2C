import numpy as np
import control as ct

class fs:
    # sampling period
    ts = 0.1

    # parameters
    Jp = 0.0211;  Jy = 0.0221
    Dp = 0.0053;  Dy = 0.0062
    Mg = 0.0153
    Kpp =  0.0011;  Kyy =  0.0047
    Kpy =  0.0021;  Kyp = -0.0027

    # system(state) matrix(discrete model)
    A = np.zeros((4,4), dtype=float)
    B = np.zeros((4,2), dtype=float)
    C = np.zeros((2,4), dtype=float)
    D = np.zeros((2,2), dtype=float)

    # output gain K
    K = np.zeros((2,4), dtype=float)

    # feedforward N_bar
    N_bar = np.zeros((2,2), dtype=float)

    # state and output
    x = np.zeros((4,1), dtype=float)
    u = np.zeros((2,1), dtype=float)

    def __init__(self, ts):
        # write your continous time linear model
        A = np.array([[0, 0, 1, 0],
                      [0, 0, 0, 1],
                      [-self.Mg/self.Jp, 0, -self.Dp/self.Jp, 0],
                      [0, 0, 0, -self.Dy/self.Jy]], dtype=float)
        B = np.array([[0, 0],
                      [0, 0],
                      [self.Kpp/self.Jp, self.Kpy/self.Jp],
                      [self.Kyp/self.Jy, self.Kyy/self.Jy]], dtype=float)
        C = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0]], dtype=float)
        D = np.array([[0, 0],
                      [0, 0]], dtype=float)
        sys_c = ct.ss(A, B, C, D)
        sys_d = sys_c.sample(ts, method='zoh')

        # save discretization value
        self.A = sys_d.A
        self.B = sys_d.B
        self.C = C
        self.D = D
        self.ts = ts

        # for gain K dlqr parameters setting
        Q_k = np.array([[1500, 0, 0, 0],
                        [0, 1500, 0, 0],
                        [0, 0, 10, 0],
                        [0, 0, 0, 10]], dtype=float)
        R_k = np.array([[0.1, 0],
                        [0, 0.1]], dtype=float)
        K, Sk, Ek = ct.dlqr(self.A, self.B, Q_k, R_k)

        N_bar = np.linalg.inv(self.C @ np.linalg.inv(np.eye(4) - (self.A - self.B @ K)) @ self.B);

        # save gain K and N_bar
        self.K = K
        self.N_bar = N_bar

    def state_update(self, x):
        self.x = x
    
    def get_output(self, ref):
        self.u = -self.K @ self.x + self.N_bar @ ref
        
        return self.u
    
class fs_q():
    # quantized level s for matrix and r for signal
    s = 1
    r = 1

    # gain of x
    H = np.zeros((2,4), dtype=float)
    H_q = np.zeros((2,4), dtype=int)

    # feedforward
    N_bar = np.zeros((2,2), dtype=float)
    N_bar_q = np.zeros((2,2), dtype=int)

    # input/output
    x_q = np.zeros((4,1), dtype=int)
    x = np.zeros((4,1), dtype=float)
    u_q = np.zeros((2,1), dtype=int)
    u = np.zeros((2,1), dtype=float)
    ref_q = np.zeros((2,1), dtype=int)
    ref = np.zeros((2,1), dtype=float)

    def __init__(self, H, N_bar):
        self.H = H
        self.N_bar = N_bar

    def set_level(self, r, s):
        self.r = r
        self.s = s

    def quantize(self):
        self.H_q = (self.s * self.H).astype(int)
        self.N_bar_q = (self.s * self.N_bar).astype(int)

    def get_output(self, x, ref):
        for i in range(4):
            self.x_q[i, 0] = int(self.r * x[i, 0])
        
        for i in range(2):
            self.ref_q[i, 0] = int(self.r * ref[i, 0]);

        self.u_q = -self.H_q @ self.x_q + self.N_bar_q @ self.ref_q
        
        self.u[0,0] = float(self.u_q[0, 0]) / self.r / self.s
        self.u[1,0] = float(self.u_q[1, 0]) / self.r / self.s

        return self.u
        
