from ever_playground import *

c = Cell("3f6079007fb856b5b20f92fa951be73294f9c378858435ecd401be58dae75b35000001894421978ecc1458621_")
s = Slice(c)

pubkey = s.u(256)
assert(pubkey == 0x3f6079007fb856b5b20f92fa951be73294f9c378858435ecd401be58dae75b35)
timestamp = s.u(64)
assert(timestamp == 0x000001894421978e)
constructed = s.u(1)
assert(constructed == 1)

opt1 = s.u(1)
assert(opt1 == 1)
len1 = s.u(4)
assert(len1 == 3)
val1 = s.u(len1 * 8)
assert(val1 == 0x051618)

opt2 = s.u(1)
assert(opt1 == 1)
len2 = s.u(4)
assert(len2 == 0)
assert(s.is_empty())
