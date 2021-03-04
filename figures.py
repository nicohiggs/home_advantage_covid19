import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
import pymc3 as pm
import arviz as az
from models import fit_poisson_model, fit_nb_model
import pickle

def fix_hist_step_vertical_line_at_end(ax):
    axpolygons = [poly for poly in ax.get_children() if isinstance(poly, mpl.patches.Polygon)]
    for poly in axpolygons:
        poly.set_xy(poly.get_xy()[:-1])

def plot_ppc_custom(ax, model, trace, colors, fontsize=8, bins=30, num_samples=2000):
    cumul = False
    with model:
        ppc = pm.sample_posterior_predictive(trace)
        q = az.from_pymc3(posterior_predictive=ppc, model=model)
        n, bs, ps = ax.hist(q.observed_data['home_points'], bins=bins, cumulative=cumul, histtype='step', density=True, align='left', color='k')
        # bins = list(range(np.unique(q.observed_data['home_points'])[0], np.unique(q.observed_data['home_points'])[-1]))
        # if len(bins) > 25:
        #     bins = list(range(np.unique(q.observed_data['home_points'])[0], np.unique(q.observed_data['home_points'])[-1], 5))
        for i in range(num_samples):
            d = ppc['home_points'][i, :]
            ax.hist(d, bins=bs, cumulative=cumul, histtype='step', density=True, color=colors[0], alpha=0.01, align='left')
        ax.hist(q.observed_data['home_points'], bins=bs, cumulative=cumul, histtype='step', density=True, align='left', color='k')
        ax.hist(ppc['home_points'].flatten(), bins=bs, cumulative=cumul, histtype='step', density=True, color=colors[1],
                linestyle='--', align='left')
        fix_hist_step_vertical_line_at_end(ax)
        custom_lines = [Line2D([0], [0], color=colors[0]),
                Line2D([0], [0], color=colors[1], linestyle='--'),
                Line2D([0], [0], color='k')]
        ax.legend(custom_lines, ['Posterior Predictive', 'Posterior Predictive Mean', 'Observed Data'],
                  loc='upper right', frameon=True, fontsize=fontsize)

fs=14
plt.rc('grid', linestyle="--")
plt.rc('axes', axisbelow=True)

with open('./saves/nhl_np_poisson', 'rb') as buff:
    data = pickle.load(buff)
pmodel, ptrace = data['model'], data['trace']
with open('./saves/nhl_np_nb', 'rb') as buff:
    data = pickle.load(buff)
nmodel, ntrace = data['model'], data['trace']
with open('./saves/nhl_np_norm', 'rb') as buff:
    data = pickle.load(buff)
normmodel, normtrace = data['model'], data['trace']

fig, axs = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(12, 4))
plot_ppc_custom(axs[0], pmodel, ptrace, ['springgreen', 'tab:green'], bins=10)
plot_ppc_custom(axs[1], nmodel, ntrace, ['tab:cyan', 'tab:blue'], bins=10)
plot_ppc_custom(axs[2], normmodel, normtrace, ['tab:pink', 'tab:red'], bins=10)

axs[0].set_title('Poisson Model Fit', fontsize=fs)
axs[1].set_title('Negative Binomial Model Fit', fontsize=fs)
axs[2].set_title('Normal Model Fit', fontsize=fs)
axs[0].grid(zorder=0)
axs[1].grid(zorder=0)
axs[2].grid(zorder=0)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel("Home Points Scored", fontsize=10)
plt.tight_layout()
plt.savefig('./figures/nhl_dist_comparison.pdf', bbox_inches='tight', pad_inches=0.0)
plt.show()


with open('./saves/nba_np_poisson', 'rb') as buff:
    data = pickle.load(buff)
pmodel, ptrace = data['model'], data['trace']
with open('./saves/nba_np_nb', 'rb') as buff:
    data = pickle.load(buff)
nmodel, ntrace = data['model'], data['trace']
with open('./saves/nba_np_norm', 'rb') as buff:
    data = pickle.load(buff)
normmodel, normtrace = data['model'], data['trace']

fig, axs = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(12, 4))
plot_ppc_custom(axs[0], pmodel, ptrace, ['springgreen', 'tab:green'])
plot_ppc_custom(axs[1], nmodel, ntrace, ['tab:cyan', 'tab:blue'])
plot_ppc_custom(axs[2], normmodel, normtrace, ['tab:pink', 'tab:red'])

axs[0].set_title('Poisson Model Fit', fontsize=fs)
axs[1].set_title('Negative Binomial Model Fit', fontsize=fs)
axs[2].set_title('Normal Model Fit', fontsize=fs)
axs[0].grid(zorder=0)
axs[1].grid(zorder=0)
axs[2].grid(zorder=0)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel("Home Points Scored", fontsize=10)
plt.tight_layout()
plt.savefig('./figures/nba_dist_comparison.pdf', bbox_inches='tight', pad_inches=0.0)
plt.show()


with open('./saves/mlb_np_poisson', 'rb') as buff:
    data = pickle.load(buff)
pmodel, ptrace = data['model'], data['trace']
with open('./saves/mlb_np_nb', 'rb') as buff:
    data = pickle.load(buff)
nmodel, ntrace = data['model'], data['trace']
with open('./saves/mlb_np_norm', 'rb') as buff:
    data = pickle.load(buff)
normmodel, normtrace = data['model'], data['trace']

fig, axs = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(12, 4))
plot_ppc_custom(axs[0], pmodel, ptrace, ['springgreen', 'tab:green'])
plot_ppc_custom(axs[1], nmodel, ntrace, ['tab:cyan', 'tab:blue'])
plot_ppc_custom(axs[2], normmodel, normtrace, ['tab:pink', 'tab:red'])

axs[0].set_title('Poisson Model Fit', fontsize=fs)
axs[1].set_title('Negative Binomial Model Fit', fontsize=fs)
axs[2].set_title('Normal Model Fit', fontsize=fs)
axs[0].grid(zorder=0)
axs[1].grid(zorder=0)
axs[2].grid(zorder=0)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel("Home Points Scored", fontsize=10)
plt.tight_layout()
plt.savefig('./figures/mlb_dist_comparison.pdf', bbox_inches='tight', pad_inches=0.0)
plt.show()


with open('./saves/nfl_np_poisson', 'rb') as buff:
    data = pickle.load(buff)
pmodel, ptrace = data['model'], data['trace']
with open('./saves/nfl_np_nb', 'rb') as buff:
    data = pickle.load(buff)
nmodel, ntrace = data['model'], data['trace']
with open('./saves/nfl_np_norm', 'rb') as buff:
    data = pickle.load(buff)
normmodel, normtrace = data['model'], data['trace']

fig, axs = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(12, 4))
plot_ppc_custom(axs[0], pmodel, ptrace, ['springgreen', 'tab:green'], bins=14)
plot_ppc_custom(axs[1], nmodel, ntrace, ['tab:cyan', 'tab:blue'], bins=14)
plot_ppc_custom(axs[2], normmodel, normtrace, ['tab:pink', 'tab:red'], bins=14)

axs[0].set_title('Poisson Model Fit', fontsize=fs)
axs[1].set_title('Negative Binomial Model Fit', fontsize=fs)
axs[2].set_title('Normal Model Fit', fontsize=fs)
axs[0].grid(zorder=0)
axs[1].grid(zorder=0)
axs[2].grid(zorder=0)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel("Home Points Scored", fontsize=10)
plt.tight_layout()
plt.savefig('./figures/nfl_dist_comparison.pdf', bbox_inches='tight', pad_inches=0.0)
plt.show()
