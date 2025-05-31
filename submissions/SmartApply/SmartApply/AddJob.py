import pandas as pd

df = pd.read_csv('JobsData.csv')

# Get the next available index
new_index = len(df)
print(new_index)
with open('JD.txt', 'r', encoding='utf-8') as file:
    combined_value = file.read().strip()  # Get text and remove extra whitespace
# Assign values directly
df.loc[new_index, 'Apply_URL'] = r"https://jobs.zalando.com/en/jobs/2718658-Business-Analyst-(all-genders)"

df.loc[new_index, 'Combined'] = combined_value
#df.loc[new_index, 'score'] =65

# Other columns will remain NaN/empty
df.to_csv('JobsData.csv', index=False)