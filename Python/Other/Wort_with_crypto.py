from curses.ascii import RS
import warnings


# --------------AES--------------
class Rijndael(object):
    NrArr = {
        128: {128: 10, 192: 12, 256: 14}, 192: {128: 12, 192: 12, 256: 14}, 256: {128: 14, 192: 14, 256: 14}
    }
    Sbox = (
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    )       # for encrypt
    InvSbox = (
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    )       # for decript

    def DropLid0(self, p):
        if len(p) > 1:
            while (len(p) > 1) and (p[0] == 0):
                p.pop(0)
        return p

    def __PolyMul(self, p1, p2, mod=2):
        res = [0]*(len(p1)+len(p2))
        p1.reverse()
        p2.reverse()
        for i in range(len(p1)):
            for j in range(len(p2)):
                res[i+j] = (res[i+j]+p1[i]*p2[j]) % mod
        res.reverse()
        return res

    def PolyMul(self, p1, p2, mod=2):
        p1 = self.DropLid0(Rijndael.inttobinlist(p1))
        p2 = self.DropLid0(Rijndael.inttobinlist(p2))
        return int(''.join(str(bit) for bit in self.__PolyMul(p1, p2, mod)), 2)

    def __XOR(self, p1, p2):
        l = len(p2)
        for i in range(len(p1)):
            p1[i] ^= p2[i % l]
        p1 = self.DropLid0(p1)
        return p1

    def XOR(self, p1, p2):
        p1 = self.DropLid0(Rijndael.inttobinlist(p1))
        p2 = self.DropLid0(Rijndael.inttobinlist(p2))
        return int(''.join(str(bit) for bit in self.__XOR(p1, p2)), 2)

    def __PolyDivMod2(self, p1, p2):
        p1 = self.DropLid0(p1)
        p2 = self.DropLid0(p2)
        while len(p1) >= len(p2):
            p1 = self.__XOR(p1[:len(p2)], p2)+p1[len(p2):]
        return p1

    def PolyDivMod2(self, p1, p2):
        p1 = self.DropLid0(Rijndael.inttobinlist(p1))
        p2 = self.DropLid0(Rijndael.inttobinlist(p2))
        return int(''.join(str(bit) for bit in self.__PolyDivMod2(p1, p2)), 2)

    def __init__(self, blocksize=128, keylen=128):
        if blocksize not in (128, 192, 256):
            warnings.warn("Unexpected block size value. Setting default (128)", UserWarning)
            blocksize = 128
        
        self.blocksize = blocksize
        self.data = ""
        
        self.__Nb = blocksize >> 5
        if keylen not in (128, 192, 256):
            warnings.warn("Unexpected key len value. Setting default (128)", UserWarning)
            keylen = 128
        self.__Nk = keylen >> 5
        self.__Nr = self.NrArr[keylen][blocksize]
        self.__State = [[b'\0']*self.__Nb]*4
        self.__Queue = []
        self.__order = 0
        self.__round = 1
        self.__key = []
        self.__Round_key = []
        self.__res = []
        self.__unused = b''

    @property
    def state(self):
        return self.__State

    @property
    def subkey(self):
        return self.__Round_key

    def state_tbl(self):
        return '\n'.join(' '.join('%02x' % M for M in Row) for Row in self.__State)

    def state_string(self):
        msg = ''.join(''.join('%02x' % M for M in Row) for Row in self.__State)
        correct_msg = ""
        for i in range (0,len(msg)//8):
            for k in range(4):
                correct_msg+=msg[i*2+k*8:i*2+2+k*8]
        return correct_msg

    def subkey_tbl(self):
        return '\n'.join(' '.join('%02x' % M for M in Row) for Row in self.__Round_key)

    @property
    def result(self):
        return '\n'.join(' '.join('%02x' % M for M in Row) for Row in self.__res)

    def set_key(self, key, raw=False):
        if not isinstance(key, bytearray):
            if not raw:
                key = Rijndael.hexstringtobytes(key)
            key = bytes(key)
        if len(key) < (4*self.__Nk):
            for i in range((4*self.__Nk)-len(key)):
                key+=b'\0'      
        # print(key)  
        key = [[key[i+(j*4)] for j in range(self.__Nk)] for i in range(4)]

        self.__key = key
        self.__Round_key = key

    def get_result(self, inhex=False):
        res = ""
        result = ""
        for i in range(self.__Nb):
            for j in range(4):
                # res.append(int(self.__State[j][i],16))
                res=str(self.__State[j][i])
                result += str(hex(int(res)))[2:]
        # res = ''.join(str(r) for r in res)
        return result
        # return res if not inhex else int(res, 16)

    def add(self, data, raw=False):
        if not isinstance(data, bytearray):
            if not raw:
                data = Rijndael.hexstringtobytes(data)
            data = bytes(data)
        if len(self.__unused) > 0:
            data = self.__unused + data
        if len(data) < (4*self.__Nb):
            data.ljust(4*self.__Nb, b'\0')
        for pos in range(0, len(data), 4*self.__Nb):
            self.__Queue.append(data[pos:pos+4*self.__Nb])
        pos = (len(data)//4*self.__Nb)*4*self.__Nb
        self.__unused = data[pos:]

    def set_state(self, data, raw=False):
        if not isinstance(data, bytearray):
            if not raw:
                data = Rijndael.hexstringtobytes(data)
            data = bytes(data)
        if len(data) < (4*self.__Nb):
            data.ljust(4*self.__Nb, b'\0')
        for pos in range(0, len(data), 4*self.__Nb):
            self.__State = [[data[pos+i+(4*j)] for j in range(self.__Nb)] for i in range(4)]

    def AddRoundKey(self, state, round_key):
        for i in range(4):
            for j in range(len(state[i])):
                state[i][j] = state[i][j] ^ round_key[i][j]

    def SubBytes(self, state, encript = True):
        if encript:
            for i in range(4):
                for j in range(len(state[i])):
                    state[i][j] = self.Sbox[state[i][j]]
        else:
            for i in range(4):
                for j in range(len(state[i])):
                    state[i][j] = self.InvSbox[state[i][j]]

    def ShiftRows(self, state, encript = True):
        rnj = (0, 1, 2, 3) if (len(state[0]) != 8) else (0, 1, 3, 4)
        if encript:
            for i in rnj:
                for shift in range(i):
                    state[i].append(state[i].pop(0))
        else:  
            for i in rnj:
                for shift in range(i):
                    state[i].insert(0, state[i].pop())

    def MixColumns(self, state, encript = True):
        if encript:
            C = ((2, 3, 1, 1), (1, 2, 3, 1), (1, 1, 2, 3), (3, 1, 1, 2))
            for j in range(len(state[0])):
                res = [0]*4
                for i in range(4):
                    for k in range(4):
                        mul = self.PolyMul(C[i][k], state[k][j])
                        mul = self.PolyDivMod2(mul, 0b100011011)
                        res[i] ^= mul
                for i in range(4):
                    state[i][j] = res[i]
        else:
            C = ((14, 11, 13, 9), (9, 14, 11, 13), (13, 9, 14, 11), (11, 13, 9, 14))
            for j in range(len(state[0])):
                res = [0]*4
                for i in range(4):
                    for k in range(4):
                        mul = self.PolyMul(C[i][k], state[k][j])
                        mul = self.PolyDivMod2(mul, 0b100011011)
                        res[i] ^= mul
                for i in range(4):
                    state[i][j] = res[i]
    
    def set_data_to_encrypt(self, data):
        if type(data) == str:
            data = data.encode("utf-8")
            data = data.hex()
        elif type(data) == int:
            pass
        
        self.blocks_of_data = self.divide_into_blocks_AES(data)
    
    def set_data_to_decrypt(self, data):
        
        self.blocks_of_data = self.divide_into_blocks_AES(data)

    def divide_into_blocks_AES(self, data):                             # data = "0x..0x.." divide on blocks = 128 bits (16 bytes)
        blocks = []
        size_of_block_bytes = self.blocksize // 8
        if len(data) % (size_of_block_bytes*2) == 0: blocks_count = len(data) // (size_of_block_bytes*2)
        else: blocks_count = len(data) // (size_of_block_bytes*2) + 1
        
        for i in range (blocks_count-1):
            blocks.append(data[i*size_of_block_bytes*2 : i * size_of_block_bytes*2 + size_of_block_bytes*2])

        blocks.append(data[(blocks_count-1) * size_of_block_bytes * 2 : len(data)])

        if len(blocks[-1]) != size_of_block_bytes*2:
            for i in range(size_of_block_bytes*2 - len(blocks[-1])):
                blocks[-1] += ('0')

        return blocks

    def EncryptBlock(self, block):
        self.set_state(block)    
        for i in range(10):             
            self.SubBytes(self.state)
            self.ShiftRows(self.state)
            self.MixColumns(self.state)
            self.AddRoundKey(self.state, self.subkey)
        self.data += str(self.state_string())
    
    def DecryptBlock(self, block):
        self.set_state(block)    
        for i in range(10):             
            self.AddRoundKey(self.state, self.subkey)
            self.MixColumns(self.state, False)
            self.ShiftRows(self.state, False)   
            self.SubBytes(self.state, False) 
        self.data += str(self.state_string())

    
    def Encrypt(self):
        print('\nStart AES encripting...')
        try:
            blocks = self.blocks_of_data
            for block in blocks:
                self.EncryptBlock(block)

            return self.data
        except:
            print("Error with encrypt AES")
    
    def Decript(self):                                                  # data (in hex) decrypt by AES
        print('\nStart AES decripting...')
        try:
            blocks = self.blocks_of_data
            for block in blocks:
                self.DecryptBlock(block)

            return self.data
        except:
            print("Error with decrypt AES")

    def inttobinlist(n):
        return [int(bit, 2) for bit in bin(n)[2:]]
    
    def chunkstring(string, length):
        return (string[0 + i:length + i] for i in range(0, len(string), length))
    
    def hexstringtobytes(string):
        if len(string) % 2:
            string = '0' + string
        string = Rijndael.chunkstring(string, 2)
        string = [int(d,16) for d in string]
        return string

# ------------Sha256-------------
class Sha256(object):        

    ks = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

    hs = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]

    M32 = 0xFFFFFFFF

    def __init__(self, m = None):
        self.mlen = 0
        self.buf = b''
        self.k = self.ks[:]
        self.h = self.hs[:]
        self.fin = False
        if m is not None:
            m = (m).encode('UTF-8')
            self.update(m)

    def print_mess_to_hash(self):
        print(self.buf)

    @staticmethod
    def pad(mlen):
        mdi = mlen & 0x3F
        length = (mlen << 3).to_bytes(8, 'big')
        padlen = 55 - mdi if mdi < 56 else 119 - mdi
        return b'\x80' + b'\x00' * padlen + length

    @staticmethod
    def ror(x, y):
        return ((x >> y) | (x << (32 - y))) & Sha256.M32

    @staticmethod
    def maj(x, y, z):
        return (x & y) ^ (x & z) ^ (y & z)

    @staticmethod
    def ch(x, y, z):
        return (x & y) ^ ((~x) & z)

    def compress(self, c):
        w = [0] * 64
        w[0 : 16] = [int.from_bytes(c[i : i + 4], 'big') for i in range(0, len(c), 4)]

        for i in range(16, 64):
            s0 = self.ror(w[i - 15],  7) ^ self.ror(w[i - 15], 18) ^ (w[i - 15] >>  3)
            s1 = self.ror(w[i -  2], 17) ^ self.ror(w[i -  2], 19) ^ (w[i -  2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & self.M32

        a, b, c, d, e, f, g, h = self.h

        for i in range(64):
            s0 = self.ror(a, 2) ^ self.ror(a, 13) ^ self.ror(a, 22)
            t2 = s0 + self.maj(a, b, c)
            s1 = self.ror(e, 6) ^ self.ror(e, 11) ^ self.ror(e, 25)
            t1 = h + s1 + self.ch(e, f, g) + self.k[i] + w[i]

            h = g
            g = f
            f = e
            e = (d + t1) & self.M32
            d = c
            c = b
            b = a
            a = (t1 + t2) & self.M32

        for i, (x, y) in enumerate(zip(self.h, [a, b, c, d, e, f, g, h])):
            self.h[i] = (x + y) & self.M32

    def update(self, m):
        if m is None or len(m) == 0:
            return

        assert not self.fin, 'Hash already finalized and can not be updated!'

        self.mlen += len(m)
        m = self.buf + m

        for i in range(0, len(m) // 64):
            self.compress(m[64 * i : 64 * (i + 1)])

        self.buf = m[len(m) - (len(m) % 64):]

    def digest(self):
        if not self.fin:
            self.update(self.pad(self.mlen))
            self.digest = b''.join(x.to_bytes(4, 'big') for x in self.h[:8])
            self.fin = True
        return self.digest

    def hexdigest(self):                                    # to hex
        tab = '0123456789abcdef'
        return ''.join(tab[b >> 4] + tab[b & 0xF] for b in self.digest())

# --------------RSA---------------
class RSA(object):
    def __init__(self, p = 11, q = 13, e = 17):
        n = q * p
        phi_n = (p-1)*(q-1)

        if (e>phi_n):
            print("e > phi_n - it is mistake!!!!!!!")
        
        d = self.find_d(e,phi_n)

        self.open_key = pair(e, n)
        self.secret_key = pair(d, n)
    
    def prepare_data(self, data):
        type_of_data = type(data)
        if type_of_data == int:
            pass
        elif type_of_data == str:
            data = data.encode("utf-8")
            data = data.hex()
            data = int(data, 16)

        return data   

    def encrypt(self, data):
        print("\nStart RSA encripting...")
        data = self.prepare_data(data)
        self.encrypt_data = self.pow_m(data, self.open_key.first_element, self.open_key.second_element)
        return self.encrypt_data                        # dec format (10 cc)

    def decrypt(self, data):
        print("\nStart RSA decripting...")
        self.encrypt_data = self.pow_m(data, self.secret_key.first_element, self.secret_key.second_element)
        return self.encrypt_data                        # dec format (10 cc)

    def find_d(self, e, phi_n):                         # e и phi_n = (p-1)*(q-1)
        a = e
        b = phi_n
        c = -1 
        k = []
        i = 0
        while (c!=0):
            k.append(a//b)
            c = a - b*k[i]
            a = b
            b = c
            i+=1;

        p = [0]*(i)
        p[0]=1
        for j in range(1,i):
            if (j!=1):
                p[j] = p[j-1]*k[j]+p[j-2]
            else:
                p[j]=k[j]

        if ((len(p)-2)%2==0):                   # если получилось отрицательное по модулю число, то делаем его положительным
            return p[len(p)-2]
        else:
            return p[len(p)-1]-p[len(p)-2]
    
    def pow_m(self, message, power, mod):               # (message**b)%m
        result = 1
        bit = message % mod

        while (power > 0):
            if (power & 1 == 1):
                result *= bit
                result %= mod
            bit *= bit
            bit %= mod
            power >>= 1
        
        return result

class pair(object):
    def __init__(self,first_element = 0, second_element = 0):
        self.first_element = first_element
        self.second_element = second_element


 


def AES_encript(data_to_encrypt, key):                      # data encrypt by AES 

    cipher = Rijndael()
    cipher.set_data_to_encrypt(data_to_encrypt)
    key = str(hex(key))[2:]
    cipher.set_key(key)
    
    return cipher.Encrypt()                                 # одна большая строка в 16 cc

def get_data_to_encrypt():                                  # get data from file to encrypt
    data_to_encrypt = ""
    try:                                    
        f = open('data_to_encrypt.txt', 'r')
        data_to_encrypt = f.read()
        f.close()
        data_to_encrypt = data_to_encrypt[:-1]
    except:
        print("No data to encrypt")
    return data_to_encrypt

def AES_decript(data_to_decrypt, key):                      # data (in hex) decrypt by AES
    cipher = Rijndael()
    cipher.set_data_to_decrypt(data_to_decrypt)
    key = str(hex(key))[2:]
    cipher.set_key(key)
    
    return cipher.Decript()                                 # одна большая строка в 10 cc

def hex_to_str(hex_str):                                    # hex data to char UTF-8
    data = ''
    for i in range (0,len(hex_str),2):
       data+=chr(int(hex_str[i:i+2],16))
    return data


if __name__ == "__main__":

    print("Select algoritm:\n1 - AES;\n2 - SHA256;\n3 - RSA;")
    choice = int(input("Input number of algoritm: "))
    
    if choice == 1 or choice == 0:
        #----------------------AES----------------------
        secret_key_for_AES = 111

        # data_to_encrypt = get_data_to_encrypt()
        # data_to_encrypt = "Hi Bro! How are YOU!!!!!!!"
        data_to_encrypt = input("Input data to encrypt:")
        encrypt_data = AES_encript(data_to_encrypt, secret_key_for_AES)        
        print("Encrypt data:", encrypt_data)


        decrypt_data = AES_decript(encrypt_data, secret_key_for_AES)
        decrypt_data = hex_to_str(decrypt_data)
        print("Decrypt data:", decrypt_data)
    if choice == 2 or choice == 0:
        #---------------------SHA256---------------------
        data = "Hi bro!!!! I care about you!"
        message_hash = Sha256(data)
        hash = message_hash.hexdigest()

        print("\nData hash:", hash)
    if choice == 3 or choice == 0:
        #-----------------------RSA-----------------------
        RSA_c = RSA(3557, 2579, 3)

        data = 111111

        # decrypt_data = prepare_data_to_encrypt_int(data)

        encrypt_by_RSA_message = RSA_c.encrypt(data)
        print("Encrypt data:", encrypt_by_RSA_message)

        decrypt_by_RSA_message = RSA_c.decrypt(encrypt_by_RSA_message)
        print("Decrypt data:", decrypt_by_RSA_message)



