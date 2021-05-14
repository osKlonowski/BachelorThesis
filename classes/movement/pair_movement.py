class PairsMovement:
    # { NS-pair, EW-pair, board group }
    def __init__(self, pair, board_group):
        self.pair = pair
        self.pairIds = [pair.split('-')[0], pair.split('-')[1]]
        self.ns_pair = pair.split('-')[0]
        self.ew_pair = pair.split('-')[1]
        self.board_group = board_group
