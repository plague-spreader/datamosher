from datamoshers import Datamosher
import numpy as np

class RandomDatamosher(Datamosher):
    BLOCK_SIZE = 4096

    def datamosh(self):
        while True:
            data_in = np.frombuffer(self.f_in.read(
                RandomDatamosher.BLOCK_SIZE), dtype=np.uint8)
            if data_in.size == 0:
                break
            rand_data = np.random.randint(256, size=(len(data_in),),
                                          dtype=np.uint8)
            self.f_out.write(np.bitwise_xor(data_in, rand_data))

class MyDatamosher(Datamosher):
    BLOCK_SIZE = 4096

    def __init__(self, f_in, f_out, a, b):
        super().__init__(f_in, f_out)
        self.a = a
        self.b = b

    def datamosh(self):
        while True:
            data_in = np.frombuffer(self.f_in.read(
                MyDatamosher.BLOCK_SIZE), dtype=np.uint8)
            if data_in.size == 0:
                break
            rand_data = []
            x = 0
            while len(rand_data) < len(data_in):
                x = (self.a * x + self.b) % 256
                rand_data.append(x)
            rand_data = np.array(rand_data, dtype=np.uint8)
            self.f_out.write(np.bitwise_xor(data_in, rand_data))

