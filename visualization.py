import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_results(df):
    dates = pd.to_datetime(df['Date'])
    balances = df['Projected Balance']

    fig, ax = plt.subplots()
    ax.plot(dates, balances, marker='o')
    ax.set_title('Projected Balance Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Balance ($)')

    # Show plot
    plt.show()
