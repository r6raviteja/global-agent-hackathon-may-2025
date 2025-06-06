import pandas as pd
import subprocess
import sys


df = pd.read_csv("JobsData.csv")
print(df)
num_job = int(sys.argv[1]) if len(sys.argv) > 1 else 0  # Default to 0 if not provided
#num_job =  num_job -1  # len(df)-1 #
print(num_job)

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

sc = df.at[num_job, "score"]

for i in range(1):
    print(f"Applying to job {num_job+1}...")
    if sc==None:
        subprocess.run(["python", "1Score.py", str(num_job)])
    subprocess.run(["python", "2CL.py", str(num_job)])
    subprocess.run(["python", s, str(num_job)])
    subprocess.run(["python", "4Mail.py", str(num_job)])



