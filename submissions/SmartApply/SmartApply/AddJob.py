import pandas as pd

df = pd.read_csv('JobsData.csv')

# Get the next available index
new_index = len(df)
print(new_index)
with open('JD.txt', 'r', encoding='utf-8') as file:
    combined_value = file.read().strip()  # Get text and remove extra whitespace
# Assign values directly
df.loc[new_index, 'Apply_URL'] = r"https://aroundhome.jobs.personio.de/job/2131369?display=de#apply"

df.loc[new_index, 'Combined'] = combined_value
#df.loc[new_index, 'score'] =65

# Other columns will remain NaN/empty
df.to_csv('JobsData.csv', index=False)