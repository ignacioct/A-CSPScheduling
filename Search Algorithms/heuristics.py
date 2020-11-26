#                     *****     Minimum Pick-up Heuristic Function     *****

# using Floyd-Warshall algorithm implemented on state, we compute the minimum distance to go in between all nodes
# then, this function will evaluate each node with the sum of the mimimun distance from current position to each pickup and from currrent position to the initial position
def MP(c_state):

    # suma = minimum distance from current position to initial position
    suma = c_state.floyd[int(c_state.current_pos[-1]) - 1][
        int(c_state.init_position[-1]) - 1
    ]

    for (
        j
    ) in (
        c_state.pending_children
    ):  # sum minimum distance from current position to every stop where there is at least a child
        suma += c_state.floyd[int(j[-1]) - 1][int(c_state.current_pos[-1]) - 1]

    return suma


#                       *****     Minimum Cost to Access Children     *****

# using Floyd-Warshall algorithm we compute firs minimum cost from current to initial position.
# then we compute a ratio between number of children of one stop/maximum capacity of our bus,
# we truncate this ratio and add 1 to it getting with this number of times that we need to get to the node to get every children
# finally we muliply this ratio by the smallest cost of that stop edges.
def MCAC(c_state):
    # suma = minimum distance from current position to initial position
    suma = c_state.floyd[int(c_state.current_pos[-1]) - 1][
        int(c_state.init_position[-1]) - 1
    ]
    for i in c_state.pending_children:  # ratio * minimum cost edge(explained above)
        suma += (
            int(len(c_state.pending_children[i]) / c_state.max_capacity) + 1
        ) * sorted(c_state.floyd[int(c_state.current_pos[-1]) - 1])[1]

    return suma
