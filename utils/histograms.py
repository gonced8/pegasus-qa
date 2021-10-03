from sys import argv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SHOW = False
SAVE = True

plt.rcParams.update({"font.size": 16})
plt.rcParams["font.family"] = "serif"


def split_df(df):
    df1, df2 = np.array_split(df, 2)
    return df1, df2


def analyze(filename):
    # Load data
    data = pd.read_csv(filename, sep="\t", index_col=False)

    print(f"Data: {data.size} entries")

    # Consider only rows/samples with all metrics
    data = pd.DataFrame.dropna(data)

    print(f"ROUGE1-R: {data['ROUGE1-R'].size} entries")

    # ROUGE1-R median
    rouge_q1 = data["ROUGE1-R"].quantile(0.25)
    rouge_q3 = data["ROUGE1-R"].quantile(0.75)

    # Plot ROUGE1-R
    fig1, ax1 = plt.subplots()

    ax1.axvline(rouge_q1, color="k", linestyle="dashed", linewidth=2)
    ax1.axvline(rouge_q3, color="k", linestyle="dotted", linewidth=2)
    ax1.hist(
        data["ROUGE1-R"],
        bins=25,
        weights=np.ones_like(data["ROUGE1-R"]) / data["ROUGE1-R"].size,
        edgecolor="white",
    )

    ax1.legend(["$1^{st}$ quartile", "$3^{rd}$ quartile"])
    ax1.set_xlabel("ROUGE1-R")
    ax1.set_ylabel("Relative Frequency [%]")

    # Split dataset in half (ROUGE1-R median)
    rouge_gt, _, _, rouge_lt = np.array_split(
        data.sort_values(by="ROUGE1-R", ascending=False), 4
    )

    print(f"MRR (upper): {rouge_gt['MRR'].size} entries")
    print(f"MRR (lower): {rouge_lt['MRR'].size} entries")

    # MRR quartiles (ROUGE1-R upper half)
    rouge_gt_mrr_q1 = rouge_gt["MRR"].quantile(0.25)
    rouge_gt_mrr_q3 = rouge_gt["MRR"].quantile(0.75)
    rouge_lt_mrr_q1 = rouge_lt["MRR"].quantile(0.25)
    rouge_lt_mrr_q3 = rouge_lt["MRR"].quantile(0.75)

    # Plot MRR
    fig2, ax2 = plt.subplots()

    ax2.hist(
        [rouge_gt["MRR"], rouge_lt["MRR"]],
        weights=[
            np.ones_like(rouge_gt["MRR"]) / rouge_gt["MRR"].size,
            np.ones_like(rouge_lt["MRR"]) / rouge_lt["MRR"].size,
        ],
    )

    ax2.legend(["ROUGE1-R > Q3", "ROUGE1-R < Q1"])
    ax2.set_xlabel("MRR")
    ax2.set_ylabel("Relative Frequency [%]")

    # Split dataset in half (MRR median)
    rouge_gt_mrr_gt, _, _, rouge_gt_mrr_lt = np.array_split(
        rouge_gt.sort_values(by=["MRR", "ROUGE1-R"], ascending=False), 4
    )
    rouge_lt_mrr_gt, _, _, rouge_lt_mrr_lt = np.array_split(
        rouge_lt.sort_values(by=["MRR", "ROUGE1-R"], ascending=False), 4
    )

    print(f"F1 or EM (upper, upper): {rouge_gt_mrr_gt['F1'].size} entries")
    print(f"F1 or EM (upper, lower): {rouge_gt_mrr_lt['F1'].size} entries")
    print(f"F1 or EM (lower, upper): {rouge_lt_mrr_gt['F1'].size} entries")
    print(f"F1 or EM (lower, lower): {rouge_lt_mrr_lt['F1'].size} entries")

    # Split dataset for MRR>0
    # rouge_gt_mrr_gt = rouge_gt[rouge_gt["MRR"] > 0]
    # rouge_gt_mrr_lt = rouge_gt[rouge_gt["MRR"] <= 0]
    # rouge_lt_mrr_gt = rouge_lt[rouge_lt["MRR"] > 0]
    # rouge_lt_mrr_lt = rouge_lt[rouge_lt["MRR"] <= 0]

    # Plot F1 (ROUGE1-R upper half)
    fig3, ax3 = plt.subplots()
    ax3.hist(
        [rouge_gt_mrr_gt["F1"], rouge_gt_mrr_lt["F1"]],
        weights=[
            np.ones_like(rouge_gt_mrr_gt["F1"]) / rouge_gt_mrr_gt["F1"].size,
            np.ones_like(rouge_gt_mrr_lt["F1"]) / rouge_gt_mrr_lt["F1"].size,
        ],
        edgecolor="white",
    )
    ax3.legend(
        ["ROUGE1-R > Q3\n          MRR > Q3", "ROUGE1-R > Q3\n          MRR < Q1"]
    )
    ax3.set_xlabel("F1")
    ax3.set_ylabel("Relative Frequency [%]")

    # Plot F1 (ROUGE1-R lower half)
    fig4, ax4 = plt.subplots()
    ax4.hist(
        [rouge_lt_mrr_gt["F1"], rouge_lt_mrr_lt["F1"]],
        weights=[
            np.ones_like(rouge_lt_mrr_gt["F1"]) / rouge_lt_mrr_gt["F1"].size,
            np.ones_like(rouge_lt_mrr_lt["F1"]) / rouge_lt_mrr_lt["F1"].size,
        ],
    )
    ax4.legend(
        ["ROUGE1-R < Q1\n          MRR > Q3", "ROUGE1-R < Q1\n          MRR < Q1"]
    )
    ax4.set_xlabel("F1")
    ax4.set_ylabel("Relative Frequency [%]")

    # Plot Exact match (ROUGE1-R upper half)
    fig5, ax5 = plt.subplots()
    ax5.hist(
        [rouge_gt_mrr_gt["Exact match"], rouge_gt_mrr_lt["Exact match"]],
        weights=[
            np.ones_like(rouge_gt_mrr_gt["Exact match"])
            / rouge_gt_mrr_gt["Exact match"].size,
            np.ones_like(rouge_gt_mrr_lt["Exact match"])
            / rouge_gt_mrr_lt["Exact match"].size,
        ],
    )
    ax5.legend(
        ["ROUGE1-R > Q3\n          MRR > Q3", "ROUGE1-R > Q3\n          MRR < Q1"]
    )
    ax5.set_xlabel("Exact match")
    ax5.set_ylabel("Relative Frequency [%]")

    # Plot Exact match (ROUGE1-R lower half)
    fig6, ax6 = plt.subplots()
    ax6.hist(
        [rouge_lt_mrr_gt["Exact match"], rouge_lt_mrr_lt["Exact match"]],
        weights=[
            np.ones_like(rouge_lt_mrr_gt["Exact match"])
            / rouge_lt_mrr_gt["Exact match"].size,
            np.ones_like(rouge_lt_mrr_lt["Exact match"])
            / rouge_lt_mrr_lt["Exact match"].size,
        ],
    )
    ax6.legend(
        ["ROUGE1-R < Q1\n          MRR > Q3", "ROUGE1-R < Q1\n          MRR < Q1"]
    )
    ax6.set_xlabel("Exact match")
    ax6.set_ylabel("Relative Frequency [%]")

    if SHOW:
        plt.tight_layout()
        plt.show()

    if SAVE:
        fig1.savefig("plots/rouge1-r.pdf", bbox_inches="tight")
        fig2.savefig("plots/mrr.pdf", bbox_inches="tight")
        fig3.savefig("plots/f1_upper.pdf", bbox_inches="tight")
        fig4.savefig("plots/f1_lower.pdf", bbox_inches="tight")
        fig5.savefig("plots/em_upper.pdf", bbox_inches="tight")
        fig6.savefig("plots/em_lower.pdf", bbox_inches="tight")


def main(filenames):
    for filename in filenames:
        analyze(filename)


if __name__ == "__main__":
    if len(argv) <= 1:
        print("Please specify CSV file to load.")
        print(f"Example: {sys.argv[0]} example_file.csv")
    else:
        main(argv[1:])
