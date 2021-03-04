import pandas as pd
import numpy as np
import pymc3 as pm, theano.tensor as tt
import arviz as az
import xarray as xr
import matplotlib.pyplot as plt
import pickle


def fit_poisson_model(df):
    # for cross-validation to work we need an arviz inference data object
    dims = {
        "home_points": ["match"],
        "away_points": ["match"],
        "home_team": ["match"],
        "away_team": ["match"],
        "atts": ["team"],
        "atts_star": ["team"],
        "defs": ["team"],
        "defs_star": ["team"],
    }

    num_teams = len(df.home_team_id.unique())
    num_seasons = len(df.season.unique())
    with pm.Model() as pois_model:
        # for loo
        home_team = pm.Data("home_team", df.home_team_id)
        away_team = pm.Data("away_team", df.away_team_id)

        sd_att = pm.HalfNormal('sd_att', sigma=1)
        sd_def = pm.HalfNormal('sd_def', sigma=1)
        home = pm.Normal('home', mu=0, sigma=1, shape=(2, num_seasons))

        intercept = pm.Normal('intercept', mu=np.log(df.away_points.mean()), sigma=np.log(df.away_points.var()), shape=(2, num_seasons))

        atts_star = pm.Normal("atts_star", mu=0, sigma=sd_att, shape=(num_teams, num_seasons))
        defs_star = pm.Normal("defs_star", mu=0, sigma=sd_def, shape=(num_teams, num_seasons))

        atts = pm.Deterministic('atts', atts_star - tt.mean(atts_star))
        defs = pm.Deterministic('defs', defs_star - tt.mean(defs_star))
        home_theta = tt.exp(intercept[df.regular_season, df.season] + home[df.regular_season, df.season] + atts[df.home_team_id, df.season] + defs[df.away_team_id, df.season])
        away_theta = tt.exp(intercept[df.regular_season, df.season] + atts[df.away_team_id, df.season] + defs[df.home_team_id, df.season])
        home_points = pm.Poisson('home_points', mu=home_theta, observed=df.home_points)
        away_points = pm.Poisson('away_points', mu=away_theta, observed=df.away_points)

        pois_trace = pm.sample(2000, tune=1000, cores=4)
        # for loo
        pdata = az.from_pymc3(pois_trace, dims=dims)

    # define helpers to make answer less verbose
    log_lik = pdata.log_likelihood
    const = pdata.constant_data
    pdata.sample_stats["log_likelihood"] = xr.concat(
        (log_lik.home_points, log_lik.away_points),
        "match"
    ).rename({"match": "observation"})

    return pois_model, pois_trace, pdata


def fit_nb_model(df):
    # for cross-validation to work we need an arviz inference data object
    dims = {
        "home_points": ["match"],
        "away_points": ["match"],
        "home_team": ["match"],
        "away_team": ["match"],
        "atts": ["team"],
        "atts_star": ["team"],
        "defs": ["team"],
        "defs_star": ["team"],
    }
    num_teams = len(df.home_team_id.unique())
    num_seasons = len(df.season.unique())
    with pm.Model() as nb_model:
        # for loo
        home_team = pm.Data("home_team", df.home_team_id)
        away_team = pm.Data("away_team", df.away_team_id)

        sd_att = pm.HalfNormal('sd_att', sigma=1)
        sd_def = pm.HalfNormal('sd_def', sigma=1)
        home = pm.Normal('home', mu=0, sigma=1, shape=(2, num_seasons))
        alpha = pm.Uniform('alpha', 0, 2000)

        intercept = pm.Normal('intercept', mu=np.log(df.away_points.mean()), sigma=np.log(df.away_points.var()), shape=(2, num_seasons))

        atts_star = pm.Normal("atts_star", mu=0, sigma=sd_att, shape=(num_teams, num_seasons))
        defs_star = pm.Normal("defs_star", mu=0, sigma=sd_def, shape=(num_teams, num_seasons))

        atts = pm.Deterministic('atts', atts_star - tt.mean(atts_star))
        defs = pm.Deterministic('defs', defs_star - tt.mean(defs_star))
        home_theta = tt.exp(intercept[df.regular_season, df.season] + home[df.regular_season, df.season] + atts[df.home_team_id, df.season] + defs[df.away_team_id, df.season])
        away_theta = tt.exp(intercept[df.regular_season, df.season] + atts[df.away_team_id, df.season] + defs[df.home_team_id, df.season])
        home_points = pm.NegativeBinomial('home_points', mu=home_theta, alpha=home_theta*alpha, observed=df.home_points)
        away_points = pm.NegativeBinomial('away_points', mu=away_theta, alpha=away_theta*alpha, observed=df.away_points)

        nb_trace = pm.sample(2000, tune=1000, cores=4)
        # for loo
        ndata = az.from_pymc3(nb_trace, dims=dims)

    # define helpers to make answer less verbose
    log_lik = ndata.log_likelihood
    const = ndata.constant_data
    ndata.sample_stats["log_likelihood"] = xr.concat(
        (log_lik.home_points, log_lik.away_points),
        "match"
    ).rename({"match": "observation"})

    return nb_model, nb_trace, ndata


