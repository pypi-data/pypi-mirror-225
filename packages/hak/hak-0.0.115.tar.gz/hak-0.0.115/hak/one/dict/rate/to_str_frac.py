from hak.one.dict.rate.make import f as make_rate
from hak.pxyz import f as pxyz

# __str__
f = lambda x: f"{x['numerator']}/{x['denominator']}"

def t():
  x = make_rate(710, 113, {'a': 1})
  y = '710/113'
  z = f(x)
  return pxyz(x, y, z)
