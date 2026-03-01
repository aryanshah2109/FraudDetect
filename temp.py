from pathlib import Path

path = Path("src")

for i in path.iterdir():
    print(i)