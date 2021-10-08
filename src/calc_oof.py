import sys
import pandas as pd
import numpy as np

oof = pd.read_csv(sys.argv[1])
score = np.abs(oof['oof'].values - oof['pressure'].values).mean()

print(score)

