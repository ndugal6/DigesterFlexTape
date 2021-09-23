# Nicholas Dugal
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns
from matplotlib.colors import ListedColormap

plt.figure(figsize=(15, 15))

mm_to_inch = lambda x: x / 25.4

BIN_STEP_SIZE = 3
BATCH_SIZE = 10

CORROSION_RATE = mm_to_inch(2.5)
SHELL_1 = 12 * 9 + 10
SHELL_2 = 12 * 18 + 8
SHELL_3 = 12 * 27 + 6


def convert_to_inches(df):
    df.x = df.x * 12
    df.y = df.y * 12


def remove_invalids(df):
    df.drop(df[df['considered_valid'] == False].index, inplace=True)


def add_thickness_min(df):
    df['thickness_min'] = df.apply(lambda x: get_thickness_min(x.y), axis=1)


def add_remaining_thickness(df):
    df['remaining_thickness'] = df['thickness'] - df['thickness_min']


def add_remaining_life(df):
    df['remaining_life'] = df['remaining_thickness'] / CORROSION_RATE


def get_thickness_min(height_inches):
    if (height_inches < SHELL_1):
        return 0.824
    elif (height_inches < SHELL_2):
        return 0.803
    elif (height_inches < SHELL_3):
        return 0.784
    else:
        return 0.763


def make_heatmap(df, x, y, key, m_cmap='brg'):
    plt.clf()
    table = df.pivot(y, x, key)  # seems backwards but its a pivot
    ax = sns.heatmap(table, cmap=m_cmap)
    ax.invert_yaxis()
    ax.set_title(f'{key} Heat Map')
    ax.figure.savefig(f'plots/{key}_heatmap.png')
    return ax


def make_heatmap_special(df, x, y, key, color_dict):
    plt.clf()
    table = df.pivot(y, x, key)  # seems backwards but its a pivot
    m_cmap = ListedColormap(list(color_dict.keys()))
    ax = sns.heatmap(table, cmap=m_cmap)
    ax.invert_yaxis()
    ax.set_title(f'{key} Heat Map')
    colorbar = ax.collections[0].colorbar
    r = colorbar.vmax - colorbar.vmin
    n = len(color_dict)
    colorbar.set_ticks([colorbar.vmin + r / n * (0.5 + i) for i in range(n)])
    colorbar.set_ticklabels(list(color_dict.values()))
    ax.figure.savefig(f'plots/{key}_heatmap.png')
    return ax


def make_scatter_plot(df, x, y, c, colormap='viridis'):
    plt.clf()
    df.plot.scatter(x=x, y=y, c=c, colormap=colormap)
    plt.title('Colored scatter of thickness (inches)')
    plt.savefig(f'scatter_plot_{c}.png')
    return plt


# Here we are going to group all the data points in 3x3 in squares together
def group_data_by_steps(df, step_size=BIN_STEP_SIZE, bache_size=None):
    bins = []
    x_min = math.floor(df['x'].min())
    x_max = math.ceil(df['x'].max())

    for i in range(x_min, x_max, step_size):
        restricted = df[(df['x'] < (i + step_size)) & (df['x'] >= i)]
        y_min = math.floor(restricted['y'].min())
        y_max = math.ceil(restricted['y'].max())
        for ii in range(y_min, y_max, step_size):
            binned = restricted[(restricted['y'] < (ii + step_size)) & (restricted['y'] >= ii)]
            binned = binned[0:bache_size]
            binned['binx'] = i
            binned['biny'] = ii
            bins.append(binned)

    return pd.concat(bins)


def agg_data(df):
    aggregrated = df.groupby(['binx', 'biny']).agg(
        {'thickness': ['min'], 'remaining_life': ['min', 'count'], 'remaining_thickness': ['mean']})
    aggregrated.columns = aggregrated.columns.map('_'.join)
    aggregrated.reset_index(level=['binx', 'biny'], inplace=True)
    aggregrated.rename(columns={'remaining_life_count': 'count'}, inplace=True)
    return aggregrated


def map_state_to_number(row):
    if row['count'] < 10:
        return 1
    elif row.remaining_life_min < 0.5:  # since remaining life is in years, 0.5 represents half year
        return 2
    return 3


def main():
    raw_data = pd.read_csv('data/thickness_data.csv')
    remove_invalids(raw_data)
    convert_to_inches(raw_data)
    add_thickness_min(raw_data)
    add_remaining_thickness(raw_data)
    add_remaining_life(raw_data)
    thick_scatter_plot = make_scatter_plot(raw_data, 'x', 'y', 'thickness')

    binned_df = group_data_by_steps(raw_data, BIN_STEP_SIZE)

    aggregated = agg_data(binned_df)

    count_heat = make_heatmap(aggregated, 'binx', 'biny', 'count')
    min_thickness_heat = make_heatmap(aggregated, 'binx', 'biny', 'thickness_min')
    aggregated['remaining_life_min'] = aggregated['remaining_life_min'].clip(
        lower=0)  # replace all negs with 0. If it's at the end of it's life, then its at the end
    min_remaining_life_heat = make_heatmap(aggregated, 'binx', 'biny', 'remaining_life_min')

    aggregated['simple_life'] = aggregated.apply(map_state_to_number, axis=1)

    color_dict = {
        "yellow": "needs manual\n follow up",
        "red": "needs repair",
        "green": "life >= \n6 months"
    }

    min_remaining_life_heat = make_heatmap_special(aggregated, 'binx', 'biny', 'simple_life', color_dict)

    raw_data.sort_values(by='remaining_thickness', inplace=True)
    binned_df = group_data_by_steps(raw_data, BIN_STEP_SIZE, BATCH_SIZE)
    aggregated = agg_data(binned_df)
    remaining_thickness_heat = make_heatmap(aggregated, 'binx', 'biny', 'remaining_thickness_mean')


if __name__ == '__main__':
    main()
