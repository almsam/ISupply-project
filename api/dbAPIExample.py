import pandas as pd
import numpy as np

from dbAPI import *

listofLeaves = getAllLeaves()
# print(listofLeaves)

parent = findParentOf("Truck Wheel")
print(parent)