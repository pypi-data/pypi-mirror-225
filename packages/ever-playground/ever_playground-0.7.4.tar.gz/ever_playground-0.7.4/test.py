from ever_playground import *
gen_dict = assemble("""
  PUSHSLICE x0
  PUSHINT 0
  NEWDICT
  PUSHINT 32
  DICTISET
""")
res = runvm(Slice(gen_dict), [])
print(res.state.cc.stack[0])
