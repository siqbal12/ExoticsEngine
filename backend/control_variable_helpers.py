import numpy as np
from scipy.stats import norm
from options import *

def vanilla_price(S0, K, r, vol, T, option_type="Call"):
    d1 = (np.log(S0 / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)

    if option_type == "Call":
        return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "Put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

def digital_price(S0, K, r, vol, T, option_type="Call"):
    d2 = (np.log(S0 / K) + (r - 0.5 * vol**2) * T) / (vol * np.sqrt(T))

    if option_type == "Call":
        return np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "Put":
        return np.exp(-r * T) * norm.cdf(-d2)

def geometric_asian_price(S0, K, r, sigma, T, n, option_type="Call"):
    # Adjusted parameters
    sigma_hat = sigma * np.sqrt((n + 1) * (2 * n + 1) / (6 * n**2))
    mu_hat = (r - 0.5 * sigma**2) * (n + 1) / (2 * n) + 0.5 * sigma_hat**2

    d1 = (np.log(S0 / K) + (mu_hat + 0.5 * sigma_hat**2) * T) / (sigma_hat * np.sqrt(T))
    d2 = d1 - sigma_hat * np.sqrt(T)

    discount = np.exp(-r * T)
    forward_adj = S0 * np.exp(mu_hat * T)

    if option_type == "Call":
        return discount * (forward_adj * norm.cdf(d1) - K * norm.cdf(d2))
    elif option_type == "Put":
        return discount * (K * norm.cdf(-d2) - forward_adj * norm.cdf(-d1))

def get_known_expectation(args, control_variable):
    S0 = float(args['S0'])
    K = float(args['K'])
    r = float(args['r'])
    vol = float(args['vol'])
    T = float(args['T'])
    num_steps = float(args['numSteps'])
    if control_variable == 'S(T)':
        #Use S(T) Formula
        return S0 * np.exp(r*T)
    elif control_variable == 'Vanilla Call':
        #Use BS Formula
        return vanilla_price(S0, K, r, vol,T, option_type='Call')
    elif control_variable == 'Vanilla Put':
        #Use BS Formula
        return vanilla_price(S0, K, r, vol,T, option_type='Put')
    elif control_variable == 'Digital Call':
        #Use BS Formula
        return digital_price(S0, K, r, vol,T, option_type='Call')
    elif control_variable == 'Digital Put':
        #Use BS Formula
        return digital_price(S0, K, r, vol,T, option_type='Put')
    elif control_variable == 'Geometric Asian Call':
        #Use BS Formula
        return geometric_asian_price(S0, K, r, vol,T, n=num_steps, option_type='Call')
    elif control_variable == 'Geometric Asian Put':
        #Use BS Formula
        return geometric_asian_price(S0, K, r, vol,T, n=num_steps, option_type='Put')

def get_control_discounted_payoff(args, stock_paths, control_variable):
    if control_variable == 'S(T)':
        terminal_stock_values = stock_paths[:, -1]
        r = float(args['r'])
        T = float(args['T'])
        return np.exp(-r*T) * terminal_stock_values
    elif control_variable in ['Vanilla Call', 'Vanilla Put']:
        control_option = EuropeanOption(args)
        return control_option.discounted_payoff(stock_paths)
    elif control_variable in ['Digital Call', 'Digital Put']:
        control_option = DigitalOption(args)
        return control_option.discounted_payoff(stock_paths)
    elif control_variable in ['Geometric Asian Call', 'Geometric Asian Put']:
        control_option = GeometricAsianOption(args)
        return control_option.discounted_payoff(stock_paths)