def fit_norm_model(df):
    # for cross-validation to work we need an arviz inference data object
    dims = {
        "home_points": ["match"],
        "away_points": ["match"],
        "home_team": ["match"],
        "away_team": ["match"],
        "atts": ["team"],
        "atts_star": ["team"],
        "defs": ["team"],
        "defs_star": ["team"],
    }
    num_teams = len(df.home_team_id.unique())
    num_seasons = len(df.season.unique())
    with pm.Model() as norm_model:
        # for loo
        home_team = pm.Data("home_team", df.home_team_id)
        away_team = pm.Data("away_team", df.away_team_id)

        sd_att = pm.HalfNormal('sd_att', sigma=1)
        sd_def = pm.HalfNormal('sd_def', sigma=1)
        home = pm.Normal('home', mu=0, sigma=1, shape=(2, num_seasons))
        alpha = pm.HalfNormal('alpha', sigma=50)

        intercept = pm.Normal('intercept', mu=np.log(df.away_points.mean()), sigma=np.log(df.away_points.var()), shape=(2, num_seasons))

        atts_star = pm.Normal("atts_star", mu=0, sigma=sd_att, shape=(num_teams, num_seasons))
        defs_star = pm.Normal("defs_star", mu=0, sigma=sd_def, shape=(num_teams, num_seasons))

        atts = pm.Deterministic('atts', atts_star - tt.mean(atts_star))
        defs = pm.Deterministic('defs', defs_star - tt.mean(defs_star))
        home_theta = tt.exp(intercept[df.regular_season, df.season] + home[df.regular_season, df.season] + atts[df.home_team_id, df.season] + defs[df.away_team_id, df.season])
        away_theta = tt.exp(intercept[df.regular_season, df.season] + atts[df.away_team_id, df.season] + defs[df.home_team_id, df.season])
        home_points = pm.Normal('home_points', mu=home_theta, sigma=alpha, observed=df.home_points)
        away_points = pm.Normal('away_points', mu=away_theta, sigma=alpha, observed=df.away_points)

        norm_trace = pm.sample(2000, tune=1000, cores=4)
        # for loo
        normdata = az.from_pymc3(norm_trace, dims=dims)

    # define helpers to make answer less verbose
    log_lik = normdata.log_likelihood
    const = normdata.constant_data
    normdata.sample_stats["log_likelihood"] = xr.concat(
        (log_lik.home_points, log_lik.away_points),
        "match"
    ).rename({"match": "observation"})

    return norm_model, norm_trace, normdata


