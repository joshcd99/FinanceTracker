import pandas as pd
from datetime import datetime, timedelta

# Step 1: Read bills and purchases from the Excel file
# Assuming the file is named 'finances.xlsx' and has two sheets: 'Bills' and 'Planned Purchases'
excel_file = '/Users/joshdunlap/Desktop/Financial Projection Sample.xlsx'
bills_df = pd.read_excel(excel_file, sheet_name='Bills')
purchases_df = pd.read_excel(excel_file, sheet_name='Planned debits-credits')

# Step 2: Ask user for current balance at runtime
current_balance = float(input("Enter your current bank balance: "))

# Ask for the end date of the projection (format: YYYY-MM-DD)
end_date_input = input("Enter the end date for the projection (YYYY-MM-DD): ")
end_date = datetime.strptime(end_date_input, "%Y-%m-%d")

# Step 3: Define the start date (today)
start_date = datetime.today()

# Step 4: Create a date range from today to the end date
dates = pd.date_range(start=start_date, end=end_date)

# Step 5: Initialize the projected balances list
projected_balances = []

# Step 6: Loop through each date, carry over the balance from the previous day
for i, date in enumerate(dates):
    # If it's the first day, start with the current balance
    if i == 0:
        daily_balance = current_balance
    else:
        daily_balance = projected_balances[i-1]['Projected Balance']  # Carry over balance from the previous day

    # Check for bills due on this day
    due_bills = bills_df[bills_df['Due Day'] == date.day]
    for _, bill in due_bills.iterrows():
        daily_balance -= bill['Amount']

    # Check for planned purchases on this day
    due_purchases = purchases_df[purchases_df['Date'] == date.strftime('%Y-%m-%d')]
    for _, purchase in due_purchases.iterrows():
        daily_balance -= purchase['Amount']

    # Append the balance for this day to the list
    projected_balances.append({
        'Date': date.strftime('%Y-%m-%d'),
        'Projected Balance': daily_balance
    })

# Step 7: Convert the projected balances to a DataFrame for easier handling
projection_df = pd.DataFrame(projected_balances)

# Step 8: Ensure the end date is included even if there was no change on that day
if projection_df['Date'].iloc[-1] != end_date.strftime('%Y-%m-%d'):
    end_date_row = pd.DataFrame([{
        'Date': end_date.strftime('%Y-%m-%d'),
        'Projected Balance': daily_balance
    }])
    projection_df = pd.concat([projection_df, end_date_row], ignore_index=True)

# Step 9: Filter the DataFrame to show only the rows where the balance changes or it's the final day
filtered_projection_df = projection_df[
    (projection_df['Projected Balance'].diff() != 0) |  # Balance changed
    (projection_df['Date'] == projection_df.iloc[-1]['Date'])  # Always include the final day
]

# Step 10: Format the output table and display it
pd.set_option('display.float_format', '${:,.2f}'.format)
print(filtered_projection_df.to_string(index=False))  # Print as a clean table without index
