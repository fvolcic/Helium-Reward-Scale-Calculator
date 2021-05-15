"""File containing important chain varibles."""

# max needed resolution
RES_MAX = 11
RES_MIN = 3

# Format = [ <N = Number of siblings>, <density_tgt>, <density_max> ]
HIP17_RES_0 = [2, 100000, 100000]
HIP17_RES_1 = [2, 100000, 100000]
HIP17_RES_2 = [2, 100000, 100000]
HIP17_RES_3 = [2, 100000, 100000]
HIP17_RES_4 = [1, 250, 800]
HIP17_RES_5 = [1, 100, 400]
HIP17_RES_6 = [1, 25, 100]
HIP17_RES_7 = [2, 5, 20]
HIP17_RES_8 = [2, 1, 4]
HIP17_RES_9 = [2, 1, 2]
HIP17_RES_10 = [2, 1, 1]
HIP17_RES_11 = [2, 100000, 100000]
HIP17_RES_12 = [2, 100000, 100000]

# a dictionary that contains metadata about a given resoution
# Written in this manner to make access to the data easier for
# different algorithms
HIP_RES_META = [
    HIP17_RES_0,
    HIP17_RES_1,
    HIP17_RES_2,
    HIP17_RES_3,
    HIP17_RES_4,
    HIP17_RES_5,
    HIP17_RES_6,
    HIP17_RES_7,
    HIP17_RES_8,
    HIP17_RES_9,
    HIP17_RES_10,
    HIP17_RES_11,
    HIP17_RES_12
]

# Number of blocks since last_poc_challenge a Hotspot is considered active.
HIP_17_INTERACTIVITY_BLOCKS = 3600