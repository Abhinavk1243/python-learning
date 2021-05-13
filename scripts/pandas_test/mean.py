import pandas as pd 
df = pd.DataFrame({"A":[12,None, 5, 1, 1],
                   "B":[7, 2, 54, 3, None],
                   "C":[20, 16, 20, 3, 8],
                   "D":[14, 3, None, 2, 6]})
# mean
"""
sr=df["A"] #series
print(df.mean(axis=1,skipna=True))
print(df.mean(skipna=True))
print(sr.mean())"""
 
#Mad
"""print(df.mad(axis=0,skipna=True))
print(df.mad(axis=1,skipna=True))
print(df["A"].mad)"""

#sem
#print(df.sem())

print(df["A"].value_counts(dropna=False))


