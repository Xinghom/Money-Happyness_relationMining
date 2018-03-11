# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals

# Common imports
import numpy as np
import os
# Ignore useless warnings
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd 
import sklearn
import sklearn.linear_model

np.random.seed(42)

plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


def save_fig(fig_id, tight_layout=True):
    path = os.path.join("images", fig_id + ".png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)

def prepare_country_stats(oecd_bli, gdp_per_capita):
    oecd_bli = oecd_bli[oecd_bli["INEQUALITY"]=="TOT"]
    oecd_bli = oecd_bli.pivot(index="Country", columns="Indicator", values="Value")
    gdp_per_capita.rename(columns={"2017": "GDP per capita"}, inplace=True)
    gdp_per_capita.set_index("Country", inplace=True)
    full_country_stats = pd.merge(left=oecd_bli, right=gdp_per_capita,
                                  left_index=True, right_index=True)
    full_country_stats.sort_values(by="GDP per capita", inplace=True)
    remove_indices = [0, 1, 6, 8, 33, 34, 35]
    keep_indices = list(set(range(36)) - set(remove_indices))
    return full_country_stats[["GDP per capita", 'Life satisfaction']].iloc[keep_indices]


# load data
life_happyness = pd.read_csv("happyness_2017.csv", thousands=',')
gdp_per_capita = pd.read_csv("GDP_PER_CAPITA.csv", thousands=',', delimiter='\t', encoding='latin1', na_values="n/a")

# preprocess
country_stats = prepare_country_stats(life_happyness, gdp_per_capita)
x = np.c_[country_stats["GDP per capita"]]
y = np.c_[country_stats["Life satisfaction"]]

# visualize
country_stats.plot(kind='scatter', x="GDP per capita", y='Life satisfaction')
save_fig('original_plot')
plt.show()

# model select
lin_reg_mode = sklearn.linear_model.LinearRegression()

# Train
lin_reg_mode.fit(x,y)
t0, t1 = lin_reg_mode.intercept_[0], lin_reg_mode.coef_[0][0]
print("Independent term t0: " + str(t0))
print("coefficient t1 " + str(t1))
country_stats.plot(kind='scatter', x="GDP per capita", y='Life satisfaction')
plt.plot(x, t0 + t1*x, "g")
plt.text(10000, 7, r"$\theta_0 = 5.33$", fontsize=14, color="b")
plt.text(10000, 6.5, r"$\theta_1 = 3.67 \times 10^{-5}$", fontsize=14, color="b")
save_fig('prediction_plot')
plt.show()

#predict
x_new = [[22587]] # Cyprus' GDP PER CAPITA
res = "Cyprus' GDP_PER_CAPITA prediction: " + str(lin_reg_mode.predict(x_new))
print(res)