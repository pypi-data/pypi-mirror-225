from ever_playground import *

cc = Continuation(stack = [NaN()])
r = runvm_generic(VmState(cc, SaveList(), Gas(1000000000, 10000)))
assert(r.state.cc.stack == [NaN()])

cc = Continuation(code = Slice(assemble("PUSHCTR c0")))
expected_c0 = Continuation(typ = ContinuationType.create_quit(0))
r = runvm_generic(VmState(cc, SaveList(), Gas(100_000, 10_000)))
assert(r.state.cc.stack == [expected_c0])

# w/o CapTvmBugfixes2022
cc = Continuation(code = Slice(assemble("PUSHCTR c2")))
r = runvm_generic(VmState(cc, SaveList(), Gas(100_000, 10_000)))
assert(r.state.cc.stack == [None])

# w/ CapTvmBugfixes2022
expected_c2 = Continuation(typ = ContinuationType.create_excquit())
r = runvm_generic(VmState(cc, SaveList(), Gas(100_000, 10_000)), capabilities = 0x0020_0000)
assert(r.state.cc.stack == [expected_c2])

# VM will panic with stack overflow if CapStcontNewFormat is not set
panic = assemble("""
    PUSHCONT { }
    PUSHINT 1666
    PUSHCONT { PUSHCONT { } SETCONT c0 } REPEAT
    NEWC
    STCONT
""")
cc = Continuation(code = Slice(panic))
r = runvm_generic(VmState(cc, SaveList(), Gas(1_000_000, 0)), capabilities = 0x0080_0000)

exit(0)

code = a("""
    PUSHINT 0
    PUSHCONT { ; condition
        DUP EQINT 0
    }
    PUSHCONT { ; body
        PUSHINT 31415 EQUAL
        THROWIFNOT 500
        INC
    }
    ; move one item into the stack of the body
    PUSHINT 31415 SWAP SETCONTARGS 1
    WHILE
""")
r = runvm(code, [], trace = True)
assert(r.exit_code == 0)

# code = a("""
#     NEWC ENDC CTOS
#     PUSHINT 100000000
#     REPEATEND
#         DUP SBITS
#         PUSHCONT {
#             DROP
#             NEWC
#             ZERO STUR 256
#             ZERO STUR 256
#             ZERO STUR 256
#             ZERO STUR 255
#             ENDC CTOS
#         }
#         IFNOT
#         LDU 1 SWAP DROP
#         BLKPUSH 15, 0
# """)
# # code = a("""
# #     PUSHINT 0
# #     PUSHINT 1000000
# #     REPEATEND
# #     BLKPUSH 15, 0
# # """)
# r = runvm(code, [], gas_limit = 1_000_000, gas_credit = 0, capabilities = 0x0020_0000)
# print(r.state.gas.used)
# print(r.state.steps)
