import copy  # needed for being able to copy objects with dictionaries without just creating a new reference to them. (deepcopy())
from timeit import default_timer as timer
import sys
from heuristics import *


# ________________________________________     STATE     _______________________________________

#   State Class
#       defines a class for creating the state of the objects


class state:

    # static parammeters, from parser
    grid = {}
    max_capacity = None
    school_positions = {}
    init_position = ""
    floyd = []
    heuristic = 0  # Dijkstra by default

    # constructor
    def __init__(
        self,
        current_pos,
        current_capacity,
        pending_children,
        onboard_children,
        gScore,
        parentNode,
    ):
        self.current_pos = current_pos
        self.current_capacity = current_capacity
        self.pending_children = pending_children  # dictionary
        self.onboard_children = onboard_children  # Dic with the number of children that want to go to each school
        self.gScore = gScore  #
        self.parentNode = parentNode
        self.fScore = self.gScore + h(self, self.heuristic)

    # override of eq operator, in order to compare nodes just by current position, pending children and on board children
    # nodes which matches these info are equal for us
    def __eq__(self, state2):
        return (
            (self.current_pos == state2.current_pos)
            and (self.pending_children == state2.pending_children)
            and (self.onboard_children == state2.onboard_children)
        )

    # override of hash operator, in order to hash our states just considering current position, pending children and on board children
    # this will help us create our closed node list
    def __hash__(self):
        return hash(
            self.current_pos + str(self.onboard_children) + str(self.pending_children)
        )

    #   isGoal Function
    #       Returns true if the node is the goal, which appens if:
    #           there are no more children in any stop AND
    #           there are no more children inside the bus AND
    #           the bus is in the initial stop
    def isGoal(self):
        return (
            len(self.pending_children) == 0
            and self.current_capacity == 0
            and self.current_pos == self.init_position
        )


# ________________________________     FUNCTIONS DEFINITION     _________________________________


#                      *****     Parser Function     *****

# it reads the input file and transform its data into in-code data structures from which we build the grid and set the problem
def parser():

    # File opening and storing in data variable
    try:
        file = open("ejemplos/" + sys.argv[1], "r")
    except ValueError:
        print("Error in the first argument: {} not found".format(sys.argv[1]))

    data = file.readlines()  # after sorting and saving the info, data is deleted

    # Dictionary declaration
    # we are going to follow a dictionary structure, dividing the graph connections, the positions of the schools and the positions of the children

    GRAPH = {}
    SCHOOLS = {}
    CHILDREN = {}
    INITIALONBOARD = {}

    # declaration of the variable of the initial position
    INITPOS = ""
    CAPACITY = 0

    for i in range(len(data)):

        # Parser for the input grid
        if i >= 1 and i <= (len(data[1]) - 1):
            data[i] = (
                data[i]
                .replace("\n", "")
                .replace("   ", " ")
                .replace("  ", " ")
                .split(" ")
            )
            lista = []
            for j in range(1, len(data[i])):
                if data[i][j] != "--":
                    lista.append(("P" + str(j), int(data[i][j])))
            GRAPH[data[i][0]] = lista

        elif i > (len(data[1]) - 1):

            # Parser for the school line
            if data[i][0] == "C":
                data[i] = (
                    data[i]
                    .replace("\n", "")
                    .replace(":", "")
                    .replace(";", "")
                    .split(" ")
                )
                for j in range(0, len(data[i]), 2):
                    SCHOOLS[data[i][j]] = data[i][j + 1]

            # Parser for the position and the destination of the children
            elif data[i][0] == "P":
                stops = (
                    data[i]
                    .replace("\n", "")
                    .replace(":", "")
                    .replace(",", "")
                    .split("; ")
                )
                for j in range(len(stops)):
                    stops[j] = stops[j].split(" ")
                    lista = []
                    for k in range(1, len(stops[j]), 2):
                        lista.append((int(stops[j][k]), stops[j][k + 1]))
                    CHILDREN[stops[j][0]] = lista

            # Parser for the bus position and its capacity
            elif data[i][0] == "B":
                data[i] = data[i].replace("\n", "").replace("B: ", "").split(" ")
                INITPOS = data[i][0]
                CAPACITY = int(data[i][1])
            else:
                print('Error: Wrong "input.txt" file.')

    for i in SCHOOLS:
        INITIALONBOARD[i] = 0
    data = None  # data erasing

    return GRAPH, SCHOOLS, CHILDREN, INITIALONBOARD, INITPOS, CAPACITY


#                     *****     Heuristic Function     *****

# it computes the heuristic value of a node
def h(c_state, heuristic):

    # no heuristic, Dijkstra algorithm is applied
    if heuristic == 0:
        return 0

    if heuristic == 1:
        return MP(c_state)

    # else
    return MCAC(c_state)


#                         *****     Cost Function     *****

