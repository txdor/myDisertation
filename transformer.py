from pandas import json_normalize

# Step 1: Load JSON Data
with open('AAPL_balanceSheet.json', 'r') as file:
    nested_json_data = json.load(file)

# Step 2: Normalize JSON Data
df = json_normalize(nested_json_data['data'], sep='_')

# Step 3: Export DataFrame to CSV
df.to_csv('AAPL_balanceSheet.csv', index=False)

# # Step 4: Export DataFrame to Excel
# df.to_excel('normalized_financial_data.xlsx', index=False)
