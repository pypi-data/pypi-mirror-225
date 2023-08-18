from hak.pxyz import f as pxyz

def f(list, item):
  result = []
  for _ in list:
    result.append(item)
    result.append(_)
  result.append(item)
  return result

def t():
  x = {
    'list': [0, 1, 2, 3, 4, 5],
    'item': 'A'
  }
  y = ['A', 0, 'A', 1, 'A', 2, 'A', 3, 'A', 4, 'A', 5, 'A']
  z = f(**x)
  return pxyz(x, y, z)
