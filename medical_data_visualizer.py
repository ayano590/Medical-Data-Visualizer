import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
# read file
df = pd.read_csv('medical_examination.csv')

# 2
# floor division returns inaccurate results, tried this bit of code, from fuzzyray
df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2 > 25).astype(int)

# 3
# set cholesterol and glucose levels to 0 and 1 accordingly
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] != 0, 'cholesterol'] = 1
df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] != 0, 'gluc'] = 1

# 4
# function to draw the plot
def draw_cat_plot():

    # 5
    # convert to long format
    df_cat = df.melt(id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'], value_name='1')
    
    # 6
    # group and calculate the counts for 0 and 1, store in a temporary table
    temp = df_cat.groupby(['cardio', 'variable']).sum().reset_index()
    temp['0'] = df_cat.groupby(['cardio', 'variable']).count().reset_index()['1'] - temp['1']

    # 7
    # melt table again to long format, store in original variable
    df_cat = temp.melt(id_vars=['cardio', 'variable'], value_vars=['0', '1'], var_name='value', value_name='total')

    # 8
    fig = sns.catplot(
    data = df_cat, x = "variable", y = "total", col="cardio",
    hue = 'value', kind = "bar")
    fig = fig.fig  # needed to convert it to a matplotlib object?

    # 9
    # save figure and return it
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():

    # 11
    # clean data
    df_heat = df.loc[(df['height'] >= df['height'].quantile(0.025)) &
                    (df['height'] <= df['height'].quantile(0.975)) &
                    (df['weight'] >= df['weight'].quantile(0.025)) &
                    (df['weight'] <= df['weight'].quantile(0.975)) &
                    (df['ap_lo'] <= df['ap_hi'])]

    # 12
    # calculate correlation matrix
    corr = df_heat.corr()

    # 13
    # create mask for upper triangle
    mask = np.triu(np.ones_like(corr))

    # 14
    # set up plot with matplotlib
    fig, ax = plt.subplots(figsize=(11, 9))

    # 15
    # plot with seaborn
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', ax=ax)

    # 16
    # save fig
    fig.savefig('heatmap.png')
    return fig
