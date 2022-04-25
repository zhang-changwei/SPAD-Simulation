import numpy as np
import pandas as pd

def save(data:np.ndarray, fp='csv'):
    df = pd.DataFrame(data.T)
    df.to_csv(fp + '.csv', index=False)