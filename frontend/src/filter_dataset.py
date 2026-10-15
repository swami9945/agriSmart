import pandas as pd
import os

input_file = os.path.join("data", "Tomato Leveled Data.csv")
output_file = os.path.join("data", "Tomato Leveled Data Healthy.csv")

df = pd.read_csv(input_file)

df_healthy = df[df["IsDiseased"] == 0]

df_healthy.to_csv(output_file, index=False)

print("Original dataset:", df.shape)
print("Healthy dataset:", df_healthy.shape)
print("\nIsDiseased values:")
print(df_healthy["IsDiseased"].value_counts())

print("\nSaved to:", output_file)