data = {
    "diffusionModelType": "GBM",
    "diffusionModelArgs": {
        "S0": 100,
        "mu": 0.05,
        "vol": 0.2,
        "T": 1,
        "r": 0.0375
    },
    "optionType": "European",
    "optionArgs": {
        "K": 100,
        "T": 1,
        "payoffType": "Put"
    },
    "pricerType": "Monte Carlo",
    "pricerArgs": {
        "numPaths": 10000,
        "numSteps": 100,
        "varianceReductionType": None
    }
}

from backend.pricing_engine import PricingEngine

if __name__ == "__main__":
    price, price_se = PricingEngine(data).price()
    print(f"Estimated Price: {price}")
    print(f"Estimated Price Standard Error: {price_se}")