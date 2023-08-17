from math import floor
from jsonsteg.dict_writer import DictionaryWriter

class ArrayWriter:
    def __init__(self, data: list[dict], payload: bytes) -> None:
        self._data = data
        self._payload = payload
        self._output = None

    def _calculate_output(self) -> None:
        bytes_per_array_item = floor((len(self._data[0].keys())-1) / 8)
        if bytes_per_array_item == 0:
            raise ValueError("Array item must contain at least 9 keys")

        # write data into array items
        self._output = []
        for i in range(0, len(self._payload), bytes_per_array_item):
            payload_chunk = self._payload[i:i+bytes_per_array_item]
            writer = DictionaryWriter(self._data.pop(0), payload_chunk)
            self._output.append(writer.output)
        self._output.extend(self._data)

    @property
    def output(self) -> list[dict]:
        if self._output is None:
            self._calculate_output()
        return self._output
