import numpy as np
from openfhe import *

class crypto():
    # cryptocontext for encryption
    paramters = any
    crypto_context = openfhe.CryptoContext

    # key_pair for encrption
    key_pair = openfhe.KeyPair

    def __init__(self):
        # parameter setting
        self.parameters = CCParamsBFVRNS()
        self.parameters.SetRingDim(1024)
        self.parameters.SetPlaintextModulus(4294008833)
        self.parameters.SetMultiplicativeDepth(2)
        self.parameters.SetSecurityLevel(SecurityLevel.HEStd_NotSet)
        
        # crypto context setting
        self.crypto_context = GenCryptoContext(self.parameters)
        self.crypto_context.Enable(PKESchemeFeature.PKE)
        self.crypto_context.Enable(PKESchemeFeature.KEYSWITCH)
        self.crypto_context.Enable(PKESchemeFeature.LEVELEDSHE)
        
        # key setting
        self.key_pair = self.crypto_context.KeyGen()
        self.crypto_context.EvalMultKeyGen(self.key_pair.secretKey)
        self.crypto_context.EvalRotateKeyGen(self.key_pair.secretKey, [1, 2, 3, 4])

    def get_crypto(self):
        return self.crypto_context

    def enc_vector(self, vec):
        # make plaintext with packing
        plaintext = self.crypto_context.MakePackedPlaintext(vec)
        
        # make ciphertext with encrypter
        ciphertext = self.crypto_context.Encrypt(self.key_pair.publicKey, plaintext)

        return ciphertext
    
    def dec_ciphertext(self, ciphertext):
        # make plaintext with decrypter
        plaintext = self.crypto_context.Decrypt(ciphertext, self.key_pair.secretKey)

        # make vecter(list) with unpacking
        vector = plaintext.GetPackedValue()

        return vector
    
class enc_for_fs():
    crypto_class = crypto

    # quantization level
    r = 1000
    s = 1000

    # gain of x
    H_q = np.zeros((2,4), dtype=int)
    N_bar_q = np.zeros((2,2), dtype=int)

    # encrypted gain
    H_enc_row1 = any
    H_enc_row2 = any
    N_bar_enc_row1 = any
    N_bar_enc_row2 = any

    # encrypted state
    x_enc = any
    ref_enc = any

    def __init__(self, crypto_class, H_q, N_bar_q):
        self.crypto_class = crypto_class
        self.H_q = H_q
        self.N_bar_q = N_bar_q
        
        vec_for_H = [-1, -1, -1, -1]
        vec_for_N_bar = [-1, -1]
        # encryption H_q value only one packing
        for j in range(4):
            vec_for_H[j] = H_q[0, j]
        self.H_enc_row1 = self.crypto_class.enc_vector(vec_for_H)
        for j in range(4):
            vec_for_H[j] = H_q[1, j]
        self.H_enc_row2 = self.crypto_class.enc_vector(vec_for_H)

        for j in range(2):
            vec_for_N_bar[j] = N_bar_q[0, j]
        self.N_bar_enc_row1 = self.crypto_class.enc_vector(vec_for_N_bar)
        for j in range(2):
            vec_for_N_bar[j] = N_bar_q[1, j]
        self.N_bar_enc_row2 = self.crypto_class.enc_vector(vec_for_N_bar)
        

    def set_level(self, r, s):
        self.r = r
        self.s = s
        
    def enc_signal(self, x, ref):
        vec_for_x = list()
        vec_for_ref = list()
        for i in range(4):
            vec_for_x.append(int(x[i, 0] * self.r))

        for i in range(2):
            vec_for_ref.append(int(ref[i, 0] * self.r))

        self.x_enc = self.crypto_class.enc_vector(vec_for_x)
        self.ref_enc = self.crypto_class.enc_vector(vec_for_ref)

        return self.x_enc, self.ref_enc
    
    def dec_signal(self, ciphertext):
        vec = self.crypto_class.dec_ciphertext(ciphertext)

        return vec[0]
    
class fs_enc():
    # for encrypted calculation (only crypto context do not save crypto class)
    crypto_context = openfhe.CryptoContext 
    
    # encrypted gain
    H_enc_row1 = any
    H_enc_row2 = any
    N_bar_enc_row1 = any
    N_bar_enc_row2 = any

    def __init__(self, crypto_context, H_enc_row1, H_enc_row2, N_bar_enc_row1, N_bar_enc_row2):
        self.crypto_context = crypto_context
        self.H_enc_row1 = H_enc_row1
        self.H_enc_row2 = H_enc_row2
        self.N_bar_enc_row1 = N_bar_enc_row1
        self.N_bar_enc_row2 = N_bar_enc_row2

    def get_output(self, x_enc, ref_enc):
        ciphertext_mul_00 = any
        ciphertext_mul_01 = any
        ciphertext_mul_10 = any
        ciphertext_mul_11 = any

        ciphertext_mul_00 = self.crypto_context.EvalMult(self.H_enc_row1, x_enc)
        ciphertext_mul_01 = self.crypto_context.EvalMult(self.H_enc_row2, x_enc)
        ciphertext_mul_10 = self.crypto_context.EvalMult(self.N_bar_enc_row1, ref_enc)
        ciphertext_mul_11 = self.crypto_context.EvalMult(self.N_bar_enc_row2, ref_enc)

        ciphertext_rot_0 = any
        ciphertext_rot_1 = any
        ciphertext_result_0 = any
        ciphertext_result_1 = any
        ciphertext_rot_0 = self.crypto_context.EvalAdd(ciphertext_mul_00, ciphertext_mul_10)
        ciphertext_result_0 = self.crypto_context.EvalAdd(ciphertext_mul_00, ciphertext_mul_10)
        ciphertext_rot_1 = self.crypto_context.EvalAdd(ciphertext_mul_01, ciphertext_mul_11)
        ciphertext_result_1 = self.crypto_context.EvalAdd(ciphertext_mul_01, ciphertext_mul_11)


        for j in range(3):
            ciphertext_rot_0 = self.crypto_context.EvalRotate(ciphertext_rot_0, 1)
            ciphertext_result_0 = self.crypto_context.EvalAdd(ciphertext_result_0, ciphertext_rot_0)
            ciphertext_rot_1 = self.crypto_context.EvalRotate(ciphertext_rot_1, 1)
            ciphertext_result_1 = self.crypto_context.EvalAdd(ciphertext_result_1, ciphertext_rot_1)

        return ciphertext_result_0, ciphertext_result_1
    
