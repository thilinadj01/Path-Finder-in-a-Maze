import random
from queue import PriorityQueue

Maze = []
Mazedict = {}
BarrierList = []
StartNode = 0
GoalNode = 0
currentNodeValue = 0
topRow = [0, 8, 16, 24, 32, 40, 48, 56]
bottomRow = [7, 15, 23, 31, 39, 47, 55, 63]


def generate_maze():
    global Maze, StartNode, GoalNode, BarrierList
    ChoiceList = []

    for i in range(64):
        # List with nodes in maze
        Maze.append(i)
        # Used to randomly select barriers
        ChoiceList.append(i)

    StartNode = random.randint(0, 15)
    GoalNode = random.randint(48, 63)

    print("\nStart Node: ", StartNode, " Goal Node: ", GoalNode)
    ChoiceList.remove(StartNode)

    # Removes start node and goal node from choice list so those nodes won't be selected as barriers
    ChoiceList.remove(GoalNode)

    while len(BarrierList) != 6:
        barrier = random.choice(ChoiceList)

        # Removes chosen node choice list so it won't be selected as a barrier again
        ChoiceList.remove(barrier)

        BarrierList.append(barrier)

    print("\nBarriers List: ", BarrierList, "\n")

    for eachNode in BarrierList:
        # Displays barriers as #
        Maze[eachNode] = "#"

    print_maze()


def generate_maze_dict():
    for x in range(8):
        for y in range(8):
            # Maze with x,y coordinates
            Mazedict[x*8 + y] = {"X": x, "Y": y}


def print_maze():
    global Maze
    tempMaze = Maze

    for each in Maze:
        if each == StartNode:
            # Displays Start Node
            Maze[each] = "S"
        if each == GoalNode:
            # Displays Goal Node
            Maze[each] = "G"

    line = ""

    for row in range(8):
        for column in range(8):
            node = str(Maze[row+column*8])
            # Displays the maze line by line
            line = line + " [" + node.center(2) + "]  "

        print(line)
        line = ""
        print(line)

    Maze = tempMaze


def search_order(cn):           # Checks neighbour nodes in increasing order
    tempQueue = []

    if cn - 8 >= 0:
        # First left node
        tempQueue.append(cn - 8)

    if cn in topRow:
        pass
    else:
        # Then Up Node
        tempQueue.append(cn - 1)

    if cn in bottomRow:
        pass
    else:
        # Then down node
        tempQueue.append(cn + 1)

    if cn + 8 <= 63:
        # Then Right node
        tempQueue.append(cn + 8)

    # returns nodes as a list
    return tempQueue


def shortest_path_finder(bm):

    # Stores the details of the shortest path.but it is stored reversed. from goal to start node
    backPathList = []

    # append goal node to the backpathlist
    backPathList.append(GoalNode)

    # This value will go from Goal node to Start node because the shortest path details are store in reversed order
    finder = GoalNode

    while finder != StartNode:
        """
        gets the value of the key(finder is the key) in backmap. In the sense, this will take the parent node of
        a child node and that parent node will be a appended to backpathlist
        """
        backPathList.append(bm[finder])
        finder = bm[finder]

    # returns the shortest path in the correct order
    return backPathList[::-1]


def results(algo, vn, sp):          # Prints the results

    print("=" * 200, "\n" + str(algo).center(150) + "\n", "=" * 200, )

    print("\nVisited Nodes: ", vn)

    print("\nTime to find the goal: ", len(vn), "minutes")

    # print("\n", "Backward map", backMap)
    # print("\n", "Backward path", backpath)

    print("\nShortest path: ", sp, "\n")

    if algo == "Uniform Cost Search":
        print("Cost: ", currentNodeValue, "\n")

    print_maze()

    print("\n\n")


