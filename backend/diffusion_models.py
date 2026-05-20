from abc import ABC, abstractmethod
import numpy as np

class StochasticProcess(ABC):
    @abstractmethod
    def simulate_paths(self, num_paths=100, num_time_steps=10, z_table=None, z2_table=None):
        pass

class GBMProcess(StochasticProcess):
    def __init__(self, args):
        self.S0 = float(args['S0'])
        self.T = float(args['T'])
        self.r = float(args['r'])
        self.vol = float(args['vol'])

    def simulate_paths(self, num_paths=100, num_time_steps=10, z_table=None, z2_table=None):
        ''' Simulates a given number of paths under GBM over a given number of time steps

        Args:
            - S0 (float): The current/initial stock price we will grow our paths from
            - maturity (float): The maturity date (in years from today) the price path will end
            - num_paths (int): The number of paths we will simulate
            - num_time_steps (int): The number of time steps we will take

        Return:
            - 1-Tuple of 2D np.arrays:
                - stock_table (2D np.array): The simulated price paths
                    - Shape is (num_paths, num_time_steps + 1)
                    - Each row represents a different simulated price path
                    - Each column represents the stock prices for each path at each time step
                        - We have an extra column at the beginning for the time 0 stock value (S0)
        '''

        #Calculating how many years each time step takes
        delta_t = self.T / num_time_steps

        if z_table is None:
            z_table = np.random.normal(0, 1, (num_paths, num_time_steps + 1))


        #Initializing the path table with S0 in the first column (we'll fill in the rest next)
        stock_table = np.zeros((num_paths, num_time_steps + 1))
        stock_table[:, 0] = self.S0

        #At each time step, we update the price based on the GBM Process
        for t_step in range(1, num_time_steps + 1):

            term_1 = (self.r - 0.5 * self.vol ** 2) * delta_t
            term_2 = self.vol * np.sqrt(delta_t) * z_table[:, t_step - 1]

            #GBM update rule across each price path
            stock_table[:, t_step] = stock_table[:, t_step - 1] * np.exp(term_1 + term_2)

        #Now we have our full stock paths
        #Note: The terminal stock values are in the last column
        #We need to return a tuple since other processes return a tuple as well
        return stock_table, None

class HestonProcess(StochasticProcess):
    def __init__(self, args):
        self.S0 = float(args['S0'])
        self.T = float(args['T'])
        self.r = float(args['r'])
        self.V0 = float(args['V0'])
        self.kappa = float(args['kappa'])
        self.theta = float(args['theta'])
        self.volvol = float(args['volvol'])
        self.corr = float(args['corr'])

    def simulate_paths(self, num_paths=100, num_time_steps=10, z_table=None, z2_table=None):
        ''' Simulates a given number of paths under Heston over a given number of time steps
            for both the stock value and the volatility value

        Args:
            - S0 (float): The current/initial stock price we will grow our paths from
            - V0 (float): The current/initial volatility we will grow our paths from
            - maturity (float): The maturity date (in years from today) the price path will end
            - num_paths (int): The number of paths we will simulate
            - num_time_steps (int): The number of time steps we will take

        Return:
            - 2-Tuple of 2D np.arrays:
                - stock_table (2D np.array): The simulated stock value paths
                    - Shape is (num_paths, num_time_steps + 1)
                    - Each row represents a different simulated stock path
                    - Each column represents the stock values for each path at each time step
                        - We have an extra column at the beginning for the time 0 stock value (S0)
                - stochastic_volatility_table (2D np.array): The simulated volatility paths
                    - Shape is (num_paths, num_time_steps + 1)
                    - Each row represents a different simulated stock path
                    - Each column represents the volatility values for each path at each time step
                        - We have an extra column at the beginning for the time 0 volatility value (V0)

        '''

        #Calculating how many years each time step takes
        delta_t = self.T / num_time_steps

        #Correlate these sources of randomness
        # according to the Heston model's given correlation value
        w1_table = np.sqrt(delta_t) * z_table
        w2_table = np.sqrt(delta_t) * (self.corr * z_table + np.sqrt(1 - self.corr ** 2) * z2_table)

        #Initialize stochastic volatility path table
        stochastic_volatility_table = np.zeros((num_paths, num_time_steps + 1))
        stochastic_volatility_table[:, 0] = self.V0

        #Initialize stock path table
        stock_table = np.zeros((num_paths, num_time_steps + 1))
        stock_table[:, 0] = self.S0

        for t_step in range(1, num_time_steps + 1):
            # For each volatility path, update the volatility under Heston
            term_1 = stochastic_volatility_table[:, t_step - 1]
            term_2 = self.kappa * (self.theta - stochastic_volatility_table[:, t_step - 1]) * delta_t
            term_3 = self.volvol * w2_table[:, t_step - 1] * np.sqrt(np.maximum(0, stochastic_volatility_table[:, t_step - 1]))
            stochastic_volatility_table[:, t_step] = np.maximum(0, term_1 + term_2 + term_3)

            # For each stock path, update the stock under Heston
            # (using previous volatility, not the one we just computed in this iteration
            term_1 = delta_t * (self.r - 0.5 * np.maximum(0, stochastic_volatility_table[:, t_step]))
            term_2 = w1_table[:, t_step - 1] * np.sqrt(np.maximum(0, stochastic_volatility_table[:, t_step - 1]))
            stock_table[:, t_step] = stock_table[:, t_step - 1] * np.exp(term_1 + term_2)

        #Now we have our full stock and volatility paths
        #Note: The terminal stock and volatility values are in the last column
        return stock_table, stochastic_volatility_table

class JumpDiffusionProcess(StochasticProcess):
    def __init__(self, args):
        self.S0 = float(args['S0'])
        self.T = float(args['T'])
        self.r = float(args['r'])
        self.vol = float(args['vol'])
        self.lmbda = float(args['lmbda'])
        self.jump_mean = float(args['jumpMean'])
        self.jump_vol = float(args['jumpVol'])

        self.k = np.exp(
            self.jump_mean + 0.5 * self.jump_vol**2
        ) - 1

    def simulate_paths(self, num_paths=100, num_time_steps=10, z_table=None, z2_table=None):

        delta_t = self.T / num_time_steps

        if z_table is None:
            z_table = np.random.normal(0, 1, (num_paths, num_time_steps + 1))

        # Poisson jump counts
        jump_table = np.random.poisson(
            self.lmbda * delta_t,
            (num_paths, num_time_steps)
        )

        stock_table = np.zeros((num_paths, num_time_steps + 1))
        stock_table[:, 0] = self.S0

        for t_step in range(1, num_time_steps + 1):

            term_1 = (self.r - self.lmbda * self.k - 0.5 * self.vol ** 2) * delta_t
            term_2 = self.vol * np.sqrt(delta_t) * z_table[:, t_step - 1]

            diffusion_term = np.exp(term_1 + term_2)

            # Number of jumps for each path
            n_jumps = jump_table[:, t_step - 1]

            # Total jump log-size
            jump_sums = np.random.normal(
                loc=n_jumps * self.jump_mean,
                scale=np.sqrt(n_jumps) * self.jump_vol
            )

            jump_term = np.exp(jump_sums)

            stock_table[:, t_step] = stock_table[:, t_step - 1] * diffusion_term * jump_term

        return stock_table, None