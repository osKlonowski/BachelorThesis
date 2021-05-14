from classes.movement.pair_movement import PairsMovement


class Round:
    def __init__(self):
        self.tables = []

    def addTable(self, table):
        self.tables.append(table)

    def getTablePairs(self):
        list = []
        for table in self.tables:
            list.append(table.pairIds)
        return list

    # def getListPairIds(self):
    #     list = []
    #     for table in self.tables:
    #         list.append(table.pair)
    #     return list
