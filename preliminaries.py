# Preliminaries:
# For a pair of history and registration files, distribute the registered pairs over the given number of sections, based on their ranking values. For details, see below.
# For each section, compute a matrix of previous meetings among the pairs.
# Meetings are counted per player. So for pairs (A,B) and (C,D), we add up the number of meetings among A-C, A-D, B-C, and B-D to compute the total number of previous meetings among them.
# For each section, record the number of previous waiting tables of each pair, also adding up the waiting tables of both players. This will be a vector of values.

# 1. Distribute (registered) pairs over sections based on combined ranking value.
#       Result: #sections with a list of pairs (evenly distributed)
#   For Each Section:
#       Compute a Matrix of Previous Meetings (Among the Pairs):
#           Meetings are counted per player.
#               Ex. For Pairs (A, B) and (C, D), we add up the number of meetings among A-C, A-D, B-C, B-D
#               Result: Compute total number of previous meetings amongst pair members.
#   For Each Section:
#       Record number of previous waiting tables of each pair (sum of both players). -> (Vector of values for each pair)

# GOAL:
# Matrix of Meetings
# Vector of Waiting Tables

# 1. Compute ranking of a pair.
#       Will need a way to query player rankings from big register.
# 2. Construct a 'Section's with a list of pairs and their ranking
# 3. ......
