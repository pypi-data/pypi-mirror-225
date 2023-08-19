from ever_playground import *

# def set(dict: Dictionary, key: int, value_bits: int) -> Dictionary:
#     k = Builder().i(32, key).slice()
#     v = Builder().ib("0" * value_bits).slice()
#     dict.add(k, v)
#     return dict

# d = Dictionary(32)
# for i in range(0x0000, 0xffff):
#     d = set(d, i, 1014) # max
# print(len(d))

# d = Dictionary(32)
# for i in range(0x0000, 0xffff):
#     d = set(d, i * 0x1000, 1014)
# print(len(d))

# max = 0
# for value_bits in range(983, 1023):
#     try:
#         d = Dictionary(32)
#         for i in range(0x0000, 0x10000):
#             d = set(d, i * 0x1000 + 0x0000, value_bits)
#             d = set(d, i * 0x1000 + 0x0001, value_bits)
#             d = set(d, i * 0x1000 + 0x0002, value_bits)
#             d = set(d, i * 0x1000 + 0x0003, value_bits)
#             d = set(d, i * 0x1000 + 0x5555, value_bits)
#             d = set(d, i * 0x1000 + 0xaaaa, value_bits)
#             d = set(d, i * 0x1000 + 0xcccc, value_bits)
#             d = set(d, i * 0x1000 + 0xffff, value_bits)
#         assert(len(d) == 0x80000)
#     except:
#         break
#     max = value_bits
#     print(max)

code = assemble("""
    PUSHCONT {
        SWAP
        
    }
    NEWDICT

    NEWC PUSHINT 983 STZEROES
    PUSHINT 0x00000001
    ROT
    PUSHINT 32
    DICTISETB

    NEWC PUSHINT 983 STZEROES
    PUSHINT 0x00000002
    ROT
    PUSHINT 32
    DICTISETB

    NEWC PUSHINT 983 STZEROES
    PUSHINT 0x00000003
    ROT
    PUSHINT 32
    DICTISETB
""")

r = runvm(Slice(code), [], trace = True)
assert(r.exit_code == 0)