def bfs_algo():

    # Stores the visited node list
    visitedBFS = []

    # Stores the nodes which were suppose to be visited
    queueBFS = []

    # enqueue the start node to the queue
    queueBFS.append(StartNode)

    # Used create a map of visited list.But it is stored backwards.(form goal to start)
    backMap = {}

    while True:
        # gets the first node of the queue
        currentNode = queueBFS[0]

        # dequeues the first node
        queueBFS.remove(currentNode)

        # add that dequeued node to visited list
        visitedBFS.append(currentNode)

        # checks if the goal is found
        if GoalNode == currentNode:
            break

        # Gets the next nodes to be visited to a temporary list(with the increasing order)
        tempQueue = search_order(currentNode)

        # Stores the nodes in temporary list(tempqueue) to this list if the node doesn't contain a barrier
        barrierCheckPassedList = []

        for eachTempNode in tempQueue:
            if eachTempNode in BarrierList:
                continue
            else:
                # If each node in temp queue doesn't contain a barrier, those nodes will added to this list
                barrierCheckPassedList.append(eachTempNode)

        # Check if each node in this list has already been visited
        for eachCheckedNode in barrierCheckPassedList:
            if eachCheckedNode in visitedBFS:
                continue
            else:
                if eachCheckedNode in queueBFS:
                    pass
                else:
                    # if a node doesn't contain a barrier or has been visited earlier,then it will be added to the queue
                    queueBFS.append(eachCheckedNode)

                    """
                    One node can have multiple child nodes. but in a dictionary, same key can't be repeated.
                    So parent node can't be a key in a dictionary. Since a child node has only one parent node,
                    dictionary named backmap will have child node as the key and current node(parent node) as value
                    So this back map is going to map all moves backwards
                    """

                    backMap[eachCheckedNode] = currentNode

    # this will get the shortest path
    shortestPath = shortest_path_finder(backMap)

    # this will print the results
    results("Breadth First Search", visitedBFS, shortestPath)


def dfs_algo():

    # Stores the nodes which were suppose to be visited
    StackDFS = []

    # Stores the visited node list
    visitedDFS = []

    # Used create a map of visited list.But it is stored backwards.(form goal to start)
    backMap = {}

    # adds the start node to the stack
    StackDFS.append(StartNode)

    while True:
        # Gets the current Node from the stack
        currentNode = StackDFS.pop()

        if currentNode in visitedDFS:
            continue

        else:
            # add the current node to the visited list
            visitedDFS.append(currentNode)

        # checks if the goal is found
        if GoalNode == currentNode:
            break

        # Gets the next nodes to be visited to a temporary list(with the increasing order)
        tempStack = search_order(currentNode)

        # Since stacks are based on the LIFO principle(last in, first out), the list has to be reversed
        tempStackRev = tempStack[::-1]

        barrierCheckPassedList = []

        for eachTempNode in tempStackRev:
            if eachTempNode in BarrierList:
                continue
            else:
                barrierCheckPassedList.append(eachTempNode)

        for eachCheckedNode in barrierCheckPassedList:
            if eachCheckedNode in visitedDFS:
                continue
            else:
                # if a node doesn't contain a barrier or has been visited earlier,then it will be added to the Stack
                StackDFS.append(eachCheckedNode)

                # add the move to the backmap
                backMap[eachCheckedNode] = currentNode

    # this will get the shortest path # this will print the results
    shortestPath = shortest_path_finder(backMap)

    # this will print the results
    results("Depth First Search", visitedDFS, shortestPath)


def ucs_algo():
    global currentNodeValue

    # Stores the nodes which were suppose to be visited
    queueUCS = []

    # Stores the visited node list
    visitedUCS = []

    # Used create a map of visited list.But it is stored backwards.(form goal to start)
    backMap = {}

    # enqueue the start node and path cost(which is zero) to the queue
    queueUCS.append([StartNode, 0])

    while True:
        # Get the current node
        currentNode = queueUCS[0][0]

        # Get the path cost of the current node
        currentNodeValue = queueUCS[0][1]

        # Dequeue the first element
        queueUCS.remove(queueUCS[0])

        if currentNode not in visitedUCS:
            # Add the current node to the visited list
            visitedUCS.append(currentNode)

        # checks if the goal is found
        if GoalNode == currentNode:
            break

        # Gets the next nodes to be visited to a temporary list(with the increasing order)
        tempQueue = search_order(currentNode)

        barrierCheckPassedList = []

        for eachTempNode in tempQueue:

            if eachTempNode in BarrierList:
                continue

            else:
                # If each node in tempqueue doesn't contain a barrier, those nodes will added to this list
                barrierCheckPassedList.append(eachTempNode)

        for eachCheckedNode in barrierCheckPassedList:

            # Check if each node in this list has already been visited
            if eachCheckedNode in visitedUCS:
                continue
            """ 
            if that node isn't visited and if the queue is already empty, then a list containing the next node and it's
            path cost will be added to the queue
            """

            if len(queueUCS) == 0:
                queueUCS.append([eachCheckedNode, currentNodeValue + 1])
                backMap[eachCheckedNode] = currentNode
                continue

            for each in queueUCS:

                # Checks if the node already in the queue
                if eachCheckedNode == each[0]:
                    # If new path has lesser cost, then the cost will be updated
                    if currentNodeValue + 1 < each[1]:
                        queueUCS[each[0]][1] = currentNodeValue + 1
                        backMap[eachCheckedNode] = currentNode
                        break

                else:
                    # if the node isn't in the queue yet, then it will be added to the queue
                    queueUCS.append([eachCheckedNode, currentNodeValue + 1])
                    backMap[eachCheckedNode] = currentNode
                    break

            minval = 999
            temp = 0

            # searches the node with lowest cost
            for each in queueUCS:
                if each[1] < minval:
                    minval = each[1]
                    temp = each

            # takes the node with lowest cost to the front in the queue
            exchanger = queueUCS[0]
            if temp != exchanger:
                queueUCS[0] = temp
                queueUCS.append(exchanger)

    shortestPath = shortest_path_finder(backMap)
    results("Uniform Cost Search", visitedUCS, shortestPath)


