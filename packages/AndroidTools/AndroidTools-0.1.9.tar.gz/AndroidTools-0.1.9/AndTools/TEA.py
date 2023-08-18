import struct


class TEA:
    """QQ TEA 加解密, 64比特明码, 128比特密钥
    这是一个确认线程安全的独立加密模块，使用时必须要有一个全局变量secret_key，要求大于等于16位
    """

    def xor(a, b):
        op = 0xffffffff
        a1, a2 = struct.unpack(b'>LL', a[0:8])
        b1, b2 = struct.unpack(b'>LL', b[0:8])
        return struct.pack(b'>LL', (a1 ^ b1) & op, (a2 ^ b2) & op)

    def code(v, k):
        n = 16
        op = 0xffffffff
        delta = 0x9e3779b9
        k = struct.unpack(b'>LLLL', k[0:16])
        y, z = struct.unpack(b'>LL', v[0:8])
        s = 0
        for i in range(n):
            s += delta
            y += (op & (z << 4)) + k[0] ^ z + s ^ (op & (z >> 5)) + k[1]
            y &= op
            z += (op & (y << 4)) + k[2] ^ y + s ^ (op & (y >> 5)) + k[3]
            z &= op
        r = struct.pack(b'>LL', y, z)
        return r

    def decipher(v, k):
        n = 16
        op = 0xffffffff
        y, z = struct.unpack(b'>LL', v[0:8])
        a, b, c, d = struct.unpack(b'>LLLL', k[0:16])
        delta = 0x9E3779B9
        s = (delta << 4) & op
        for i in range(n):
            z -= ((y << 4) + c) ^ (y + s) ^ ((y >> 5) + d)
            z &= op
            y -= ((z << 4) + a) ^ (z + s) ^ ((z >> 5) + b)
            y &= op
            s -= delta
            s &= op
        return struct.pack(b'>LL', y, z)

    def encrypt(v, key):
        if isinstance(key, str):
            secret_key = bytearray.fromhex(key.replace(' ', ''))
        else:
            secret_key = key

        END_CHAR = b'\0'
        FILL_N_OR = 0xF8
        vl = len(v)
        filln = (8 - (vl + 2)) % 8 + 2
        fills = b''
        for i in range(filln):
            fills = fills + bytes([220])
        v = (bytes([(filln - 2) | FILL_N_OR])
             + fills
             + v
             + END_CHAR * 7)
        tr = b'\0' * 8
        to = b'\0' * 8
        r = b''
        o = b'\0' * 8
        for i in range(0, len(v), 8):
            o = TEA.xor(v[i:i + 8], tr)
            tr = TEA.xor(TEA.code(o, secret_key), to)
            to = o
            r += tr
        return r

    def decrypt(v, key):
        if isinstance(key, str):
            secret_key = bytearray.fromhex(key.replace(' ', ''))
        else:
            secret_key = key
        l = len(v)
        prePlain = TEA.decipher(v, secret_key)
        pos = (prePlain[0] & 0x07) + 2
        r = prePlain
        preCrypt = v[0:8]
        for i in range(8, l, 8):
            x = TEA.xor(TEA.decipher(TEA.xor(v[i:i + 8], prePlain), secret_key), preCrypt)
            prePlain = TEA.xor(x, preCrypt)
            preCrypt = v[i:i + 8]
            r += x
        if r[-7:] != b'\0' * 7:
            return None
        return r[pos + 1:-7]

