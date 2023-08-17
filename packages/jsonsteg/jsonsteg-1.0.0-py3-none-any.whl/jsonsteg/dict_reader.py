from math import floor
from jsonsteg.utils.byte_converter import bits_to_bytes

class DictionaryReader:
    def __init__(self, data: dict) -> None:
        self._data = data
        self._keys = list(data.keys())
        self._sorted_keys = sorted(self._keys)
        self._payload = None

    def _read_bits_from_keys(self):
        ones_and_zeros = []
        front_index, back_index = 0, len(self._keys)-1      # ordinal expected to be seen next
        for key in self._keys:
            ordinal = self._sorted_keys.index(key)
            if ordinal == front_index and ordinal != back_index:
                ones_and_zeros.append(0)
                front_index += 1
            elif ordinal == back_index and ordinal != front_index:
                ones_and_zeros.append(1)
                back_index -= 1
            else:
                break
        return ones_and_zeros

    def _calculate_payload(self):
        ones_and_zeros = self._read_bits_from_keys()
        
        # clip so that length of ones and zeros is multipla of 8
        ones_and_zeros = ones_and_zeros[:8*floor(len(ones_and_zeros)/8)]

        # make bytes out of bits
        self._payload = bits_to_bytes(ones_and_zeros)

    @property
    def payload(self) -> bytes:
        if self._payload is None:
            self._calculate_payload()
        return self._payload
