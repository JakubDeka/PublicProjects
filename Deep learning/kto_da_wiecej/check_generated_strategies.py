import numpy as np


strategy = np.load("strategy.npy", allow_pickle=True)

for coins in [2, 3, 4, 6, 10, 14, 18, 20]:
    print(f" ----- {coins} coins ----- \nstrategy:\n{strategy[coins]}")
