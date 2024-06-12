import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col='date', parse_dates=['date'])


# Clean data
description = df.describe(percentiles=[0.025, 0.975])
small_cutoff = description.loc['2.5%'][0]
big_cutoff = description.loc['97.5%'][0]
df = df.loc[(df['value'] > small_cutoff) & (df['value'] < big_cutoff)]


def draw_line_plot():
    # Draw line plot
    x = df.index
    y = df['value']

    fig = plt.figure(figsize=(15, 4.8))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x,y)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot

      # Convert date index to month column
    print(df.head())
    df_period = df.reset_index()
    print(df_period.head())
    df_period['month'] = df_period['date'].apply(pd.Period, args=('M'))
    df_period = df_period.drop(columns=['date'])
    print(df_period.head())

      # Find average page views per month
    df_month_avg = df_period.groupby('month').mean()
    print(df_month_avg.head())

      # Add year column
    df_bar = df_month_avg.reset_index()
    print(df_bar.head())
    df_bar['year'] = df_bar['month'].apply(pd.Period, args=('Y'))
    print(df_bar.head())

      # Truncate month column (not sure if necessary? tbd)
    df_bar['month'] = df_bar['month'].apply(lambda x: x.month)
    print(df_bar.head())
    print(df_bar.info())
    

    # Draw bar plot


    fig = plt.figure()


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
