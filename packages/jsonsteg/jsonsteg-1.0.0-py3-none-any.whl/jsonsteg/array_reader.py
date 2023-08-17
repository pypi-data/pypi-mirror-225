from math import floor
from jsonsteg.dict_reader import DictionaryReader

class ArrayReader:
    def __init__(self, data: list[dict]) -> None:
        self._data = data
        self._payload = None

    def _calculate_payload(self) -> None:
        bytes_per_array_item = floor((len(self._data[0].keys())-1) / 8)
        if bytes_per_array_item == 0:
            raise ValueError("Array item must contain at least 9 keys")

        # read data from array items
        self._payload = bytearray()
        for i in range(len(self._data)):
            reader = DictionaryReader(self._data[i])
            if len(reader.payload) < bytes_per_array_item:
                raise RuntimeError(f"read {len(reader.payload)} instead of {bytes_per_array_item}")
            self._payload.extend(reader.payload[:bytes_per_array_item])
        self._payload = bytes(self._payload)

    @property
    def payload(self) -> bytes:
        if self._payload is None:
            self._calculate_payload()
        return self._payload