#       it sums heuristic score and g score, to give the f value from which we decide the nodes that A* will expand
def f(Node):
    return Node.gScore + h(Node, Node.heuristic)


#                      *****     Operators Function     *****

#       movement: always possible
#       pick children
#       drop children: it is automatic, so no node expansion is required.
def operators(current_state):
    # move will be always possible so we dont need to take it into account

    # Check if collecting children is possible
    return (
        current_state.current_capacity < current_state.max_capacity
        and current_state.current_pos in current_state.pending_children
    )


#                   *****     Neighbour expansion Function     *****

#       pick parammeter is a boolean that, if true, tells that in the current stop children can be picked up
#       this function will return the possible nodes that can be expanded
def neighbourNodes(current_state, pick):
    neighbours = []

    # move will always be possible so we can add it without reading the operators
    moves = current_state.grid[
        current_state.current_pos
    ]  # Gets from the static attribute "grid" of the class state every
    for i in moves:  # possible destination from our initial position

        obj = copy.deepcopy(
            current_state
        )  # we were forced to use deepcopy as when we tryed to do dictionary2 = dictionary1
        # python just makes a reference to that same dictionary so they are no independent
        # and when we modified one, every other node also made that change
        obj.current_pos = i[0]
        obj.gScore += i[1]
        obj.parentNode = current_state

        # This for-loop checks if in the new position is possible to drop any children, and if so, does it
        for j in current_state.school_positions:
            if obj.current_pos == current_state.school_positions[j]:
                if obj.onboard_children[j] >= 1:
                    obj.current_capacity = (
                        obj.current_capacity - obj.onboard_children[j]
                    )
                    obj.onboard_children[j] = 0

        neighbours.append(obj)

    if pick:  # if it's possible to pick children
        for i in current_state.pending_children[current_state.current_pos]:
            penChildren = current_state.pending_children[
                current_state.current_pos
            ].copy()  # List of every children in current stop
            newPending = (
                current_state.pending_children.copy()
            )  # new dictionary refreshing pending an onboard children when picking up or dropping.
            newOnBoard = current_state.onboard_children.copy()
            # more than 1 children that want to go to same school
            if i[0] > 1:
                penChildren.append((i[0] - 1, i[1]))
                newOnBoard[i[1]] = newOnBoard[i[1]] + 1
                penChildren.remove(i)
            # only 1 child want to go to that school
            elif i[0] == 1:
                newOnBoard[i[1]] = newOnBoard[i[1]] + 1
                penChildren.remove(i)

            if (
                len(penChildren) == 0
            ):  # if there are no more pending children in that stop erase the key from dictionary to save space
                newPending.pop(current_state.current_pos)
            else:
                newPending[current_state.current_pos] = penChildren
            # When we pick or drop a children we reached a mid-minigoal so we refresh each cost of node to search a new destination without interferences
            obj = copy.copy(current_state)
            obj.current_capacity += 1
            obj.pending_children = newPending
            obj.onboard_children = newOnBoard
            obj.parentNode = current_state
            neighbours.append(obj)

    return neighbours


#                        *****     Merge Sort Function     *****

#       Recursive method which divides input list in two halves, calls itself for the two halves and then merges the two sorted halves.
#       The merge function is used for merging two halves.
def mergeSort(lista):
    if len(lista) == 1:
        return lista
    else:
        result = []
        mid = int(len(lista) / 2)
        list1 = mergeSort(lista[:mid])
        list2 = mergeSort(lista[mid:])
        result = merge(list1, list2)
        return result


#                           *****     Merge Function     *****

#       Orders both sublists and returns a merged, ordered list
def merge(list1, list2):
    result = []
    while len(list1) != 0 and len(list2) != 0:
        state1 = list1[0]
        state2 = list2[0]
        if f(state1) < f(state2):
            result.append(state1)
            list1.remove(state1)

        elif f(state1) > f(state2):
            result.append(state2)
            list2.remove(state2)

        else:  # tie breaker, gmax is focused to priorise depth
            if state1.gScore > state2.gScore:
                result.append(state1)
                result.append(state2)

            else:
                result.append(state2)
                result.append(state1)

            list1.remove(state1)
            list2.remove(state2)

    # if one of both sublist is empty, the merged list will be just the other one
    if len(list1) == 0:
        result.extend(list2)
    else:
        result.extend(list1)

    return result


#                        *****     outputWrite Function     *****

