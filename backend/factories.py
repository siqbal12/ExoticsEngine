from backend.diffusion_models import *
from backend.options import *
from backend.pricers import *

class DiffusionModelFactory:
    @staticmethod
    def create(data):
        ''' Given the inputs from the user, creates our diffusion model, option, and pricer

        Args:
            - data (dict/json): The input data from the user

        Returns:
            - diffusion_model_process (StochasticProcess): The parametrized diffusion model wanted by the user'''
        diffusion_model_type = data['diffusionModelType']
        diffusion_model_args = data['diffusionModelArgs']

        if diffusion_model_type == 'GBM':
            return GBMProcess(diffusion_model_args)
        elif diffusion_model_type == 'Heston':
            return HestonProcess(diffusion_model_args)
        elif diffusion_model_type == 'Jump Diffusion':
            return JumpDiffusionProcess(diffusion_model_args)
        else:
            raise ValueError(f"Unknown Diffusion Model Type: {diffusion_model_type}")

class OptionFactory:
    @staticmethod
    def create(data):
        ''' Given the inputs from the user, creates our diffusion model, option, and pricer

        Args:
            - data (dict/json): The input data from the user

        Returns:
            - option (Option): The parametrized option wanted by the user'''
        option_type = data['optionType']
        option_args = data['optionArgs']

        if option_type == 'European':
            return EuropeanOption(option_args)
        elif option_type == 'Asian':
            return ArithmeticAsianOption(option_args)
        elif option_type == 'Barrier':
            return BarrierOption(option_args)
        # elif option_type == 'Digital':
        #     return EuropeanOption(**option_args)
        # elif option_type == 'Lookback':
        #     return EuropeanOption(**option_args)
        elif option_type == 'AutoCallable':
            return AutoCallableOption(option_args)
        else:
            raise ValueError(f"Option type unknown: {option_type}")

class PricerFactory:
    @staticmethod
    def create(data):
        ''' Given the inputs from the user, creates our diffusion model, option, and pricer

        Args:
            - data (dict/json): The input data from the user

        Returns:
            - pricer (Pricer): The parametrized pricer wanted by the user'''
        pricer_type = data['pricerType']
        pricer_args = data['pricerArgs']

        if pricer_type == 'Analytical':
            return AnalyticalPricer(pricer_args)
        elif pricer_type == 'Monte Carlo':
            return MonteCarloPricer(pricer_args)
        elif pricer_type == 'PDE':
            return PDEPricer(pricer_args)
        else:
            raise ValueError(f"Unknown Pricer Type: {pricer_type}")