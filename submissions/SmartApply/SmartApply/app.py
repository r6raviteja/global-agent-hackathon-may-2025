import pandas as pd
import subprocess

df = pd.read_csv("JobsData.csv")
num_job =  2 -2  # len(df)-1 #

l = len(df)
if num_job > l:
    print(f"Job {num_job} is out of range. There are only {l} jobs.")
    exit()

if df.loc[num_job, 'Apply_Source'] == 'ashbyhq':
    s="3Browser_ash.py"
else:
    s="3Browser_other.py"
print(df.loc[num_job, 'Apply_URL'])
print(df.loc[num_job, 'Apply_Source'])

for i in range(1):
    print(f"Applying to job {num_job}...")
    subprocess.run(["python", "1Score.py", str(num_job)])
    subprocess.run(["python", "2CL.py", str(num_job)])
    subprocess.run(["python", s, str(num_job)])
    subprocess.run(["python", "4Mail.py", str(num_job)])



