from abc import ABC, abstractmethod
import numpy as np
from control_variable_helpers import get_known_expectation, get_control_discounted_payoff

class Pricer(ABC):
    @abstractmethod
    def price(self, option, model):
        pass

class AnalyticalPricer(Pricer):
    def price(self, option, model):
        pass

class MonteCarloPricer(Pricer):
    def __init__(self, args):
        self.variance_reduction_type = str(args['varianceReductionType'])
        self.num_paths = int(args['numPaths'])
        self.num_time_steps = int(args['numSteps'])
        self.args = args

    def price_classic_mc(self, diffusion_model, option, z_table=None):
        paths = diffusion_model.simulate_paths(num_paths=self.num_paths, num_time_steps=self.num_time_steps, z_table=z_table)
        discounted_payoffs = option.discounted_payoff(paths[0])
        discounted_payoff_mean = np.mean(discounted_payoffs)
        discounted_payoff_se = np.std(discounted_payoffs) / np.sqrt(len(discounted_payoffs))

        return discounted_payoff_mean, discounted_payoff_se

    def price_classic_antithetic(self, diffusion_model, option, z_table=None):
        paths = diffusion_model.simulate_paths(num_paths=self.num_paths, num_time_steps=self.num_time_steps, z_table=z_table)
        discounted_payoffs = option.discounted_payoff(paths[0])
        discounted_payoff_mean = np.mean(discounted_payoffs)
        discounted_payoff_se = np.std(discounted_payoffs) / np.sqrt(len(discounted_payoffs))

        return discounted_payoff_mean, discounted_payoff_se

    def price_classic_control(self, diffusion_model, option, z_table=None, control_variable='S(T)'):
        paths = diffusion_model.simulate_paths(num_paths=self.num_paths, num_time_steps=self.num_time_steps, z_table=z_table)
        known_expectation = get_known_expectation(self.args, control_variable)
        main_discounted_payoffs = option.discounted_payoff(paths[0])
        control_discounted_payoffs = get_control_discounted_payoff(paths[0], control_variable=control_variable)

        cov_xy = np.cov(main_discounted_payoffs, control_discounted_payoffs, ddof=1)[0, 1]
        var_y = np.var(control_discounted_payoffs, ddof=1)
        optimal_b = cov_xy / var_y

        estimator = main_discounted_payoffs - optimal_b * (control_discounted_payoffs - known_expectation)
        estimator_mean = np.mean(estimator)
        estimator_se = np.std(estimator) / np.sqrt(len(estimator))

        return estimator_mean, estimator_se

    def price(self, diffusion_model, option, z_table=None):
        if self.variance_reduction_type in ['None', 'Antithetic', 'Stratified Sampling']:
            return self.price_classic_mc(diffusion_model, option, z_table=z_table)
        elif self.variance_reduction_type == 'Control':
            return self.price_classic_control(diffusion_model, option, z_table=z_table, control_variable=self.args['controlVariable'])

class PDEPricer(Pricer):
    def price(self, option, model):
        pass