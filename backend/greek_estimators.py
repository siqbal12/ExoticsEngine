from abc import ABC, abstractmethod
import numpy as np
from factories import DiffusionModelFactory
from greek_estimator_helpers import get_greek_estimator_se

GREEK_VARIABLE_MAPPING = {
    'Delta': 'S0',
    'Gamma': 'S0',
    'Theta': 'T',
    'Vega': 'vol',
    'Rho': 'r'
}

class GreekEstimator(ABC):
    def __init__(self, args, diffusion_model, option, pricer, z_table):
        self.diffusion_model = diffusion_model
        self.option = option
        self.pricer = pricer
        self.z_table = z_table

        self.greek_type = args['greekType']
        self.variable = GREEK_VARIABLE_MAPPING[args['greekType']]

    @abstractmethod
    def calculate(self, calculated_price):
        pass


class ResimulationEstimator(GreekEstimator):

    def __init__(self, args, h=0.001):
        super().__init__(args)
        self.h = h

    def calculate(self, calculated_price):
        args_up = self.args.copy()
        args_up[self.variable] = str(int(args_up[self.variable]) + self.h)
        args_down = self.args.copy()
        args_down[self.variable] = str(int(args_up[self.variable]) - self.h)

        diffusion_model_up = DiffusionModelFactory.create(args_up)
        diffusion_model_down = DiffusionModelFactory.create(args_down)

        price_up, price_se_up = self.pricer.price(diffusion_model_up, self.option, z_table=self.z_table)
        price_down, price_se_down = self.pricer.price(diffusion_model_down, self.option, z_table=self.z_table)

        if self.greek_type == 'Gamma':
            greek_calculation = (price_up - 2*calculated_price + price_down) / (self.h**2)
        else:
            greek_calculation = (price_up - price_down) / (2*self.h)

        return greek_calculation


class PathwiseDifferentiationEstimator(GreekEstimator):

    def __init__(self, args):
        super().__init__(args)
        self.num_paths = int(self.args['numPaths'])
        self.num_time_steps = int(self.args['numSteps'])
        self.S0 = int(self.args['S0'])
        self.T = int(self.args['T'])
        self.vol = int(self.args['vol'])
        self.r = int(self.args['r'])
        self.option_type = int(self.args['optionType'])

    def calculate(self, calculated_price):
        price_paths, _ = self.diffusion_model.simulate_paths(num_paths=self.num_paths, num_time_steps=self.num_time_steps, z_table=self.z_table)
        greek_estimator, greek_se = get_greek_estimator_se(price_paths, self.args, self.z_table, calculated_price)
        return greek_estimator, greek_se

class LikelihoodMethodEstimator(GreekEstimator):

    def calculate(self, calculated_price):
        pass