if __name__ == '__main__':

    df = pd.read_csv('./data/curated_csvs/nhl.csv')
    pmodel, ptrace, pdata = fit_poisson_model(df)
    nmodel, ntrace, ndata = fit_nb_model(df)
    normmodel, normtrace, normdata = fit_norm_model(df)
    print('-'*40)
    print('NHL')
    df_comp_loo = az.compare({'pois': pdata, 'nb': ndata, 'norm': normdata})
    print(df_comp_loo)
    df_comp_waic = az.compare({'pois': pdata, 'nb': ndata, 'norm': normdata}, ic='waic')
    print(df_comp_waic)
    print('-'*40)
    with open('./saves/nhl_np_poisson', 'wb') as buff:
        pickle.dump({'model': pmodel, 'trace': ptrace}, buff)
    with open('./saves/nhl_np_nb', 'wb') as buff:
        pickle.dump({'model': nmodel, 'trace': ntrace}, buff)
    with open('./saves/nhl_np_norm', 'wb') as buff:
        pickle.dump({'model': normmodel, 'trace': normtrace}, buff)


    df = pd.read_csv('./data/curated_csvs/nba.csv')
    pmodel, ptrace, pdata = fit_poisson_model(df)
    nmodel, ntrace, ndata = fit_nb_model(df)
    normmodel, normtrace, normdata = fit_norm_model(df)
    print('-'*40)
    print('NBA')
    df_comp_loo = az.compare({'pois': pdata, 'nb': ndata, 'norm': normdata})
    print(df_comp_loo)
    df_comp_waic = az.compare({'pois': pdata, 'nb': ndata, 'norm': normdata}, ic='waic')
    print(df_comp_waic)
    print('-'*40)
    with open('./saves/nba_np_poisson', 'wb') as buff:
        pickle.dump({'model': pmodel, 'trace': ptrace}, buff)
    with open('./saves/nba_np_nb', 'wb') as buff:
        pickle.dump({'model': nmodel, 'trace': ntrace}, buff)
    with open('./saves/nba_np_norm', 'wb') as buff:
        pickle.dump({'model': normmodel, 'trace': normtrace}, buff)


    df = pd.read_csv('./data/curated_csvs/mlb.csv')
    pmodel, ptrace, pdata = fit_poisson_model(df)
    nmodel, ntrace, ndata = fit_nb_model(df)
    normmodel, normtrace, normdata = fit_norm_model(df)
    print('-'*40)
    print('MLB')
    df_comp_loo = az.compare({'pois': pdata, 'nb': ndata, 'norm': normdata})
    print(df_comp_loo)
    df_comp_waic = az.compare({'pois': pdata, 'nb': ndata, 'norm': normdata}, ic='waic')
    print(df_comp_waic)
    print('-'*40)
    with open('./saves/mlb_np_poisson', 'wb') as buff:
        pickle.dump({'model': pmodel, 'trace': ptrace}, buff)
    with open('./saves/mlb_np_nb', 'wb') as buff:
        pickle.dump({'model': nmodel, 'trace': ntrace}, buff)
    with open('./saves/mlb_np_norm', 'wb') as buff:
        pickle.dump({'model': normmodel, 'trace': normtrace}, buff)

    df = pd.read_csv('./data/curated_csvs/nfl.csv')
    pmodel, ptrace, pdata = fit_poisson_model(df)
    nmodel, ntrace, ndata = fit_nb_model(df)
    normmodel, normtrace, normdata = fit_norm_model(df)
    print('-'*40)
    print('NFL')
    df_comp_loo = az.compare({'pois': pdata, 'nb': ndata, 'norm': normdata})
    print(df_comp_loo)
    df_comp_waic = az.compare({'pois': pdata, 'nb': ndata, 'norm': normdata}, ic='waic')
    print(df_comp_waic)
    print('-'*40)
    with open('./saves/nfl_np_poisson', 'wb') as buff:
        pickle.dump({'model': pmodel, 'trace': ptrace}, buff)
    with open('./saves/nfl_np_nb', 'wb') as buff:
        pickle.dump({'model': nmodel, 'trace': ntrace}, buff)
    with open('./saves/nfl_np_norm', 'wb') as buff:
        pickle.dump({'model': normmodel, 'trace': normtrace}, buff)
