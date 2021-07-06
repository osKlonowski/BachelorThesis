from classes.section import Section
from classes.list_of_sections import ListOfSections
import numpy as np


def partition(listPairs, divisions):
    indices = []
    prev_index_split = 0
    for div in divisions:
        prev_index_split += div
        indices.append(prev_index_split)
    print(f'Split List of Pairs by Indices: {indices}')
    sections = [listPairs[i:j]
                for i, j in zip([0]+indices, indices)]
    print(f'Num of Section from Partition: {len(sections)}')
    for sec in sections:
        print(f'Partition Section Len: {len(sec)}')
    return sections


def getTotalWaitingTablesForSection(listPairs):
    totalWaiting = 0
    for pair in listPairs:
        totalWaiting += pair.total_waiting
    return totalWaiting


def getIndexSectionWithLeastWaitingTables(sections):
    listWaiting = []
    for section in sections:
        totalWaiting = getTotalWaitingTablesForSection(section)
        listWaiting.append(totalWaiting)
    return listWaiting.index(min(listWaiting))


def getSize(element):
    return len(element)


def getSectionSizeDiff(divisions):
    listSizes = list(map(getSize, divisions))
    max_diff = 0
    for i in range(0, len(listSizes)):
        for j in range(0, len(listSizes)):
            # i => 0
            # j => 0, 1, 2
            diff = listSizes[i] - listSizes[j]
            if diff > max_diff:
                max_diff = diff
    return max_diff


def reallocate(divisions):
    print('REALLOCATE')
    listSizes = list(map(getSize, divisions))
    indexMaxDivision = listSizes.index(max(listSizes))
    indexMinDivision = listSizes.index(min(listSizes))
    one_element = divisions[indexMaxDivision].pop()
    second_element = divisions[indexMaxDivision].pop()
    divisions[indexMinDivision].append(one_element)
    divisions[indexMinDivision].append(second_element)
    for section in divisions:
        print(len(section))
    return divisions


def organizeOddPairs(listPairs, numSections):
    listOfPairs = listPairs.copy()
    lastPair = listOfPairs.pop()
    print(f'Odd Pairs -> Popped Pair: {lastPair}')
    divisible = len(listOfPairs) % numSections == 0
    if divisible:
        divisions = organizeEvenDivisibleDivision(listOfPairs, numSections)
        index_least_waiting_tables = getIndexSectionWithLeastWaitingTables(
            divisions)
        divisions[index_least_waiting_tables].append(lastPair)
        return divisions
    else:
        divisions = organizeEvenIndivisible(listOfPairs, numSections)
        index_least_waiting_tables = getIndexSectionWithLeastWaitingTables(
            divisions)
        divisions[index_least_waiting_tables].append(lastPair)
        largestSizeDiff = getSectionSizeDiff(divisions)
        # 1. Check max diff, if diff >= 3 then redistribute (e.g. [18, 16, 15]=> max diff of 3)
        if(largestSizeDiff >= 3):
            # 2. Reallocate max - 2, min + 2 (e.g. [16, 16, 17]=> max diff of 1)
            # 3. Redistribute players into newly allocated divisions
            print('There is a size diff larger or equal to 3 --> REDISTRIBUTE')
            divisions = reallocate(divisions)
        # TODO:  *2. Alternatively, you can "push" the player pairs
        # TODO:  E.g. push two lowest ranked pair of A into B ([18, 16, 15]=> [16, 18, 15]
        # TODO:  push two lowest ranked pair of B into C ([16, 18, 15]=> [16, 16, 17])
        return divisions


def organizeEvenIndivisible(listPairs, numSections):
    print(f'Even and In-divisible Received: {len(listPairs)} pairs')
    numPlayersPerSection = len(listPairs) / numSections
    numPlayersPerSection = round(numPlayersPerSection)
    while numPlayersPerSection % 2 != 0:
        numPlayersPerSection -= 1
    divisions = []
    for i in range(0, numSections):
        divisions.append(numPlayersPerSection)
    currentIndex = 0
    while sum(divisions) < len(listPairs):
        print('Len of Divisions < len of Pairs -> Adding two to sections starting from A')
        divisions[currentIndex] = divisions[currentIndex] + 2
        currentIndex += 1
    print(f'Even In-Divisible -- Divisions: {divisions}')
    return partition(listPairs, divisions)


def organizeEvenDivisibleDivision(listPairs, numSections):
    sections = np.array_split(listPairs, numSections)
    print('Successfully Divided Pairs into Sections:')
    return sections


def splitIntoSections(listPairs, numSections):
    listSections = ListOfSections()
    if numSections < 1:
        return
    if len(listPairs) / numSections < 8:
        return
    isEven = len(listPairs) % 2 == 0
    isDivisible = len(listPairs) % numSections == 0
    divisions = []
    if isEven and isDivisible:
        print('-- Even and Divisible Num of Pairs --')
        divisions = organizeEvenDivisibleDivision(listPairs, numSections)
    elif isEven:
        print('-- Even and In-Divisible Num of Pairs --')
        divisions = organizeEvenIndivisible(listPairs, numSections)
    else:
        print('-- Odd Num of Pairs --')
        divisions = organizeOddPairs(listPairs, numSections)
    print('Final Partition')
    for section in divisions:
        print(f'Pairs in Section: {len(section)}')
        listSections.addSection(Section(section))
    return listSections
