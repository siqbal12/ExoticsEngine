from backend.factories import *

class PricingEngine:
    def __init__(self, data):
        ''' Given the inputs from the user, creates our diffusion model, option, and pricer

        Args:
            - data (dict/json): The input data from the user'''

        self.diffusion_model = DiffusionModelFactory.create(data)
        self.option = OptionFactory.create(data)
        self.pricer = PricerFactory.create(data)

    def price(self):
        ''' Pries the option by simulating paths with the diffusion model,
            then calculating the average discounted payoff with the option

        Return:
            - price (float): The estimated price of the option'''
        return self.pricer.price(self.diffusion_model, self.option)