import base64
from ever_playground import *

data = "te6ccgEBAgEAKAABAcABAEPQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAg"
data = base64.b64decode(data)
cell = Cell.read(data)
print(cell)

def info(filename: str):
    b = open(filename, "rb").read()
    print(f"bytes {len(b)}")
    cell = Cell.read(b)
    print(f"cells in total {cell.cells_count()}, unique {cell.unique_cells_count()}")
    #print(cell)

info("/tonlabs/sol2tvm/tests2/5253a82a87b58db960a112b6a4be53f160c00fe5940b259979677cbba0ce5f73.tvc")
info("/tonlabs/sol2tvm/tests2/test_mycode.tvc")

from ever_playground import ed25519_new_keypair, Currency

secret, public = ed25519_new_keypair()

c = Currency.from_str("1/3")

exit(0)

text = """
    IFJMPREF {
        DUP
        PUSHINT 429793271
        EQUAL
        IFJMPREF {
            ; CALL $fff$
            DROP
            GETGLOB 6
            THROWIFNOT 76
            LDREF
            ENDS
            CALLREF {
                CALL 1
            }
            IFREF {
                CALL 2
            }
            THROW 0
        }
        DUP
        PUSHINT 567600489
        EQUAL
        ; first .ifjmp (above) gets assembled into pushcont+ifjmp
        ; at this point the code is 33 bytes long (dup, pushint, equal, pushcont+ifjmp, dup, pushint, equal)
        ;
        ; second .ifjmp (below) gets assembled into ifjmpref
        ; because it's body has 2 refs, and we have 2 refs already
        ; (4 refs are forbidden)
        IFJMPREF {
            ; CALL $ffff2$
            DROP
            GETGLOB 6
            THROWIFNOT 76
            LDREF
            ENDS
            CALLREF {
                CALL 3
            }
            OVER
            PUSHCONT {
                PUSH S3
                CTOS
                LDU 2
                LDMSGADDR
                DROP
                NIP
                NEWC
                STSLICECONST xc
                STSLICE
                PUSHINT 2715084137
                STUR 130
                STU 256
                ENDC
                PUSHINT 0
                SENDRAWMSG
            }
            PUSHCONT {
                DROP
            }
            IFELSE
            IFREF {
                CALL 4
            }
            THROW 0
        }
        DUP
        PUSHINT 654916061
        EQUAL
        IFJMPREF {
            ; CALL $setSalt2$
            DROP
            GETGLOB 6
            THROWIFNOT 76
            LDREF
            ENDS
            CALLREF {
                CALL 5
            }
            IFREF {
                CALL 6
            }
            THROW 0
        }
        DUP
        PUSHINT 1457755318
        EQUAL
        PUSHCONT {
            ; CALL $ff$
            DROP
            GETGLOB 6
            THROWIFNOT 76
            GETGLOB 2
            ISNULL
            IFREF {
                CALL 7
            }
;            ENDS
;            CALLREF {
;                CALL 8
;            }
;            OVER
;            PUSHCONT {
;                PUSH S3
;                CTOS
;                LDU 2
;                LDMSGADDR
;                DROP
;                NIP
;                NEWC
;                STSLICECONST xc
;                STSLICE
;                PUSHINT 3605238966
;                STUR 130
;                STU 256
;                ENDC
;                PUSHINT 0
;                SENDRAWMSG
;            }
;            PUSHCONT {
;                DROP
;            }
;            IFELSE
;            CALLREF {
;                CALL 9
;            }
;            THROW 0
        }
        IFJMP
    }
"""
code = assemble(text)
print(code)

