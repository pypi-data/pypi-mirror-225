from ever_playground import *

code0 = assemble("""
    ; stack to be preserved, here 1 slot
    PUSHINT 111
    ; try cont
    PUSHCONT {
        INC ; update stack [111]
        PUSHINT 222
        ; compiler knows added stack, here it is [222]
        ; drop it
        DROP
        ; pass remaining (and updated) stack to c2 (catch cont)
        PUSHCTR c2
        DEPTH DEC ; r <= 255
        PUSHINT 0 ; n
        SETCONTVARARGS
        POPCTR c2
        ; fire an exception
        THROW 123
    }
    ; catch cont
    PUSHCONT {
        ; do something with exception pair; here, just drop
        DROP2
        ; do somethig else
        PUSHINT 333
    }
    TRY
    PUSHINT 444
""")

# int v = 111;
# try {
#   inc(v);
#   push(222);
#   throw(123);
# } catch (val, exccode) {
#   push(333);
# }
# push(444);
code = assemble("""
    ; stack to be preserved; here, it's 1 slot
    PUSHINT 111
    DEPTH
    ; try cont
    PUSHCONT {
        ; user code 1
        INC
        PUSHINT 222
        PUSHINT 333
        ; pass entire stack to c2 (catch cont) + current stack depth
        DEPTH
        PUSHCTR c2
        DEPTH DEC ; r < 256
        PUSHINT -1 ; nargs
        SETCONTVARARGS
        POPCTR c2
        ; user code 2: fire an exception
        THROW 123
    }
    ; catch cont
    PUSHCONT {
        ; leave only (1) stack being preserved and (2) exc pair
        ; here goes the magic of [n, x1..xn, y1..yk, k+n, v, e] -> [x1..xn, v, e]
        DEPTH DEC ROLLX
        ROLL 3 SUBR DUP
        PUSHINT 2 ADD
        PUSHINT 1
        REVX
        DROPX
        SWAP
        ; do smth with exception pair; here, just drop it
        DROP2
        PUSHINT 444
    }
    XCHG s1, s2
    SETCONTARGS 1, -1
    TRY
    PUSHINT 555
""")

code = assemble("""
    PUSHINT 111
    PUSHCONT {
        PUSHINT 222
        PUSHINT 333
        PUSHCTR c2
        SETCONTARGS 3, -1
        POPCTR c2
        THROW 123
    }
    PUSHCONT {
        PUSHINT 444
    }
    TRY
""")

code = assemble("""
    PUSHCONT {
        PUSHCONT {
            TRUE
        }
        PUSHCONT {
            SAVEALT c2 ;; c1.savelist(2) = c2
            PUSHCONT {
                THROW 111 ;RETALT
            }
            PUSHCONT {
                RETALT
            }
            .blob xf2fe ;; TRYKEEP
        }
        WHILEBRK
    }
    CALLX
    THROW 228
""")

r = runvm(Slice(code), [], capabilities = 0x0020_0000, trace = True)
assert(r.exit_code == 228)
exit(0)

# d c1 c2 - c1 d c2 ; a b c - b a c
# XCHG s1, s2

# [k, x1..xn, y1..yk, v, e] -> [x1..xn, v, e]

r = runvm(Slice(code), [], capabilities = 0x0020_0000, trace = True)
print(r.stack)
assert(r.stack == [112, 444, 555])

code = assemble("""
    PUSHCTR c0
    PUSHCONT {
        JMPX
    }
    PUSHCONT {
    }
    TRY
    THROW 500
""")

code = assemble("""
    PUSHCONT {
        PUSHREF {
            .blob x800000000fffffc00000000002_
            .cell {
            }
        }
        CTOS LDCONT ENDS
        JMPX
    }
    PUSHCONT {
    }
    TRY
    THROW 500
""")
