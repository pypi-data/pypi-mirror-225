import sys
from ever_playground import *

# capIhr = 1
capCreateStats = 2
capBounceMsgBody = 4
capReportVersion = 8
# capSplitMergeTransactions = 16
capShortDequeue = 32
# сapFastStorageStat = 128
# capInitCodeHash = 256
# capOffHypercube = 512
# capMyCode = 1024
# capFixTupleIndexBug 4096

def prepare_param8(version: int, capabilities: int) -> Cell:
    return Builder().x("c4").i(32, version).i(64, capabilities).finalize()

# create new value for config param #8
param8 = prepare_param8(20, capCreateStats or capBounceMsgBody or capReportVersion or capShortDequeue)
# check the validity of this value
if not is_valid_config(8, param8):
    raise Exception("not a valid value for chosen configuration parameter")

print(f"Serialized value = {param8}")
filename = sys.argv[1]
open(filename, "wb").write(param8.write(2))
print(f"Saved to file {filename}")

# { dup -1000 = { drop <s ref@ <s 12 u@ 0xFF0 = } {
#   dup -1001 = { drop <s ref@ <s 12 u@ 0xFF0 = } {
#   over null? { 2drop true } {
#   config-valid?
#   } cond } cond } cond
# } : is-valid-config?
