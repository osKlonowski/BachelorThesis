class MovementHeader:
    # pairs or players, number of tables, number of rounds, number of board groups, Individual
    def __init__(self, n_of_pairs, n_of_tables, n_of_rounds, n_of_board_groups, individual):
        self.n_of_pairs = n_of_pairs
        self.n_of_tables = n_of_tables
        self.n_of_rounds = n_of_rounds
        self.n_of_board_groups = n_of_board_groups
        self.individual = individual
