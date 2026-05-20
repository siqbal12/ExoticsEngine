from abc import ABC, abstractmethod
import numpy as np

rf = 0.03

class Option(ABC):
    def __init__(self, args):
        self.K = float(args['K'])
        self.T = float(args['T'])
        #Note: Payoff is 'Call' or 'Put'
        self.payoff_type = str(args['payoffType'])

    @abstractmethod
    def discounted_payoff(self, stock_paths):
        pass

    def discounted_payoff_helper(self, terminal_value):
        if self.payoff_type == 'Call':
            return np.exp(-rf * self.T) * np.maximum(terminal_value - self.K, 0)
        else:
            return np.exp(-rf * self.T) * np.maximum(self.K - terminal_value, 0)

class EuropeanOption(Option):

    def discounted_payoff(self, stock_paths):
        terminal_stock_values = stock_paths[:, -1]
        return self.discounted_payoff_helper(terminal_stock_values)

class DigitalOption(Option):

    def discounted_payoff(self, stock_paths):
        terminal_stock_values = stock_paths[:, -1]
        if self.payoff_type == 'Call':
            return np.exp(-rf * self.T) * np.where(terminal_stock_values > self.K, 1, 0)
        else:
            return np.exp(-rf * self.T) * np.where(terminal_stock_values < self.K, 1, 0)

class ArithmeticAsianOption(Option):

    def discounted_payoff(self, stock_paths):
        average_stock_values = np.mean(stock_paths, axis=1)
        return self.discounted_payoff_helper(average_stock_values)

class GeometricAsianOption(Option):

    def discounted_payoff(self, stock_paths):
        # product across time steps then nth-root where n = #columns (time steps)
        geometric_average_stock_values = np.exp(np.mean(np.log(stock_paths), axis=1))
        return self.discounted_payoff_helper(geometric_average_stock_values)

class BarrierOption(Option):
    def __init__(self, args):
        super().__init__(args)
        self.barrier_level = float(args['barrierLevel'])
        #Note: Barrier Activation Type is 'In' or 'Out'
        self.barrier_activation_type = str(args['barrierActivationType'])
        #Note: Barrier Direction Type is 'Up' or 'Down'
        self.barrier_direction_type = str(args['barrierDirectionType'])

    def discounted_payoff(self, stock_paths):
        #Identify which paths had the stock price hit the barrier!
        if self.barrier_direction_type == 'Up':
            barrier_mask = stock_paths >= self.barrier_level
        else:
            barrier_mask = stock_paths <= self.barrier_level
        barrier_hit = barrier_mask.any(axis=1)

        #Get the payoffs of each stock path (before considering barrier condition)
        terminal_stock_values = stock_paths[:, -1]
        payoffs = self.discounted_payoff_helper(terminal_stock_values)

        #Force any paths that hit barrier to be 0, keep the rest
        if self.barrier_activation_type == 'In':
            return payoffs * barrier_hit
        else:
            return payoffs * (~barrier_hit)

#Note: Autocallable Option is not a subclass of Option since it is so different than a classic option
class AutoCallableOption:
    def __init__(self, args):
        self.S0 = float(args['S0'])
        self.T = float(args['T'])
        self.autocall_level = float(args['autocallLevel'])
        self.coupon_barrier_level = float(args['couponBarrierLevel'])
        self.knock_in_barrier_level = float(args['knockInBarrierLevel'])
        self.notional = float(args['notional'])
        self.coupon_amount = float(args['couponAmount'])

    def discounted_payoff(self, stock_paths):

        times = np.linspace(0, self.T, stock_paths.shape[1])

        path_payoffs = []

        #Iteratively go through each of the paths, identifying their discounted payoff values
        for path_idx in range(0, stock_paths.shape[0]):
            path = stock_paths[path_idx, :]
            payoff = 0
            knock_in_barrier_breached = False
            #Go through each of the time steps, identifying the discounted payoff at each step
            for t_idx in range(1, stock_paths.shape[1]):
                current_price = path[t_idx]
                time = times[t_idx]

                # We need to check if we have breached the knock in barrier
                if current_price < self.knock_in_barrier_level:
                    knock_in_barrier_breached = True

                #To identify payoffs, we first need to identify if we are at maturity or not

                #We are not at maturity yet
                if t_idx < stock_paths.shape[1] - 1:
                    # Case 1) We are autocalled and must STOP
                    if current_price >= self.autocall_level:
                        payoff += np.exp(-rf * time) * (self.notional + self.coupon_amount)
                        break
                    #Case 2) We are not autocalled, and we are still receiving coupons
                    elif current_price >= self.coupon_barrier_level:
                        payoff += np.exp(-rf * time) * self.coupon_amount
                    #Case 3) We are not autocalled, and we are not receiving coupons
                    # Note: we don't need to add 0, so there is no need to write code

                #We are at maturity
                else:
                    # Case 1) The barrier was not breached
                    if knock_in_barrier_breached:
                        payoff += np.exp(-rf * time) * (self.notional + self.coupon_amount)
                    # Case 2) The barrier was breached
                    else:
                        payoff += np.exp(-rf * time) * (self.notional * (current_price / self.S0))

            #Now we have the total payoff for this path
            path_payoffs.append(payoff)

        return np.array(path_payoffs)










