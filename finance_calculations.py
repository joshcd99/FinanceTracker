import pandas as pd
from datetime import datetime


def calculate_projection(bills_df, purchases_df, current_balance, end_date_str):
    """
    Calculates projected balances given the bills, purchases, current balance, and an end date.
    """
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    start_date = datetime.today()
    dates = pd.date_range(start=start_date, end=end_date)

    projected_balances = []
    for i, date in enumerate(dates):
        if i == 0:
            daily_balance = current_balance
        else:
            daily_balance = projected_balances[i - 1]['Projected Balance']

        # Deduct due bills for the day
        due_bills = bills_df[bills_df['Due Day'] == date.day]
        for _, bill in due_bills.iterrows():
            daily_balance -= bill['Amount']

        # Deduct planned purchases for the day
        due_purchases = purchases_df[purchases_df['Date'] == date.strftime('%Y-%m-%d')]
        for _, purchase in due_purchases.iterrows():
            daily_balance -= purchase['Amount']

        # Append the calculated balance for this date
        projected_balances.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Projected Balance': daily_balance
        })

    return pd.DataFrame(projected_balances)
