from AndTools import hexFormat


class pack_u:
    """解包"""

    def __init__(self, data):
        if isinstance(data, str):
            self._byte_data = bytearray.fromhex(data.replace(' ', ''))
        else:
            self._byte_data = data

    def _get_bytes(self, length: int) -> bytes:
        res = self._byte_data[:length]
        self._byte_data = self._byte_data[length:]
        return res

    def get_int(self, length=4):
        """取整数"""
        res = self._get_bytes(length)
        return int.from_bytes(res, 'big')

    def get_long(self):
        """取长整数"""
        res = self._get_bytes(8)
        return int.from_bytes(res, 'big')

    def get_byte(self):
        """取字节"""
        res = self._get_bytes(1)
        return int.from_bytes(res, 'big', signed=True)

    def get_bin(self, length):
        """取字节集"""
        res = self._get_bytes(length)
        return res

    def get_short(self):
        """取短整数"""
        res = self._get_bytes(2)
        return int.from_bytes(res, 'big')

    def get_len(self):
        """取长度"""
        return len(self._byte_data)

    def get_all(self, Hex=False):
        """取全部"""
        res = self._byte_data[:]
        if Hex:
            res = ' '.join(['{:02x}'.format(byte) for byte in res])
        return res


class pack_b:
    """组包
    好像作用不大....
    """

    def __init__(self):
        self._bytes_data = bytearray()

    def add_bin(self, bytes_temp):
        if bytes_temp is not None:
            self._bytes_data.extend(bytes_temp)

    def add_Hex(self, bytes_temp):
        if bytes_temp is not None:
            self._bytes_data.extend(bytearray.fromhex(bytes_temp))

    def add_bytes(self, bytes_temp):
        """字节或字节集"""
        if bytes_temp is not None:
            self._bytes_data.append(bytes_temp)

    def add_int(self, int_temp, length=4):
        """整数
        length:
        int:4
        Short:2
        long:8
        """
        if int_temp is not None:
            self._bytes_data.extend(int_temp.to_bytes(length, 'big'))

    def add_body(self, data, length=4, _hex=False, add_len=0):
        """头部&内容"""
        if data is None:
            return

        if isinstance(data, str):
            bytes_data = bytes.fromhex(data) if _hex else data.encode('utf-8')
        else:
            bytes_data = data

        self.add_int(len(bytes_data) + add_len, length)
        self.add_bin(bytes_data)

    def set_data(self, byte_temp):
        """置数据"""
        if byte_temp is not None:
            self._bytes_data = byte_temp

    def empty(self):
        """清空"""
        self._bytes_data = bytearray()

    def get_bytes(self, Hex=False):
        if Hex:
            _bytes_temp = self._bytes_data.hex()
            _bytes_temp = hexFormat(_bytes_temp)
        else:
            _bytes_temp = self._bytes_data
        return _bytes_temp
