# estimators_factory.py
from greek_estimators import ResimulationEstimator, PathwiseDifferentiationEstimator

class GreekFactory:
    @staticmethod
    def create(data, diffusion_model, option, pricer, z_table, z2_table):
        greek_estimator_type = data['greekEstimatorType']
        if greek_estimator_type == 'Resimulation':
            return ResimulationEstimator(data, diffusion_model, option, pricer, z_table, z2_table)
        elif greek_estimator_type == 'Pathwise Differentiation':
            return PathwiseDifferentiationEstimator(data, diffusion_model, option, pricer, z_table, z2_table)
        else:
            raise ValueError(f"Unknown Greek Estimator Type: {greek_estimator_type}")
