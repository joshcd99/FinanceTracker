import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from finance_calculations import calculate_projection
from datetime import datetime


# Function to calculate the projection and display the results
def on_calculate():
    try:
        # Load the bills and purchases from Excel
        excel_file = '/Users/joshdunlap/Desktop/Financial Projection Sample.xlsx'
        bills_df = pd.read_excel(excel_file, sheet_name='Bills')
        purchases_df = pd.read_excel(excel_file, sheet_name='Planned debits-credits')

        # Get current balance and end date from the user input
        current_balance = float(balance_entry.get())
        end_date_str = end_date_entry.get()

        # Calculate the projected balance using the inputs
        df = calculate_projection(bills_df, purchases_df, current_balance, end_date_str)

        # Ensure the end date is included if missing
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        if pd.to_datetime(df['Date']).iloc[-1] != end_date:
            final_balance = df['Projected Balance'].iloc[-1]
            new_row = pd.DataFrame([{'Date': end_date.strftime('%Y-%m-%d'), 'Projected Balance': final_balance}])
            df = pd.concat([df, new_row], ignore_index=True)

        # Filter the table to only show dates where the balance changed, plus the final day
        filtered_df = filter_projection_table(df)

        # Display the table of projected balances in the Text widget
        display_table(filtered_df)

        # Plot the results in the GUI window
        plot_results(df)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")


# Function to filter the projected balances
def filter_projection_table(df):
    # Filter to keep only the rows where the balance changes
    filtered_df = df[df['Projected Balance'].diff() != 0]

    # Always include the last row (final day) even if there's no change in balance
    if filtered_df.iloc[-1]['Date'] != df.iloc[-1]['Date']:
        filtered_df = pd.concat([filtered_df, df.iloc[[-1]]])

    return filtered_df


# Function to display the results as a table in the Text widget
def display_table(df):
    # Clear previous content in the text widget
    text_widget.delete('1.0', 'end')

    # Format the header
    text_widget.insert('end', f"{'Date':<15} {'Projected Balance':>20}\n")
    text_widget.insert('end', '-' * 35 + '\n')

    # Insert the projected balances
    for index, row in df.iterrows():
        text_widget.insert('end', f"{row['Date']:<15} ${row['Projected Balance']:>20,.2f}\n")


# Function to plot the projected balances
def plot_results(df):
    # Clear previous plots if any
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Create a figure and plot the balance over time
    fig, ax = plt.subplots(figsize=(6, 3))

    # Convert the 'Date' column to datetime and plot the data
    dates = pd.to_datetime(df['Date'])
    balances = df['Projected Balance']
    ax.plot(dates, balances, linestyle='-', color='b')  # Line plot without circles

    # Customize X-axis to show only the final date
    ax.set_xticks([dates.iloc[-1]])  # Set only the final date as a tick
    ax.set_xticklabels([dates.iloc[-1].strftime('%Y-%m-%d')])  # Show only the final date label

    ax.set_title('Projected Balance Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Balance ($)')

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Setting up the Tkinter window
window = Tk()
window.title("Financial Projection Tool")
window.geometry("700x600")

# Adding labels and entry fields for inputs
Label(window, text="Enter Current Balance:").pack()
balance_entry = Entry(window)
balance_entry.pack()

Label(window, text="Enter End Date (YYYY-MM-DD):").pack()
end_date_entry = Entry(window)
end_date_entry.pack()

# Adding a button to calculate projection
Button(window, text="Calculate Projection", command=on_calculate).pack()

# Text widget to display the table of projected balances
Label(window, text="Projected Balances:").pack()
text_widget = Text(window, height=10, width=50)
text_widget.pack()

# Scrollbar for the text widget (optional if there is overflow)
scrollbar = Scrollbar(window, command=text_widget.yview)
text_widget.config(yscrollcommand=scrollbar.set)

# Frame to hold the plot
canvas_frame = Label(window)
canvas_frame.pack()

# Running the Tkinter main loop
window.mainloop()
