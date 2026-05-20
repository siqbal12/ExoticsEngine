import numpy as np
from scipy.stats import norm

def get_differential_payoffs_vanilla(price_paths, args, z_table):
    terminal_stock_values = price_paths[:, -1]
    S0 = float(args['S0'])
    T = float(args['T'])
    vol = float(args['vol'])
    r = float(args['r'])
    K = float(args['K'])
    payoff_type = args['payoffType']
    greek_type = args['greekType']
    delta_t = T / (z_table.shape[1])
    Z_eff = np.sum(np.sqrt(delta_t) * z_table, axis=1) / np.sqrt(T)

    indicator = (terminal_stock_values > K if payoff_type == 'Call' else terminal_stock_values < K).astype(float)

    if greek_type == 'Delta':
        return indicator * terminal_stock_values / S0
    elif greek_type == 'Gamma':
        pass
    elif greek_type == 'Theta':
        return indicator * terminal_stock_values * (r - 0.5*vol*vol + vol*Z_eff/(2*np.sqrt(T)))
    elif greek_type == 'Vega':
        return indicator * terminal_stock_values * (np.sqrt(T)*Z_eff - vol*T)
    elif greek_type == 'Rho':
        return indicator * terminal_stock_values * T


def get_differential_payoffs_arithmetic_asian(price_paths, args, z_table):
    terminal_stock_values = price_paths[:, -1]
    S0 = float(args['S0'])
    T = float(args['T'])
    vol = float(args['vol'])
    r = float(args['r'])
    K = float(args['K'])
    payoff_type = args['payoffType']
    greek_type = args['greekType']
    delta_t = T / (z_table.shape[1])
    Z_eff = np.sum(np.sqrt(delta_t) * z_table, axis=1) / np.sqrt(T)
    averages = np.mean(price_paths, axis=1)
    z_table_used = z_table[:, 1:]
    num_time_steps = z_table_used.shape[1]
    delta_t = T / num_time_steps

    indicator = (averages > K if payoff_type == 'Call' else averages < K).astype(float)

    if greek_type == 'Delta':
        return indicator * np.mean(price_paths / S0, axis=1)
    elif greek_type == 'Gamma':
        pass
    elif greek_type == 'Theta':
        return indicator * terminal_stock_values * (r - 0.5*vol*vol + vol*Z_eff/(2*np.sqrt(T)))
    elif greek_type == 'Vega':
        t_grid = np.linspace(delta_t, T, num_time_steps)
        W = np.cumsum(np.sqrt(delta_t) * z_table_used, axis=1)
        return indicator * np.mean(price_paths * (W - vol * t_grid), axis=1)
    elif greek_type == 'Rho':
        return indicator * terminal_stock_values * T


def get_differential_payoffs(price_paths, args, z_table):
    terminal_stock_values = price_paths[:, -1]
    S0 = float(args['S0'])
    T = float(args['T'])
    vol = float(args['vol'])
    r = float(args['r'])
    K = float(args['K'])
    payoff_type = args['payoffType']
    greek_type = args['greekType']
    delta_t = T / (z_table.shape[1])
    Z_eff = np.sum(np.sqrt(delta_t) * z_table, axis=1) / np.sqrt(T)
    arithmetic_averages = np.mean(price_paths, axis=1)
    geometric_averages = np.exp(np.mean(np.log(price_paths), axis=1))
    z_table_used = z_table[:, 1:]
    num_time_steps = z_table_used.shape[1]
    delta_t = T / num_time_steps

    W_full = np.zeros((price_paths.shape[0], num_time_steps + 1))
    if num_time_steps > 0:
        W_full[:, 1:] = np.cumsum(np.sqrt(delta_t) * z_table_used, axis=1)

    # mean of W across time steps (including t=0)
    mean_W = np.mean(W_full, axis=1)
    # mean time across time points from 0..T inclusive is T/2 for evenly spaced grid
    mean_t = 0.5 * T

    option_type = args['optionType']
    if option_type == 'Vanilla':

        indicator = (terminal_stock_values > K if payoff_type == 'Call' else terminal_stock_values < K).astype(float)

        if greek_type == 'Delta':
            return indicator * terminal_stock_values / S0
        elif greek_type == 'Gamma':
            pass
        elif greek_type == 'Theta':
            return indicator * terminal_stock_values * (r - 0.5*vol*vol + vol*Z_eff/(2*np.sqrt(T)))
        elif greek_type == 'Vega':
            return indicator * terminal_stock_values * (np.sqrt(T)*Z_eff - vol*T)
        elif greek_type == 'Rho':
            return indicator * terminal_stock_values * T

    elif option_type == 'Arithmetic Asian':

        indicator = (arithmetic_averages > K if payoff_type == 'Call' else arithmetic_averages < K).astype(float)

        if greek_type == 'Delta':
            return indicator * np.mean(price_paths / S0, axis=1)
        elif greek_type == 'Gamma':
            pass
        elif greek_type == 'Theta':
            return indicator * terminal_stock_values * (r - 0.5*vol*vol + vol*Z_eff/(2*np.sqrt(T)))
        elif greek_type == 'Vega':
            t_grid = np.linspace(delta_t, T, num_time_steps)
            W = np.cumsum(np.sqrt(delta_t) * z_table_used, axis=1)
            return indicator * np.mean(price_paths * (W - vol * t_grid), axis=1)
        elif greek_type == 'Rho':
            return indicator * terminal_stock_values * T

    elif option_type == 'Geometric Asian':

        indicator = (geometric_averages > K if payoff_type == 'Call' else geometric_averages < K).astype(float)

        if greek_type == 'Delta':
            return indicator * geometric_averages / S0

        elif greek_type == 'Gamma':
            pass
        elif greek_type == 'Theta':
            return indicator * geometric_averages * (r - 0.5*vol*vol + vol * Z_eff/(2*np.sqrt(T)))

        elif greek_type == 'Vega':
            return indicator * geometric_averages * (mean_W - vol * mean_t)

        elif greek_type == 'Rho':
            return indicator * geometric_averages * mean_t

    else:
        raise Exception(f'Pathwise Differentiation not Supported for {option_type} - Payoff function must be differentiable')

def get_greek_estimator_se(price_paths, args, z_table, calculated_price):

    r = float(args['r'])
    T = float(args['T'])
    greek_type = args['greekType']

    differential_payoffs = get_differential_payoffs(price_paths, args, z_table)
    discounted_differential_payoffs = np.exp(-r*T) * differential_payoffs
    N = len(discounted_differential_payoffs)

    if greek_type in ['Delta', 'Vega']:
        greek_estimator = np.mean(discounted_differential_payoffs)
        greek_std = np.std(discounted_differential_payoffs) / np.sqrt(N)
    elif greek_type == 'Theta':
        greek_estimator = np.mean(discounted_differential_payoffs) - r*calculated_price
        greek_std = np.std(discounted_differential_payoffs) / np.sqrt(N)
    elif greek_type == 'Rho':
        greek_estimator = np.mean(discounted_differential_payoffs) - T*calculated_price
        greek_std = np.std(discounted_differential_payoffs) / np.sqrt(N)

    return greek_estimator, greek_std






