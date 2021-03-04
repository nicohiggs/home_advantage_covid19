from scipy.stats.kde import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt
import pickle

def ridgeline(ax, data, colors, shrink=1, overlap=0, fill=True, labels=None, n_points=1500):
    """
    Creates a standard ridgeline plot.

    data, list of lists.
    overlap, overlap between distributions. 1 max overlap, 0 no overlap.
    fill, matplotlib color to fill the distributions.
    n_points, number of points to evaluate each distribution function.
    labels, values to place on the y axis to describe the distributions.
    """
    if overlap > 1 or overlap < 0:
        raise ValueError('overlap must be in [0 1]')
    xx = np.linspace(-.8, .8, n_points)
    ys = []
    # for i, d in enumerate(np.flip(data, axis=0)):
    for i, d in enumerate(reversed(data)):
        pdf = gaussian_kde(d)
        y = i*(1.0-overlap)
        ys.append(y)
        curve = pdf(xx) / shrink
        if fill:
            ax.fill_between(xx, np.ones(n_points)*y,
                             curve+y, zorder=len(data)-i+1, color=colors[i], alpha=0.70)
        ax.plot(xx, curve+y, c='k', zorder=len(data)-i+1)
    if labels:
        plt.yticks(ys, labels)

plt.rc('grid', linestyle="--")
fsize = (18, 6)
fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=fsize)
shrink=5
with open('./saves/nhl_np_nb', 'rb') as buff:
    data = pickle.load(buff)
model, trace = data['model'], data['trace']
years = ['2020', '2019', '2018', '2017', '2016']
data = trace['home'][:, 1, :].T
colors = ['tab:blue', 'tab:blue', 'tab:blue', 'tab:blue', 'tab:blue']
ridgeline(axs[0], data, colors=colors, shrink=shrink, labels=years, overlap=0)
axs[0].set_title('Regular Season',
          loc='center', fontsize=18)
axs[0].grid(zorder=0)
axs[0].set_xlim(-.4, .4)

years = ['2020', '2019', '2018', '2017', '2016']
data = trace['home'][:, 0, :].T
colors = ['tab:red', 'tab:blue', 'tab:blue', 'tab:blue', 'tab:blue']
ridgeline(axs[1], data, colors=colors, shrink=shrink/1.25, labels=years, overlap=0)
axs[1].set_title('Playoffs',
          loc='center', fontsize=18)

plt.grid(zorder=0)
# fig.xlim(-0.3, 0.3)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel('Estimated Home Advantage Parameter Distribution', fontsize=14)
plt.tight_layout()
plt.savefig('./figures/nhl_ha.pdf', bbox_inches='tight', pad_inches=0.0)
plt.show()


fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=fsize)
shrink=27
with open('./saves/nba_np_nb', 'rb') as buff:
    data = pickle.load(buff)
model, trace = data['model'], data['trace']
years = ['2020', '2019', '2018', '2017', '2016']
data = trace['home'][:, 1, :].T
colors = ['tab:orange', 'tab:orange', 'tab:orange', 'tab:orange', 'tab:orange']
ridgeline(axs[0], data, colors=colors, shrink=shrink, labels=years, overlap=0)
axs[0].set_title('Regular Season',
          loc='center', fontsize=18)
axs[0].grid(zorder=0)
axs[0].set_xlim(-.1, .1)

years = ['2020', '2019', '2018', '2017', '2016']
data = trace['home'][:, 0, :].T
colors = ['tab:red', 'tab:orange', 'tab:orange', 'tab:orange', 'tab:orange']
ridgeline(axs[1], data, colors=colors, shrink=shrink/1.25, labels=years, overlap=0)
axs[1].set_title('Playoffs',
          loc='center', fontsize=18)

plt.grid(zorder=0)
# fig.xlim(-0.3, 0.3)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel('Estimated Home Advantage Parameter Distribution', fontsize=14)
plt.tight_layout()
plt.savefig('./figures/nba_ha.pdf', bbox_inches='tight', pad_inches=0.0)
plt.show()


fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=fsize)
shrink=6
with open('./saves/mlb_np_nb', 'rb') as buff:
    data = pickle.load(buff)
model, trace = data['model'], data['trace']
years = ['2020', '2019', '2018', '2017', '2016']
data = trace['home'][:, 1, :].T
colors = ['tab:red', 'tab:purple', 'tab:purple', 'tab:purple', 'tab:purple']
ridgeline(axs[0], data, colors=colors, shrink=shrink, labels=years, overlap=0)
axs[0].set_title('Regular Season',
          loc='center', fontsize=18)
axs[0].grid(zorder=0)
axs[0].set_xlim(-.6, .6)

years = ['2020', '2019', '2018', '2017', '2016']
data = trace['home'][:, 0, :].T
colors = ['tab:red', 'tab:purple', 'tab:purple', 'tab:purple', 'tab:purple']
ridgeline(axs[1], data, colors=colors, shrink=shrink/1.25, labels=years, overlap=0)
axs[1].set_title('Playoffs',
          loc='center', fontsize=18)

plt.grid(zorder=0)
# fig.xlim(-0.3, 0.3)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel('Estimated Home Advantage Parameter Distribution', fontsize=14)
plt.tight_layout()
plt.savefig('./figures/mlb_ha.pdf', bbox_inches='tight', pad_inches=0.0)
plt.show()


fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=fsize)
shrink=3
with open('./saves/nfl_np_nb', 'rb') as buff:
    data = pickle.load(buff)
model, trace = data['model'], data['trace']
years = ['2020', '2019', '2018', '2017', '2016']
data = trace['home'][:, 1, :].T
colors = ['tab:red', 'tab:green', 'tab:green', 'tab:green', 'tab:green']
ridgeline(axs[0], data, colors=colors, shrink=shrink, labels=years, overlap=0)
axs[0].set_title('Regular Season',
          loc='center', fontsize=18)
axs[0].grid(zorder=0)
axs[0].set_xlim(-.75, .75)

years = ['2020', '2019', '2018', '2017', '2016']
data = trace['home'][:, 0, :].T
colors = ['tab:red', 'tab:green', 'tab:green', 'tab:green', 'tab:green']
ridgeline(axs[1], data, colors=colors, shrink=shrink/1.25, labels=years, overlap=0)
axs[1].set_title('Playoffs',
          loc='center', fontsize=18)

plt.grid(zorder=0)
# fig.xlim(-0.3, 0.3)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel('Estimated Home Advantage Parameter Distribution', fontsize=14)
plt.tight_layout()
plt.savefig('./figures/nfl_ha.pdf', bbox_inches='tight', pad_inches=0.0)
plt.show()
