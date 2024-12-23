import pandas as pd

df = pd.DataFrame(
    [
        (1, "A", 10, True),
        (2, "B", 12, False),
        (3, "B", 21, False),
        (4, "C", 18, False),
        (5, "A", 13, True),
        (6, "C", 42, True),
        (7, "B", 19, True),
        (8, "A", 21, False),
    ],
    columns=["colA", "colB", "colC", "colD"],
)
print(df)

"""
str_in = ['A', 'B']
#df = df[df.colB.isin(['A', 'C'])]
df = df[df.colB.isin(str_in)]
print(df)

df = df[~df.colB.isin(['A', 'C'])]
print(df)
"""
vals_to_keep = ["A", "B"]
df = df.query("colB in @vals_to_keep")
print(df)
