from factories import *
from scipy.stats import norm

class PricingEngine:
    def __init__(self, data):
        ''' Given the inputs from the user, creates our diffusion model, option, and pricer

        Args:
            - data (dict/json): The input data from the user'''

        self.diffusion_model = DiffusionModelFactory.create(data)
        self.option = OptionFactory.create(data)
        self.pricer = PricerFactory.create(data)

        num_paths = int(data['numPaths'])
        num_time_steps = int(data['numSteps'])

        if data['varianceReductionType'] == 'Antithetic':
            #Generate half of the zs, then add the negative of those to the bottom
            z_table = np.random.normal(0, 1, (num_paths // 2, num_time_steps + 1))
            self.z_table = np.concatenate((z_table, -z_table), axis=0)
            z2_table = np.random.normal(0, 1, (num_paths // 2, num_time_steps + 1))
            self.z2_table = np.concatenate((z2_table, -z2_table), axis=0)
        elif data['varianceReductionType'] == 'Stratified Sampling':

            self.z_table = np.random.normal(0, 1, (num_paths, num_time_steps + 1))
            self.z2_table = np.random.normal(0, 1, (num_paths, num_time_steps + 1))

            def stratified_normal(N):
                u = (np.arange(N) + np.random.rand(N)) / N
                np.random.shuffle(u)  # important
                z = norm.ppf(u)
                return z

            for j in range(3):  # first few dimensions
                self.z_table[:, j] = stratified_normal(num_paths)
                self.z2_table[:, j] = stratified_normal(num_paths)
        else:
            self.z_table = np.random.normal(0, 1, (num_paths, num_time_steps + 1))
            self.z2_table = np.random.normal(0, 1, (num_paths, num_time_steps + 1))

        self.greek_estimator = GreekFactory.create(data, self.diffusion_model, self.option, self.pricer, self.z_table, self.z2_table)

    def price(self):
        ''' Pries the option by simulating paths with the diffusion model,
            then calculating the average discounted payoff with the option

        Return:
            - price (float): The estimated price of the option'''
        price, price_se = self.pricer.price(self.diffusion_model, self.option, z_table=self.z_table, z2_table=self.z2_table)
        greek, greek_se = self.greek_estimator.calculate(calculated_price=price, calculated_price_se=price_se)
        return price, price_se, greek, greek_se
