
def bytes_to_bits(b: bytes) -> list[int]:
    bits = []
    for byte in b:
        str_repr = f"{byte:08b}"
        int_array = [int(x) for x in list(str_repr)]
        bits.extend(int_array)
    return bits

def bits_to_bytes(bits: list[int]) -> bytes:
    b = bytearray()
    for i in range(0, len(bits), 8):
        byte_str = "".join([str(bits[x]) for x in range(i, i+8)])
        b.append(int(byte_str, 2))
    return bytes(b)
