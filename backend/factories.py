from diffusion_models import *
from options import *
from pricers import *
from greek_estimators import *
from estimators_factory import GreekFactory


class DiffusionModelFactory:
    @staticmethod
    def create(data):
        ''' Given the inputs from the user, creates our diffusion model, option, and pricer

        Args:
            - data (dict/json): The input data from the user

        Returns:
            - diffusion_model_process (StochasticProcess): The parametrized diffusion model wanted by the user'''
        diffusion_model_type = data['diffusionModelType']

        if diffusion_model_type == 'GBM':
            return GBMProcess(data)
        elif diffusion_model_type == 'Heston':
            return HestonProcess(data)
        elif diffusion_model_type == 'Jump Diffusion':
            return JumpDiffusionProcess(data)
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

        if option_type == 'Vanilla':
            return EuropeanOption(data)
        elif option_type == 'Arithmetic Asian':
            return ArithmeticAsianOption(data)
        elif option_type == 'Geometric Asian':
            return GeometricAsianOption(data)
        elif option_type == 'Barrier':
            return BarrierOption(data)
        elif option_type == 'Digital':
            return DigitalOption(data)
        # elif option_type == 'Digital':
        #     return EuropeanOption(**option_args)
        # elif option_type == 'Lookback':
        #     return EuropeanOption(**option_args)
        elif option_type == 'AutoCallable':
            return AutoCallableOption(data)
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

        if pricer_type == 'Analytical':
            return AnalyticalPricer(data)
        elif pricer_type == 'Monte Carlo':
            return MonteCarloPricer(data)
        elif pricer_type == 'PDE':
            return PDEPricer(data)
        else:
            raise ValueError(f"Unknown Pricer Type: {pricer_type}")