#       Writes on output files the path and the statistics
def outputWrite(result, time, expansions):

    # we create here the output file to use the input name as file name for both, and we append the suffix
    prob = open("ejemplos/" + sys.argv[1] + ".output", "w+")
    stats = open("ejemplos/" + sys.argv[1] + ".statistics", "w+")

    result.reverse()
    output = "" + result[0].current_pos + " ---> "
    for i in range(1, len(result)):
        output += result[i].current_pos

        if result[i - 1].current_capacity < result[i].current_capacity:
            output += " (S: "
            for j in result[i].onboard_children:
                if (
                    result[i - 1].onboard_children[j] - result[i].onboard_children[j]
                    != 0
                ):
                    output += (
                        str(
                            abs(
                                result[i - 1].onboard_children[j]
                                - result[i].onboard_children[j]
                            )
                        )
                        + " "
                        + j
                        + ", "
                    )
            output = output[:-2]
            output += " )"

        elif result[i - 1].current_capacity > result[i].current_capacity:
            output += " (B: "
            for j in result[i].onboard_children:
                if (
                    result[i - 1].onboard_children[j] - result[i].onboard_children[j]
                    != 0
                ):
                    output += (
                        str(
                            abs(
                                result[i - 1].onboard_children[j]
                                - result[i].onboard_children[j]
                            )
                        )
                        + " "
                        + j
                        + ", "
                    )
            output = output[:-2]
            output += " )"
        output += " ---> "

    prob.write(output[:-5])

    stats.write("Overall time: {} s\n".format(time))
    stats.write(
        "Overall cost: {}\n".format(
            result[-1].gScore,
        )
    )
    stats.write("# Stops: {}\n".format(len(result)))
    stats.write("# Expansions: {}\n".format(expansions))

    # we close this files, as they will be reopened and used at the end of the program
    prob.close()
    stats.close()


#                      *****     Search algorithm function     *****

#    if a solution is found returns last node and number of nodes expanded
#    if no solution is found returns None and 0 nodes expanded
def Astar(start):

    openSet = [
        start
    ]  # OrderedList that will contain discovered nodes waiting for expansion

    closedSet = set([])  # Set containing every node we have already expanded.
    # in order to be able to store our nodes we had to define a new __hash__ & __eq__ function for our class "state"

    while len(openSet) != 0:  # While open set is not empty
        current = openSet.pop(
            0
        )  # Select first node (with less f() value) and remove it from open list
        if (
            not current in closedSet
        ):  # checks if it has been expanded yet and if it's the goal node
            if current.isGoal():

                result = []
                result.append(current)
                while not current.parentNode is None:

                    if result[-1].current_pos != current.current_pos:
                        result.append(current)
                    current = current.parentNode
                result.append(current)

                return result, len(
                    closedSet
                )  # returns last node and total nodes expanded

            neighbours = neighbourNodes(
                current, operators(current)
            )  # list with every node expanded from our one selected previously
            neighbours = mergeSort(neighbours)  # order this smaller list
            openSet = merge(
                openSet, neighbours
            )  # and merge this with the open list that is also sorted

            closedSet.add(current)  # add last node expanded to closedSet

    return None, len(closedSet)  # No solution has been found (open list got emptied)


# ________________________________      HEURISTICS        ______________________________


def floydWarshallMatrix():

    matrix = [
        [999999999 for x in range(len(state.grid))] for y in range(len(state.grid))
    ]

    for i in range(len(state.grid)):
        matrix[i][i] = 0  # cost from one stop to itself is 0
        for j in state.grid[
            "P" + str(i + 1)
        ]:  # "P"+str(i+1) transform indexes into our proper dictionary keys
            matrix[i][int(j[0][-1]) - 1] = j[
                1
            ]  # [int(j[0][-1])-1]   transform "PX" stops into the proper index of our matrix

    for k in range(len(state.grid)):
        for i in range(len(state.grid)):
            for j in range(len(state.grid)):
                matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

    return matrix


# _________________________________     MAIN FUNCTION     _________________________________

if __name__ == "__main__":

    (
        GRAPH,
        SCHOOLS,
        CHILDREN,
        INITIALONBOARD,
        INITPOS,
        CAPACITY,
    ) = parser()  # saves data from input file
    start = timer()  # start timer for search algorithm

    state.grid = GRAPH  # define value of static fields for the state class
    state.school_positions = SCHOOLS
    state.max_capacity = CAPACITY
    state.init_position = INITPOS
    state.floyd = (
        floydWarshallMatrix()
    )  # FloydWarshall matrix used by heuristics functions and stores it statically in state class

    if (
        sys.argv[2] == "no"
    ):  # convertin user input to our program parameter to use the specified heuristic function
        state.heuristic = 0
    elif sys.argv[2] == "MP":
        state.heuristic = 1
    elif sys.argv[2] == "MCAC":
        state.heuristic = 2
    else:
        print(
            'Error: Wrong heuristic name, type "/BusRouting.sh -h" in order to see possible values'
        )
        sys.exit()

    initial_state = state(
        INITPOS, 0, CHILDREN, INITIALONBOARD, 0, None
    )  # definition of our initial state
    result, nodes = Astar(initial_state)  # list containing final path found by A*

    end = timer()  # stops timer
    time = end - start

    outputWrite(result, time, str(nodes))  # creates .statistics & .output files