def heuristic_cost(n, called_by):           # Calculates heuristic cost
    Nx = Mazedict[n]["X"]
    Gx = Mazedict[GoalNode]["X"]
    Ny = Mazedict[n]["Y"]
    Gy = Mazedict[GoalNode]["Y"]
    delta_X = Nx - Gx
    delta_Y = Ny - Gy

    if delta_X < 0:
        delta_X = delta_X*(-1)
    if delta_Y < 0:
        delta_Y = delta_Y*(-1)

    mDistance = delta_X + delta_Y

    if called_by == 0:
        manhattan_result(Nx, Gx, Ny, Gy, mDistance)
    elif called_by == 1:
        return mDistance


def manhattan_result(nx, gx, ny, gy, md):           # Displays heuristic cost
    print("=" * 200, "\n" + str("Heuristic Cost Using The Manhattan Distance").center(150) + "\n", "=" * 200, )

    print("\n")

    print("d(N,G) = |Nx − Gx| + |Ny − Gy|")

    print("       = |", nx, " - ", gx, "| + |", ny, " - ", gy, "|")

    print("       = ", md)

    print("\nHeuristic cost: ", md)

    print("\n\n")


def bestfs_algo():

    # Priority queue has been used to get nodes with lowest path cost
    queueBestFS = PriorityQueue()

    visitedBestFS = []
    backMap = {}

    # gets heuristic cost
    heu_cost = heuristic_cost(StartNode, 1)

    # appends the cost and node to the queue
    queueBestFS.put((heu_cost, StartNode))

    while True:
        currentNode = queueBestFS.get()[1]
        visitedBestFS.append(currentNode)

        if GoalNode == currentNode:
            break

        tempQueue = search_order(currentNode)

        barrierCheckPassedList = []
        for eachTempNode in tempQueue:
            if eachTempNode in BarrierList:
                continue
            else:
                barrierCheckPassedList.append(eachTempNode)

        for eachCheckedNode in barrierCheckPassedList:
            if eachCheckedNode in visitedBestFS:
                continue
            else:
                # Gets heuristic cost of each child node of the current node
                heu_cost = heuristic_cost(eachCheckedNode, 1)

                # adds the costs and child nodes to the queue
                queueBestFS.put((heu_cost, eachCheckedNode))

                backMap[eachCheckedNode] = currentNode

    shortestPath = shortest_path_finder(backMap)
    results("Best First Search", visitedBestFS, shortestPath)


def ass_algo():
    ScoredMaze = []
    for i in range(64):
        """
        Used to store the path costs of the nodes. all node's path cost is zero in the beginning. they will be updated
        if needed
        """
        ScoredMaze.append([i, 0])

    queueASS = PriorityQueue()
    visitedASS = []
    backMap = {}

    # Calculates cost(path cost + heuristic cost)
    cost = ScoredMaze[StartNode][1] + heuristic_cost(StartNode, 1)

    queueASS.put((cost, StartNode))

    while True:
        currentNode = queueASS.get()[1]
        visitedASS.append(currentNode)

        if GoalNode == currentNode:
            break

        tempQueue = search_order(currentNode)

        barrierCheckPassedList = []
        for eachTempNode in tempQueue:
            if eachTempNode in BarrierList:
                continue
            else:
                barrierCheckPassedList.append(eachTempNode)

        for eachCheckedNode in barrierCheckPassedList:
            if eachCheckedNode in visitedASS:
                continue
            else:
                # updates the path costs of each child node
                ScoredMaze[eachCheckedNode][1] = ScoredMaze[eachCheckedNode][1] + 1

                # Calculates cost(path cost + heuristic cost) of each child node
                cost = heuristic_cost(eachCheckedNode, 1) + ScoredMaze[eachCheckedNode][1]

                queueASS.put((cost, eachCheckedNode))
                backMap[eachCheckedNode] = currentNode

    shortestPath = shortest_path_finder(backMap)
    results("A Star Search", visitedASS, shortestPath)


generate_maze()
generate_maze_dict()
bfs_algo()
dfs_algo()
ucs_algo()
heuristic_cost(StartNode, 0)
bestfs_algo()
ass_algo()
