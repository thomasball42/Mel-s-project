# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 12:31:25 2025

@author: tom
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data_out.csv")

df = df[df["count"] > 0]

df = df.sort_values("count", ascending = False)

fig, ax = plt.subplots()

for i, (idx, row) in enumerate(df.iterrows()):
    
    lname = row.long_name
    count = row["count"]
    
    ax.bar(i, count, color = "g", alpha = 0.5)

ax.set_xticks(np.arange(0, len(df), 1), labels = df.long_name, rotation = 90)

fig.set_size_inches(8, 6)
fig.tight_layout()   

fig.savefig("fig.png", dpi = 300)