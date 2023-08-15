import matplotlib.pyplot as plt
import seaborn as sns

PLOT_DIR = './plots/'


def default_binned_volume_chart(exhibit_dict, col_name):
    df = exhibit_dict['bin_one_way']

    if df.shape[0] >= 1:
        plt.ioff()

        fig, axs = plt.subplots()
        sns.barplot(data=df, x=col_name, y='rec_count', color='steelblue', estimator='sum', errorbar=None, ax=axs)

        plt.savefig(f"{PLOT_DIR}{col_name}.png")
        plt.show()
        plt.clf()
