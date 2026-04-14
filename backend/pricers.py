from abc import ABC, abstractmethod
import numpy as np

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

    def price_classic_mc(self, diffusion_model, option):
        paths = diffusion_model.simulate_paths(num_paths=self.num_paths, num_time_steps=self.num_time_steps)
        discounted_payoffs = option.discounted_payoff(paths[0])
        discounted_payoff_mean = np.mean(discounted_payoffs)
        discounted_payoff_se = np.std(discounted_payoffs) / np.sqrt(len(discounted_payoffs))

        return discounted_payoff_mean, discounted_payoff_se

    def price_classic_antithetic(self, diffusion_model, option):
        pass

    def price_classic_control(self, diffusion_model, option):
        pass

    def price(self, diffusion_model, option):
        if self.variance_reduction_type == 'None':
            return self.price_classic_mc(diffusion_model, option)
        elif self.variance_reduction_type == 'Antithetic Variables':
            pass
        elif self.variance_reduction_type == 'Control Variables':
            pass

class PDEPricer(Pricer):
    def price(self, option, model):
        pass