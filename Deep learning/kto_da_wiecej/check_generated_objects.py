import numpy as np


strategy = np.load("strategy.npy", allow_pickle=True)

print(strategy[10])
