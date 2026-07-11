import kagglehub
import pandas as pd

# Download latest version
# path = kagglehub.dataset_download("aramacus/companion-plants")
path = "C:\Users\user\.cache\kagglehub\datasets\aramacus\companion-plants\versions\3"

print("Path to dataset files:", path)

# Convert files to pandas DataFrames
df = pd.read_csv(f"{path}/companion_plants.csv")