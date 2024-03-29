import pandas as pd


class SolutionResult:
    def __init__(self, fitness, time_taken, assignments, num_iter, num_ants, alpha, beta, Q, rho, tau0, q0, phi):
        self.fitness = fitness
        self.time_taken = time_taken
        self.assignments = assignments
        self.num_iter = num_iter
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        self.rho = rho
        self.tau0 = tau0
        self.q0 = q0
        self.phi = phi

    def show(self):
        print('\n')
        print(f'Best Fitness Achieved: {self.fitness}')
        print(f'This Section Took: {self.time_taken}')
        print(f'Final Solution: {self.assignments}')

    def get_csv_res(self):
        #['fitness', 'time', 'num_iter', 'num_ants', 'alpha', 'beta', 'Q']
        return [self.fitness, self.time_taken, self.num_iter, self.num_ants, self.alpha, self.beta, self.Q]

    def basic_params(self):
        return [self.num_iter, self.num_ants, self.alpha, self.beta, self.Q, self.rho, self.tau0, self.q0, self.phi]