# data = 'cb 63 ea be db ef f9 ff 79 f8 36 b4 d2 7a e7 0d 67 6e 04 49 a6 fa 9d 83 08 79 8f f2 39 07 25 25 12 28 b1 53 4e 0d d0 1e eb 3f 36 f0 f2 27 1d d0 07 d6 0e 6b bd da 4f fb b7 6a b4 5d 65 5f 03 66 bf 32 88 1e a5 3c 4d f6 a9 7f 9e 53 6b 71 44 c1 49 52 a2 5a 27 34 a2 eb d0 c0 6e df a5 5e 37 b7 90 01 2d 43 9d 3f 18 80 50 0e 81 c9 9b ae a5 2c aa fc 73 33 16 8e 2f 02 a8 1b 00 9b fc f1 ef 9e 48 f9 d1 30 69 45 84 24 a9 99 a1 88 40 09 72 94 20 89 2d 62 5a 5a 7a a1 9f ec a1 ec a8 c2 b5 e3 b7 3d fb 8b 26 63 15 41 fd c3 21 16 f4 1b 2c c0 72 0f cc 2b c1 39 5c ba 9b 37 90 be c8 9e 25 94 d7 6c a4 07 27 45 64 a8 67 73 30 8c c0 83 c4 94 eb 78 d8 32 3a 4e 2d 52 52 b3 62 9d 94 49 35 5d 0f 5f c0 89 bc 58 c8 71 28 fe 45 51 c4 12 60 a8 46 ac 0d 97 dc ab 74 21 7d 9b b7 b8 63 64 e7 c0 62 ea e7 11 5a 75 74 f6 b2 2e 40 af a3 3d 8e 3d 5c 4a 73 53 59 0c 76 71 07 3b 48 e9 35 ba f6 a5 91 3a e0 b2 43 3a fe 67 02 a0 91 c5 6e 27 81 6c e5 ba 1b 63 07 35 fb 2e 07 6c 7f 77 ac cd a8 17 d5 cd 74 84 fd 85 59 0e 60 fe 82 6a 71 b9 9e ef 24 54 c7 61 b7 16 6d 6f e5 e9 97 36 80 60 81 f9 2d 57 05 72 3b 6f cb 5e f9 d3 f7 f8 ee b4 8b 21 0f 7f ec 55 63 2c e2 ee d0 78 5c ac 18 d4 05 ad ca f8 e5 2c 29 a3 5b 89 cb 26 89 ef 0e a6 82 35 61 5e 3b 02 50 b3 48 d2 d6 52 b8 83 f4 da ce e2 1a 7a 94 36 22 61 bf 38 a1 4f 4b 36 1c e6 5a 89 b1 1e c0 6a ef b2 34 3b 39 e7 f1 13 96 c2 9d d8 bc 7d 2c 99 b8 cd fb 5c c8 f8 8a 11 f1 85 e7 76 2e 45 a1 17 7a c4 7c f8 6f 99 97 d6 81 10 ba 30 75 11 e6 6f 33 5a ab 35 bf 4c 0a 31 44 24 cf dd 91 cc e3 a9 67 80 30 d3 bf 6c b5 e4 29 f6 1b 57 35 7d da b4 b8 d1 6f ae df 9d 3d 63 75 88 30 23 11 3b ce 2d 87 1b 5c 48 f4 f8 1a ff 1c 0b a0 0b b6 7b 0e c4 45 2a 20 80 64 a2 ab d6 cb f6 d7 70 c8 bd 34 76 5b 1f 60 6c 71 ea b1 d2 49 0b e4 2b 85 e0 43 2e fe c1 7c 09 3e 9d cd 6c 1a 6c 1d c0 6b 2a f4 f8 82 e1 a1 03 80 63 fa 52 71 fc 67 e4 df 88 95 3d 71 72 ac 77 80 5f f5 d0 63 57 18 a5 c4 fa 56 42 3a 26 b5 d0 05 af f6 ee c5 da 54 90 cc 98 35 81 9d c8 07 a1 70 a5 23 1a 7e 73 23 04 50 d4 1e db 73 d9 2a 05 d3 c4 10 3e 77 f0 90 cc b3 85 f5 cb db fd 60 41 d0 be 99 d6 2a 27 7f 0e e9 00 27 fe 58 64 65 00 5e 55 8c 7e 86 80 2d b1 cc 3a 1f b8 ba 6f fe 07 a6 38 af 53 e5 1d 4c 90 bb ef 98 96 28 32 8f 93 6f a7 8d 6c d3 62 a0 f4 6a a8 79 33 8a c7 69 48 c9 b9 35 d2 11 cc 16 72 03 f6 9c c1 75 09 ed 7d 2a 37 7d 52 a5 6c e3 72 fc 80 85 6d 73 3b 77 f2 26 bf 08 43 fa 44 d1 7b 8d 93 a2 2b af b2 2b 9d 49 16 18 a8 8e a6 0a 94 77 86 1f 4b 9c a8 bb bb e3 8b 02 70 9c 2b 6b 9a d4 be 61 b7 de ee 7e 3c 6c 12 17 56 74 0c e9 96 ea d3 09 93 4c 31 4d 14 f6 3d ed 91 81 18 5f 86 9a 16 96 91 57 92 ff 20 70 1b d6 6e c9 e0 c2 42 af 95 06 80 6c 82 ca 53 5f 50 df 40 54 d1 6f ed 7b f2 18 bc 27 c4 5a a5 a2 3c c2 9d db f2 a5 c9 1e 55 95 26 a8 fb 9f e4 0b 09 f7 c8 22 ba b8 c8 e7 eb 60 35 b4 f3 7d 99 b6 f8 fc 27 79 36 c3 a2 28 d3 90 7b 4b 98 a8 e8 13 12 e4 d0 fa d9 ca 3f 32 f2 5f 45 df 97 e5 0a bd 9e 5b cc 4d c9 60 52 82 be aa e5 ee 53 91 57 fd b6 cf ba 68 d9 25 af 96 18 6a 21 ff 23 11 dd 58 0d 55 e6 f1 55 60 df 2a f9 6b 8c 4d 4b 64 d3 50 cb 22 ed aa 59 ad cd 45 c0 bd 5a 9e fd c4 57 91 e6 d2 c0 ff ce 8c 47 e5 a6 92 7e 86 ce 4d 2c c5 d3 2c c2 6d de b1 79 86 d1 74 00 86 97 f9 66 e5 d4 d2 d9 35 ec 0a 26 61 5c f5 63 9e 20 17 c2 10 75 74 38 5d fc fb 95 55 4d 60 68 85 55 83 74 af b8 a6 dd 08 8e 94 ba 3d 75 bb 67 5d 24 18 c1 42 69 32 5f 51 2f 7f 9b 7a 1e 5e cd 56 e4 d0 72 43 6a d5 cd 91 6c 6e 28 0b 64 d0 cf 53 d6 58 f1 6b 51 52 7d 2a 95 0b 98 01 bc 73 13 32 4c 32 de 0c 66 3c 7a cd 01 a8 c3 38 c9 04 c3 02 49 bf 72 9f 2b 98 fa 33 a4 76 b4 61 22 26 96 e2 3c 40 df 34 c2 36 4a 0a 90 16 47 87 5e ce e4 0f 14 f5 7a 92 63 9c bf 84 06 30 1f ae 0b b0 f6 d1 a8 d5 e6 1d 8c f6 ab f2 56 34 2d e6 e7 11 96 fe 29 d0 f9 12 c9 8c 9d 43 59 26 a6 ec 1f 67 b5 55 c6 22 14 c0 d9 2e cf 5c f7 e0 84 17 07 bb 96 32 0e 75 30 2e 27 66 f1 c7 c8 3a a3 69 b5 4f fc 58 3b 3b 92 c1 a4 86 00 13 d7 cc ca e6 d2 a0 d5 a7 89 d5 98 23 2b 12 a4 fa fd 05 be 15 13 31 f9 8f af f1 b7 46 4d 63 8e c7 cf 52 ad 43 49 64 ac 19 df bb 03 fb 30 17 ec a3 40 44 81 b6 2e 38 ab b0 e8 e9 2f 61 41 4d 44 0e 48 d9 9b 9a 63 78 ac 8d a4 f9 36 16 2f ea ee 87 74 a3 c6 ab 89 23 7c 7c a1 e8 c7 22 15 a2 94 9f c0 cf ad 35 df 90 25 1d 06 da 76 34 6c 3f 6d 36 06 e2 1f da 0d be ed 2f 9a a5 1a 7a 00 a6 0e 64 34 23 1e 13 0a c4 85 40 86 3c b6 69 d3 e8 32 11 43 69 b7 14 44 a2 a6 86 67 50 f7 fa a8 6c 74 35 f0 ff 47 49 1c 6a 5a 60 cd 11 d7 bc 8e 18 20 60 8d 60 e6 13 29 ba 89 f3 a5 3e 3d 2c de 86 49 04 7f af 41 46 15 15 21 de 82 a1 6a 2b e9 61 d7 83 35 80 c0 e4 af 06 5a 12 2e 4e a7 06 26 e1 fa 22 cd 78 ac fb 1b 17 85 23 6f 6b 23 83 c2 ca 78 b8 7a 3f db f7 70 79 22 15 61 0e 34 42 f8 56 4a b1 b1 91 0f 38 55 8e 38 da cf 70 73 a4 28 1a 56 90 29 0e 1f a6 aa c2 56 88 93 9a 1d 73 c6 7d 39 6e d0 7b 9c 19 19 ed 97 4b 2f 5c 09 c1 72 ea 06 89 95 b7 46 63 a6 cc c8 69 23 d0 8e 0d da 5d a8 b3 5b c7 de 27 39 0e 25 95 19 1d af 81 54 d7 98 61 a5 67 f5 2b 1f 0b 09 e7 b6 6a 22 7f 70 01 c1 11 e4 72 aa a4 be 45 e9 32 d7 82 3c b7 e7 82 33 89 d5 a6 3e 69 79 1f e1 6d c6 64 02 c0 4a fa bc 77 2d 9c e7 e9 c1 76 a1 09 86 7a 7f d4 ad dc a8 3a 1d d2 80 17 f1 27 f3 3a a9 a4 0e 97 ad f8 93 37 62 28 32 7a c2 c8 ab 84 21 a3 1c 7a 8e 4e 33 ba b8 2b 0e 2d 1a bd a8 88 18 27 95 60 3c 5d 84 e0 4b d1 72 b3 fa 96 56 0c 68 43 5d bf ca d3 2f e9 53 b6 90 e7 23 50 49 09 ec 88 a3 41 6d 99 c8 25 42 dc d4 c3 b7 57 bf a1 62 c3 51 f1 34 4b 94 d1 82 4c 66 0d 99 33 bc d8 82 aa b9 0e 29 4d 0f ac 8d 94 5a 92 8f db 45 27 4a 2a c9 be 4a 2f b7 c5 34 19 56 26 67 48 50 52 62 13 95 d8 66 72 14 69 f4 7c 1b 99 9c 62 b0 74 c2 97 20 64 91 46 71 a3 85 ca 1d 89 2b 15 d4 51 03 b3 23 4a 0a 84 88 8f c5 3c 3a 7b 1a 34 0e 49 81 bc 69 0d 43 4a 6b 2f 3a 63 c1 5a a9 c6 b2 a9 6b 07 47 f3 75 4d 8a 0f fa 23 ae bb 1a 1f 7b 61 51 36 e0 5c c5 21 9e d3 16 bd 53 20 a8 f4 c3 34 10 d6 f6 06 d9 be d4 ad 31 a3 10 ab f9 5f 77 57 12 95 87 75 16 d2 48 58 ef 88 f7 18 1c 33 70 a4 b8 8f e5 9f ac b8 26 1a ba 77 ac 1e 5c af 3e de ef 0d e3 fd be ac 82 17 a1 15 82 45 3a 29 65 f0 2d 29 de ac 32 ed 67 4e 18 fd e7 1c aa 88 37 65 1d e0 56 73 31 ff 30 5e 53 cf 9a f7 5b 17 c4 0a ff 33 84 81 cf 43 02 e5 ad 9d 45 fe a8 23 59 a3 c9 60 ef a1 fa 29 82 b5 6d 7d 12 60 49 81 72 e1 34 5e 46 57 9c 73 51 4b 9d d3 2b d6 43 8d 11 8d 8d 3e f4 a6 c5 6c 45 07 c2 be c5 af ce ca fb a3 0b 94 09 21 58 b4 e9 9b cb c1 cb d7 22 e7 92 00 dd 6e ce d7 c5 32 03 8c 4e 4c 97 70 4b ef 40 c2 64 ba 8a 1b 9b b4 9a 56 03 fd 70 '
#
# key = '7F9C5F4A38168696190994E1392CDF16'
# bin = bytearray.fromhex(data.replace(' ', ''))
# secret_key = bytearray.fromhex(key.replace(' ', ''))
#
# print(TEA.decrypt(bin, secret_key))
