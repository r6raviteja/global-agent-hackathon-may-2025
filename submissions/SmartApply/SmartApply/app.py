import pandas as pd
import subprocess

df = pd.read_csv("JobsData.csv")
num_job = 4 -2  # len(df)-1 #

l = len(df)
if num_job > l:
    print(f"Job {num_job} is out of range. There are only {l} jobs.")
    exit()

for i in range(1):
    print(f"Applying to job {num_job}...")
    subprocess.run(["python", "1Score.py", str(num_job)])
    subprocess.run(["python", "2CL.py", str(num_job)])
    subprocess.run(["python", "3Bro5.py", str(num_job)])
    subprocess.run(["python", "4Mail.py", str(num_job)])



