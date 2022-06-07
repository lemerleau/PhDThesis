"""
    @author: Nono Saha Cyrille Merleau (@email csaha@aims.edu.gh/nonosaha@mis.mpg.de)
"""

# Import useful libs
import numpy as np
import pandas as pd


import matplotlib.pyplot as plt
import seaborn as sb



ROOT_DATA = "../../../data/rafft/rufft_benchmarks/updated_benchmarks/lags/"


def main() :
    """
    data_df = pd.read_csv(ROOT_DATA+"rufft_time_length_lags_50-1000.csv", ";")
    stack_data_df = pd.read_csv(ROOT_DATA+"../../rufft_time_length_trajectories_50.csv", ";")
    print(data_df.columns)
    figure = plt.figure(constrained_layout=True, figsize=(11,5))
    gs = figure.add_gridspec(nrows=1, ncols=2, left=0.05, right=0.48, wspace=0.05)
    ax = figure.add_subplot(gs[0,0])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlabel("Sequence length", fontsize=12)
    ax.set_ylabel(r"Execution time ($s$)", fontsize=12)
    plt.title(r"(A) Number of positional lags ($n$)", fontsize=12)
    lag_set = set(data_df[" positional_lags"].values)
    for lag in sorted(lag_set):
        df_plot = data_df[data_df[" positional_lags"]==lag]
        df_plot.sort_values(by="length")
        plt.xscale("log")
        plt.yscale('log')
        lengths = set((df_plot["length"].values))
        lengths = sorted(list(lengths))
        mean_times = [np.median(df_plot[df_plot["length"]==l][" time"].values)*(10**-9) for l in lengths]
        print(lengths, mean_times)
        plt.plot(lengths, mean_times, '--o', label=r"$n="+str(lag)+"$")

    plt.legend()

    ax = figure.add_subplot(gs[0,1])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.title(r"(B) Stack size ($N$)", fontsize=12)
    ax.set_xlabel("Sequence length", fontsize=12)
    ax.set_ylabel(r"Execution time ($s$)", fontsize=12)
    print(stack_data_df.columns)
    stack_set = set(stack_data_df[" saved_trajectories"].values)
    for N in sorted(stack_set):
        df_plot = stack_data_df[stack_data_df[" saved_trajectories"]==N]
        df_plot.sort_values(by="length")
        plt.xscale("log")
        plt.yscale('log')
        lengths = set((df_plot["length"].values))
        lengths = sorted(list(lengths))
        mean_times = [np.median(df_plot[df_plot["length"]==l][" time"].values)*(10**-9) for l in lengths]
        print(lengths, mean_times)
        plt.plot(lengths, mean_times, '--o', label=r"$N="+str(N)+"$")


    plt.legend()
    plt.savefig("../../../images/rafft/CPU_time.pdf")
    plt.savefig("../../../images/rafft/CPU_time.png")
    plt.show()
    """

    all_cpu_time = pd.read_csv(ROOT_DATA+"../tools_comparison/executiontime/executiontimes_all.csv")

    print(all_cpu_time)
    regression_data =  {
    'RAFFT': 1.9,
    'RNAfold': 2.7,
    'LinearFold': 1.0,
    'CONTRAfold': 2.6,
    'RNAstructure': 3.0
    }
    figure = plt.figure(constrained_layout=True, figsize=(6,4))
    gs = figure.add_gridspec(nrows=1, ncols=1, left=0.05, right=0.48, wspace=0.05)
    ax = figure.add_subplot(gs[0,0])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlabel("Sequence length", fontsize=12)
    ax.set_ylabel(r"Execution time ($s$)", fontsize=12)
    for tool in set(all_cpu_time["Tool"].values):
        plt.xscale("log")
        plt.yscale("log")
        df_plot = all_cpu_time[all_cpu_time['Tool']==tool]
        df_plot.sort_values(by="length")
        plt.xscale("log")
        plt.yscale('log')
        lengths = set((df_plot["length"].values))
        lengths = sorted(list(lengths))
        if tool == "RAFFT" :
            continue

        if tool == "RNAstructure" or tool== "CONTRAfold":
            mean_times = [np.median(df_plot[df_plot["length"]==l]["time"].values)*(10**-9) for l in lengths]
        else :
            mean_times = [np.median(df_plot[df_plot["length"]==l]["time"].values)for l in lengths]
        if tool == "rufft" :
            tool = "RAFFT"
        plt.plot(lengths,mean_times, "o-", label=tool+r" $\eta="+str(regression_data[tool])+"$")
    plt.legend()
    plt.savefig("../../../images/rafft/All_CPU_time.pdf")
    plt.savefig("../../../images/rafft/All_CPU_time.png")
    plt.show()


if __name__ == "__main__" :
    main()
