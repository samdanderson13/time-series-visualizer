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

    # OLD: Uses Period columns
    
      # Convert date index to month column
    #print(df.head())
    df_period = df.reset_index()
    #print(df_period.head())
    df_period['month'] = df_period['date'].apply(pd.Period, args=('M'))
    df_period = df_period.drop(columns=['date'])
    #print(df_period.head())

      # Find average page views per month
    df_month_avg = df_period.groupby('month').mean()
    #print(df_month_avg.head())

      # Add year column
    df_bar = df_month_avg.reset_index()
    #print(df_bar.head())
    #df_bar['year'] = df_bar['month'].apply(pd.Period, args=('Y'))
    df_bar['year_trunc'] = df_bar['month'].apply(lambda x: x.year)
    #print(df_bar.head())

      # Truncate month column (not sure if necessary? TBD)
    df_bar['month_trunc'] = df_bar['month'].apply(lambda x: x.month)
    print(df_bar.head())
    print(df_bar.info())
    

    # NEW: Uses DateTime columns
    '''
          # Convert date index to month column
    print(df.head())
    df_period = df.reset_index()
    print(df_period.head())
    #df_period['month'] = df_period['date'].apply(pd.Period, args=('M'))
    df_period['month'] = df_period['date'].apply(lambda x: pd.Timestamp(year = x.year, month = x.month, day = None))
    df_period = df_period.drop(columns=['date'])
    print(df_period.head())

      # Find average page views per month
    df_month_avg = df_period.groupby('month').mean()
    print(df_month_avg.head())

      # Add year column
    df_bar = df_month_avg.reset_index()
    print(df_bar.head())
    #df_bar['year'] = df_bar['month'].apply(pd.Period, args=('Y'))
    df_bar['year'] = df_bar['month'].apply(lambda x: pd.Timestamp(year = x.year, month = None, day = None))
    print(df_bar.head())

      # Truncate month column (not sure if necessary? TBD)
    df_bar['month_trunc'] = df_bar['month'].apply(lambda x: pd.Timestamp(month = x.month, year = None, day = None))
    print(df_bar.head())
    print(df_bar.info())
    '''

    # Draw bar plot
    fig = plt.figure()

    #Step 1: bar chart for 2016
    '''
    ax = fig.add_subplot(1,1,1)
    copy = df_bar.loc[df_bar['year_trunc'] == 2017]
    x = copy['month_trunc']
    height = copy['value']
    ax.bar(x, height)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    '''

    #Step 2: December by year
    '''
    ax = fig.add_subplot(1,1,1)
    december = 12
    dec = df_bar.loc[df_bar['month_trunc'] == december]
    month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']
    ax.bar(dec['year_trunc'], dec['value'], label=month_names[december-1])


    ax.legend()
    ax.set_xlabel('Years')
    years = df_bar['year_trunc'].unique()
    width = 0.25
    num_years = years.size
    x = [i + width for i in range(num_years)]
    print(years)
    print(num_years)
    #ax.set_xticks(x, years)
    ax.set_ylabel('Average Page Views')
    '''


    # Step 3: Plot each month
    '''
    ax = fig.add_subplot(1,1,1)
    month_names = [None,'January','February','March','April','May','June','July','August','September','October','November','December']
    years = df_bar['year_trunc'].unique()
    num_years = years.size
    first_year = years[0]
    print(first_year)
    width = 0.1
    months = range(1,13)

    for month in months:
        df_month = df_bar.loc[df_bar['month_trunc'] == month]
        # Determine relative position:
          # 0 is January of first year
          # 1 is February of first year
          # 13 is January of second year
        x = [(12 * (year - first_year)) + (month - 1) for year in df_month['year_trunc']]
        ax.bar(x, df_month['value'], label=month_names[month])
    

    # Add legends and such
    ax.legend()
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    # Determine relative position:
      # 6 is first year
      # 18 is second year
      # 6 + ((year - first_year) * 12)
    #xticks = [6 + ((year - first_year) * 12) for year in years]
    xticks = [0,1,2,3]
    ax.set_xticks(x, years)
    '''

    # Step 4: Add width
    ax = fig.add_subplot(1,1,1)
    month_names = [None,'January','February','March','April','May','June','July','August','September','October','November','December']
    years = df_bar['year_trunc'].unique()
    num_years = years.size
    first_year = years[0]
    #x = [0,2,4,6] # Base locations: I did the math
    width = 0.1 # Width of each bar
    months = range(1,13)
    for month in months:
        df_month = df_bar.loc[df_bar['month_trunc'] == month]
        offset = width * (month-1)
        x = [(2 * (year - first_year)) + offset for year in df_month['year_trunc']]
        #x_mod = [n + offset for n in x]
        ax.bar(x, df_month['value'], width, label=month_names[month])

    x_ticks = [((year - first_year) * 2) + (width * (len(months) / 2)) for year in years]
    print(x_ticks)
    # ((year - first_year) * 2) + (width * len(months))
    x = [0.6,2.6,4.6,6.6]
    ax.set_xticks(x_ticks, years)
    ax.legend()
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

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
