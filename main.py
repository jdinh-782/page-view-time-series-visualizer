import matplotlib.pyplot as plt
from matplotlib import ticker as ticker
from matplotlib import dates as mpl_date
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=True)
df = pd.DataFrame(df)

# Clean data
df = df[df['value'] <= df['value'].quantile(0.025)]
df = df[df['value'] >= df['value'].quantile(0.975)]
# print(df)


# function to help with visualization 'issues' for bar and box plots
def updated_dataframe_for_visualization_purposes():
    temp_df = pd.read_csv('fcc-forum-pageviews.csv', index_col="date", parse_dates=True)

    # clean data by filtering out days when page views were in top 2.5% or bottom 2.5% of dataset
    bottom = temp_df['value'] <= temp_df['value'].quantile(0.025)
    top = temp_df['value'] >= temp_df['value'].quantile(0.975)

    temp_df = temp_df.drop(index=temp_df[bottom | top].index)

    return temp_df


def draw_line_plot():
    # Draw line plot

    df = updated_dataframe_for_visualization_purposes()

    fig, ax = plt.subplots()
    fig.set_figwidth(14)
    fig.set_figheight(6)

    # ax.plot(df['date'], df['value'])
    ax.plot_date(df.index, df['value'], linestyle="solid", marker=None)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(6 * 30))

    # specific date format for x axis label
    date_format = mpl_date.DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(date_format)

    fig.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # # global df_bar
    #
    # # Copy and modify data for monthly bar plot
    # updated_date_list = []
    # for date in df['date']:
    #     updated_date_list.append(date[:7])
    # df['date'] = updated_date_list
    #
    # df_bar = df.copy()
    # # print(df_bar)
    #
    # month_and_year_list = []
    # for date in df_bar['date']:
    #     if date not in month_and_year_list:
    #         month_and_year_list.append(date)
    #
    # years = []
    # months = []
    # for date in month_and_year_list:
    #     years.append(date[:4])
    #     months.append(date[-2:])
    #
    # # for i in range(0, len(years)):
    # #     s = f"{years[i]}-{months[i]}"
    # #     print(s)
    #
    # # reset the index for smoother indexing operation
    # df_bar = df_bar.reset_index()
    # values = []
    #
    # # track each date and month and calculate average page views of that date and month
    # for i in range(0, len(month_and_year_list)):
    #     value = 0
    #     count = 0
    #
    #     for j in range(0, len(df_bar['date'])):
    #         if df_bar['date'][j] == month_and_year_list[i]:
    #             value += int(df_bar['value'][j])
    #             count += 1
    #     average = value / count
    #     values.append(average)
    #
    # # for i in range(0, len(years)):
    # #     print(f"{years[i]}-{months[i]} \t {values[i]}")
    #
    # df_bar = pd.DataFrame(years, columns=['year'])
    #
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    #
    # for i in range(0, len(months)):
    #     month_num = int(months[i])
    #     months[i] = month_list[month_num - 1]
    #
    # df_bar['month'] = months
    # df_bar['value'] = values
    # # print(df_bar)

    # create another dataframe with index_col="date" to help with bar plot
    temp_df = updated_dataframe_for_visualization_purposes()

    df_bar = temp_df.copy()

    df_bar['year'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.strftime('%B')
    df_grp = df_bar.groupby(['year', 'Month'])
    # series
    df_grp['value'].apply(lambda x: x.mean())

    sns.set_style("ticks")
    g = sns.catplot(data=df_bar, kind='bar', x='year', y='value', hue='Month', ci=None,
                    hue_order=month_list, legend=False, palette="hls")

    # Draw bar plot
    # cat_plot = sns.catplot(data=df_bar, kind='bar', x="year", y='value', hue="month")
    # cat_plot.set_ylabels('value')
    # fig = cat_plot.fig

    # sns.set_style("ticks")
    # g = sns.catplot(data=df_bar, kind='bar', x='year', y='value', hue='month', ci=None,
    #                 legend=False, palette="hls")

    fig = g.fig
    ax = g.ax

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    plt.xticks(rotation=90)
    plt.legend(loc="upper left", title="Month")
    plt.setp(ax.get_legend().get_texts(), fontsize='8')
    plt.setp(ax.get_legend().get_title(), fontsize='8')
    plt.tight_layout()

    # fig.show()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def fixed_boxplot(*args, label=None, **kwargs):
    sns.boxplot(*args, **kwargs, labels=[label])


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    # df_box = df_bar.copy() # enable global df_bar

    temp_df = updated_dataframe_for_visualization_purposes()

    # copy dataframe
    df_box = temp_df.copy()

    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box.sort_values(by=['year', 'date'], ascending=[False, True], inplace=True)

    # Draw box plots (using Seaborn)
    df_box['Page Views'] = df_box['value']
    df_box['Month'] = df_box['month']
    df_box['Year'] = df_box['year']
    # print(df_box)

    g = sns.PairGrid(df_box, x_vars=['Year', 'Month'], y_vars=['Page Views'], palette="hls")
    g.map(fixed_boxplot)

    fig = g.fig
    fig.set_figwidth(16)
    fig.set_figheight(6)
    fig.axes[0].set_ylabel('Page Views')
    fig.axes[1].set_ylabel('Page Views')
    fig.axes[0].set_title('Year-wise Box Plot (Trend)')
    fig.axes[1].set_title('Month-wise Box Plot (Seasonality)')
    plt.tight_layout()

    # fig.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig


if __name__ == "__main__":
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()
