"""
    @author: Nono Saha Cyrille Merleau (@email csaha@aims.edu.gh/nonosaha@mis.mpg.de)
"""

# Import useful libs
import numpy as np
import pandas as pd


import matplotlib.pyplot as plt
import seaborn as sb



ROOT_DATA = "../../../data/rafft/rufft_benchmarks/updated_benchmarks/"


def main() :
    data_all = []
    mxfold_df = pd.read_csv(ROOT_DATA+"tools_comparison/mxfold_scores.csv")
    rafft_df = pd.read_csv(ROOT_DATA+"tools_comparison/rufft_scores.csv")
    rafft_df2 = pd.read_csv(ROOT_DATA+"tools_comparison/fft_100n_50ms_scores.csv")
    rnastructure_df = pd.read_csv(ROOT_DATA+"tools_comparison/rnastructure_scores.csv")
    contrafold_df = pd.read_csv(ROOT_DATA+"tools_comparison/contrafold_scores.csv")
    rnafold_df = pd.read_csv(ROOT_DATA+"tools_comparison/mfe_scores.csv")
    linearfold_df = pd.read_csv(ROOT_DATA+"tools_comparison/linearfold_scores.csv")

    linearfold_lengths = set(linearfold_df["len_seq"].values)
    linerafold_ppv = []
    linerafold_ss = []

    ppv_less = []
    sens_less = []

    ppv_high = []
    sens_high = []


    for l in linearfold_lengths :
        linerafold_ppv += [np.median(linearfold_df[linearfold_df["len_seq"]==l]["pvv"].values)]
        linerafold_ss += [np.median(linearfold_df[linearfold_df["len_seq"]==l]["sens"].values)]
        if l < 200 :
            ppv_less += [np.median(linearfold_df[linearfold_df["len_seq"]==l]["pvv"].values)]
            sens_less += [np.median(linearfold_df[linearfold_df["len_seq"]==l]["sens"].values)]
        else :
            ppv_high += [np.median(linearfold_df[linearfold_df["len_seq"]==l]["pvv"].values)]
            sens_high += [np.median(linearfold_df[linearfold_df["len_seq"]==l]["sens"].values)]


    print("---------------PPV---------------------")
    print("LinearFold: ", np.median(linerafold_ppv), np.median(ppv_less), np.median(ppv_high), linerafold_ppv)
    print("---------------------------------------")
    print("-------------Sensitivity---------------------")
    print("LinearFold: ", np.median(linerafold_ss), np.median(sens_less), np.median(sens_high), linerafold_ss)
    print("---------------------------------------")
    print(len(rafft_df),len(mxfold_df), len(rnafold_df),len(rnastructure_df),len(contrafold_df), len(linearfold_df))

    for vals in rafft_df.values :
        data_all += [[vals[-1], vals[1], vals[4], vals[3], vals[-2], vals[-3], "RAFFT"]]

    for vals in linearfold_df.values :
        if vals[3] >=0 :
            continue
        data_all += [[vals[-1], vals[1], vals[4], vals[3], vals[-2], vals[-3], "LinearFold"]]

    for vals in contrafold_df.values :
        if vals[3] >=0 :
            continue
        data_all += [[vals[-1], vals[1], vals[4], vals[3], vals[-2], vals[-3], "CONTRAfold"]]

    for vals in rafft_df.values :
        val = mxfold_df[mxfold_df["name"]==vals[-1]].values

        if len(val) > 0 :
            val = val[0]
            if val[3] >=0 :
                continue
            data_all += [[val[-1], val[1], val[4], val[3], val[-2], val[-3], "Mxfold2"]]

    for vals in rafft_df.values :
        val = rnafold_df[rnafold_df["name"]==vals[-1]].values
        if len(val) > 0 :
            val = val[0]
            data_all += [[val[-1], val[1], val[4], val[3], val[-2], val[-3], "RNAfold"]]

    for vals in rnastructure_df.values :
        data_all += [[vals[-1], vals[1], vals[4], vals[3], vals[-2], vals[-3], "RNAstructure"]]

    for vals in rafft_df2.values :
        data_all += [[vals[-1], vals[1], vals[4], vals[3], vals[-2], vals[-3], r"RAFFT$^*$"]]

    #for vals in contrafold_df.values :
    #    data_all += [[vals[-1], vals[1], vals[4], vals[3], vals[-2], vals[-3], "CONTRAfold"]]

    #for vals in rnafold_df.values :
    #    data_all += [[vals[-1], vals[1], vals[4], vals[3], vals[-2], vals[-3], "RNAfold"]]


    data_all_df = pd.DataFrame(data_all, columns=["Name", "Length", "Number of BP", "Energy", "PPV", "Sensitivity", "Tool"])

    print("Mxfold2, RNAfold =====" ,len(data_all_df[data_all_df["Tool"]=="Mxfold2"].values), len(data_all_df[data_all_df["Tool"]=="RNAfold"].values))
    print(data_all_df)
    s = 100
    labels= { str(t)+ " - " +str(t+s) : (t, t+s, []) for t in range(min(data_all_df['Length'].values),max(data_all_df['Length'].values),s) if t<528}
    labels[str(528)+ " - " +str(max(data_all_df['Length'].values))] =  (528,max(data_all_df['Length'].values), [])
    print(len(labels))
    new_data = []
    for key in labels.keys() :
        for l in range(labels[key][0],labels[key][1]):
            val = data_all_df[data_all_df["Length"]==l].values.tolist()
            if len(val) > 0 :
                for elt in val :
                    nl = list(elt)
                    new_data += [nl+[key]]
    print(len(data_all), len(new_data))
    new_dt = pd.DataFrame(new_data, columns=["Name", "Length", "Number of BP", "Energy", "PPV", "Sensitivity", "Tool", "Length group"])


    figure = plt.figure(constrained_layout=True, figsize=(8,6))
    gs = figure.add_gridspec(nrows=2, ncols=1, left=0.05, right=0.48, wspace=0.05)
    ax = figure.add_subplot(gs[0,0])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    #sb.set(rc={'figure.figsize': (20., 8.27)})
    #plt.ylabel('Hamming Distance')
    plt.xticks(rotation=90, fontsize=12)
    plt.title("(A)", fontsize=15)
    colors = {
    "RNAfold": "#AAA662",
    "RNAstructure": "#8C000F",
    "LinearFold": "#008000",
    "CONTRAfold": "#F97306",
    "RAFFT": "#ADD8E6",
    "RAFFT$^*$": "#069AF3",
    "Mxfold2" : "#FE420F"
    }
    #sb.set(font_scale = 1)
    #ax.set_ylabel('Hamming distance',fontsize=12)
    #ax.set_xlabel('Length Group', fontsize=12)
    print("Energy", min(new_dt['Energy'].values), max(new_dt['Energy']), new_dt[new_dt['Energy']==max(new_dt['Energy'])])
    sb_bx = sb.boxplot(ax=ax, y='PPV', x='Length group', hue='Tool', data=new_dt, palette=colors)
    plt.legend([],[], frameon=False)
    sb_bx.set(xticklabels=[])
    sb_bx.set(xlabel=None)
    sb_bx.set_ylabel("PPV", fontsize=12, fontweight='bold')
    #handles, _ = sb_bx.get_legend_handles_labels()          # Get the artists.
    #sb_bx.legend(handles, ["Lévy mutation", "Local mutation"], loc="best") # Associate manually the artists to a label.


    ax = figure.add_subplot(gs[1,0])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    #sb.set(rc={'figure.figsize': (20., 8.27)})
    #plt.ylabel('Hamming Distance')
    plt.xticks(fontsize=12)
    plt.title("(B)", fontsize=15)
    ax.set_ylabel('Hamming distance',fontsize=12)
    #ax.set_xlabel('Length Group', fontsize=12)

    sb_bx = sb.boxplot(ax=ax, y='Sensitivity', x='Length group', hue='Tool', data=new_dt, palette=colors)

    sb_bx.set_xlabel("Length group", fontsize=12,fontweight='bold')
    sb_bx.set_ylabel("Sensitivity", fontsize=12, fontweight='bold')
    plt.legend(loc="upper left",bbox_to_anchor=(-0.1, 0.8, 0.5, 0.5), ncol=3, fontsize="small")
    #sb_bx.set(xticklabels=[])bbox_to_anchor=(0.5, 0.8, 0.5, 0.5)
    #sb_bx.set(xlabel=None)


    plt.savefig("../../../images/rafft/accuracy.pdf")
    plt.savefig("../../../images/rafft/accuracy.png")
    plt.show()




if __name__ == "__main__" :
    main()
