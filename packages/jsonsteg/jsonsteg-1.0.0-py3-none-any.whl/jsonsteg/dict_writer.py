from jsonsteg.utils.byte_converter import bytes_to_bits

class DictionaryWriter:
    def __init__(self, data: dict, payload: bytes) -> None:
        self._data = data
        self._payload = payload
        self._keys = sorted(data.keys())
        self._output = None

    def _reorder_keys(self) -> list:
        bits = bytes_to_bits(self._payload)
        ordered_keys = []
        for value in bits:
            key_index = 0 if value == 0 else -1
            ordered_keys.append(self._keys.pop(key_index))
        ordered_keys.extend(self._keys)
        return ordered_keys

    def _calculate_output(self):
        ordered_keys = self._reorder_keys()
        self._output = { key: self._data[key] for key in ordered_keys }

    @property
    def output(self) -> dict:
        if self._output is None:
            self._calculate_output()
        return self._output
