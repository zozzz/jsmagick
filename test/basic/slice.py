'''
Created on 2011.05.10.

>>> seq[:]                # [seq[0],   seq[1],          ..., seq[-1]    ]
>>> seq[low:]             # [seq[low], seq[low+1],      ..., seq[-1]    ]
>>> seq[:high]            # [seq[0],   seq[1],          ..., seq[high-1]]
>>> seq[low:high]         # [seq[low], seq[low+1],      ..., seq[high-1]]
>>> seq[::stride]         # [seq[0],   seq[stride],     ..., seq[-1]    ]
>>> seq[low::stride]      # [seq[low], seq[low+stride], ..., seq[-1]    ]
>>> seq[:high:stride]     # [seq[0],   seq[stride],     ..., seq[high-1]]
>>> seq[low:high:stride]  # [seq[low], seq[low+stride], ..., seq[high-1]]

@author: Zozzz
'''
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
class t:
    class c:
        b = [1, 2, 3, 4, 5]

print x[:1]
print x[1:]
print x[:]
print x[::2]
print x[::-1]
print x[2:3:9]
print x[2]
print x[t.c.b]
print x["Test"]
print t.c.b[1:1:1]