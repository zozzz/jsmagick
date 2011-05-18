
import pckg1.module_a
from pckg1.pckg2 import *
import pckg1.pckg2.module_a as A

A.printGV()

A.GLOBAL_VAR = 10

A.printGV()

class Z(pckg1.module_a.Test):
    pass