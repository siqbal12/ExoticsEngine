data = {
    "diffusionModelType": "Heston",
    "S0": 100,
    "mu": 0.05,
    "vol": 0.2,
    "T": 1,
    "r": 0.0375,
    "V0": 0.04,
    "kappa": 2.0,
    "theta": 0.04,
    "volvol": 0.5,
    "corr": -0.7,
    "optionType": "Arithmetic Asian",
    "K": 100,
    "T": 1,
    "payoffType": "Call",
    "pricerType": "Monte Carlo",
    "numPaths": 10000,
    "numSteps": 100,
    "varianceReductionType": 'None',
    # "varianceReductionType": 'Antithetic',
    # "varianceReductionType": 'Control',
    # "varianceReductionType": 'StratifiedSampling',
    "controlVariable": 'None',
    # "controlVariable": 'S(T)',
    # "controlVariable": 'Geometric Asian Call',
    # "controlVariable": 'Digital Option',
    "greekType": 'None',
    # "greekType": 'Delta',
    # "greekType": 'Gamma',
    # "greekType": 'Theta',
    # "greekType": 'Vega',
    # "greekType": 'Rho',
}

from backend.pricing_engine import PricingEngine

if __name__ == "__main__":
    price, price_se = PricingEngine(data).price()
    print(f"Estimated Price: {price}")
    print(f"Estimated Price Standard Error: {price_se}")