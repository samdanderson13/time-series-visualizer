import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

import matplotlib.ticker as tick

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
    df_period = df.reset_index()
    df_period['month'] = df_period['date'].apply(pd.Period, args=('M'))
    df_period = df_period.drop(columns=['date'])

      # Find average page views per month
    df_month_avg = df_period.groupby('month').mean()

      # Add year column
    df_bar = df_month_avg.reset_index()
    df_bar['year'] = df_bar['month'].apply(lambda x: x.year)

      # Truncate month column
    df_bar['month_trunc'] = df_bar['month'].apply(lambda x: x.month)

    # Draw bar plot
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    month_names = [None,'January','February','March','April','May','June','July','August','September','October','November','December']
    years = df_bar['year'].unique()
    first_year = years[0]
    width = 0.1 # Width of each bar

    # Plot by month
    months = range(1,13)
    for month in months:
        df_month = df_bar.loc[df_bar['month_trunc'] == month]
        # Calculate positions for each month (YY/MM where year zero is 00)
        # 0.0: 00-01, 0.1: 00-02... 1.1: 00-12
        # 2.0: 01-01...
        offset = width * (month-1)
        x = [(2 * (year - first_year)) + offset for year in df_month['year']]
        ax.bar(x, df_month['value'], width, label=month_names[month])

    # Set ticks to the middle of each year's bars
    x_ticks = [((year - first_year) * 2) + (width * (len(months) / 2)) for year in years]
    ax.set_xticks(x_ticks, years)

    ax.legend(fontsize='small')
    ax.set_xlabel('Years', fontsize='small')
    ax.set_ylabel('Average Page Views', fontsize='small')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, ax = plt.subplots(1,2,figsize=(18,8))

    year_plot = sns.boxplot(x=df_box['year'].astype("category"), y=df_box['value'], orient='v', ax=ax[0])

    year_plot.set_title('Year-wise Box Plot (Trend)')
    year_plot.set_xlabel('Year')
    year_plot.set_ylabel('Page Views')

    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_plot = sns.boxplot(x=df_box['month'].astype("category"), y=df_box['value'], orient='v', ax=ax[1], order=month_order)

    month_plot.set_title('Month-wise Box Plot (Seasonality)')
    month_plot.set_xlabel('Month')
    month_plot.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
