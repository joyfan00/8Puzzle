# Joy Fan
# CSDS 391: Programming Assignment 1

# import packages
import random
from queue import PriorityQueue

class EightPuzzle:
    # global variables
    # contains the 8 puzzle board
    state = []
    # goal state
    goal_state = ["b", "1", "2", "3", "4", "5", "6", "7", "8"]
    # cost
    cost = 0
    # nodes
    nodes = 0
    # maxNodes
    max_nodes = 0

    # constructor
    def __init__(self):
        pass
    # reads in the file using the name of the textfile
    def readInFile(self, textfile):
        # reads in the files
        file1 = open(textfile, "r")
        # gets a list of lines from the text file
        lines = file1.readlines()
        # iterates through each line in the text file
        for line in lines:
            # gets rid of any white space before and after the command and parameter
            line = line.strip()
            if " " in line:
                # helps to splice the command and parameter
                first_space_index = line.index(' ')
                # command and parameter
                command = line[:first_space_index]
                parameter = line[first_space_index + 1:]
            else:
                command = line
            # necessary for solving for a-star or beam
            if command == "solve":
                second_space_index = line.find(' ', first_space_index + 1)
                command = line[:second_space_index]
                parameter = line[second_space_index + 1:]
                if command == "solve A-star":
                    self.solve_A_Star(parameter)
                elif command == "solve beam":
                    self.solve_beam(int(parameter))
            else:
                # calls setState function if selfState appears
                if command == "setState":
                    self.setState(parameter)
                # calls printState function if printState appears
                elif command == "printState":
                    self.printState()
                # calls the move function if move appears
                elif command == "move":
                    self.move(parameter)
                # calls the randomizeState function if randomizeState appears
                elif command == "randomizeState":
                    self.randomizeState(int(parameter))
                elif command == "maxNodes":
                    self.maxNodes(int(parameter))
                else:
                    print("No command available")

    # # sets the state of the 8-puzzle
    def setState(self, state):
        if type(state) is str:
            self.state = list(state.replace(" ", ""))
        elif type(state) is list:
            self.state = state

    # prints the state passed in the parameter
    def printState(self):
        stringState = self.toString(self.state)
        print(stringState)

    # converts the state to a string
    def toString (self, state):
        # joins all list items together into a string
        stringState = ''.join(state)
        # adds space every three letters
        stringState = ' '.join(stringState[i:i + 3] for i in range(0, len(stringState), 3))
        return stringState

    # moves the blank tile to corresponding direction
    def move(self, direction):
        if direction == "left":
            return self.moveLeft(self.state.index("b"))
        elif direction == "right":
            return self.moveRight(self.state.index("b"))
        elif direction == "up":
            return self.moveUp(self.state.index("b"))
        elif direction == "down":
            return self.moveDown(self.state.index("b"))
        # no corresponding direction: return false
        else:
            return False

    # moves the blank to the left
    def moveLeft(self, blank):
        # unable to move to the left condition
        if blank % 3 == 0:
            return False
        # swaps locations
        temp = self.state[blank - 1]
        self.state[blank - 1] = "b"
        self.state[blank] = temp
        return True

    # moves the blank to the right
    def moveRight(self, blank):
        # doesn't allow to move right if unable to
        if blank % 3 == 2:
            return False
        # swaps locations
        temp = self.state[blank + 1]
        self.state[blank + 1] = "b"
        self.state[blank] = temp
        return True

    # moves the blank to the left
    def moveUp(self, blank):
        # doesn't allow to move up if unable to
        if blank - 3 < 0:
            return False
        # swaps locations
        temp = self.state[blank - 3]
        self.state[blank - 3] = "b"
        self.state[blank] = temp
        return True

    # moves the blank to the down
    def moveDown(self, blank):
        # doesn't allow to move down if unable to
        if blank + 3 > 8:
            return False
        # swaps locations
        temp = self.state[blank + 3]
        self.state[blank + 3] = "b"
        self.state[blank] = temp
        return True

    # randomize the state
    def randomizeState(self, n):
        random.seed(10)
        # sets the current state to the goal state
        self.setState(["b", "1", "2", "3", "4", "5", "6", "7", "8"])
        # counter to determine how many moves have been taken
        counter = 0
        # loops until all randomized moves have been made
        while counter < n:
            # helps to determine what action the computer will take
            random_move = random.randint(1, 4)
            # determines if the move actually was executed (some are unable to occur)
            ifMoved = True
            # 1: moving up, checks to see if was able to execute
            if random_move == 1:
                ifMoved = self.move("up")
            # 2: moving down, checks to see if was able to execute
            elif random_move == 2:
                ifMoved = self.move("down")
            # 3: moving right, checks to see if was able to execute
            elif random_move == 3:
                ifMoved = self.move("right")
            # 4: moving left, checks to see if was able to execute
            else:
                ifMoved = self.move("left")
            # if was able to execute, count as a random move that occurred
            if ifMoved:
                counter += 1

    # solve A star algorithm: searches when
    def solve_A_Star(self, heuristic):
        # reset the cost
        self.cost = 0
        if heuristic == "h1":
            self.solve_h1()
        elif heuristic == "h2":
            self.solve_h2()
        else:
            return False

    # helper method for solving A star using h1 heuristic
    def solve_h1(self):
        # set initial parent as the original state
        parent = self.state
        # priority queue as frontier
        frontier = PriorityQueue()
        # reached as a HashMap or in this case a dictionary (Python)
        reached = {}
        # frontier's first value for parent, contains heuristic + cost, cost, and parent string
        frontier.put((self.cost + self.h1_value(parent), (self.cost, self.toString(parent))))
        # reached first value for parent
        reached[self.toString(parent)] = {"parent": None, "heuristic + cost": self.h1_value(parent) + self.cost, "cost":self.cost}
        # determines whether the goal state has been reached
        isReached = False
        # 3 conditions: while the queue is not empty (if its empty, no other values), whether the number
        # of nodes explored is less than the maximum number of nodes allowed to be explored, and if the
        # goal state is not reached yet
        while not frontier.empty() and len(reached.keys()) < self.max_nodes and not isReached:
            # the tuple with parent heuristic + cost and the cost
            parent_tuple = frontier.get()
            # gets the heuristic + cost and the cost separately from the tuple
            heuristic_cost, (self.cost, parent) = parent_tuple
            print(parent)
            # converts parent string to list to better compare
            parent = list(parent.replace(" ", ""))
            # sees if the parent state is the same as the goal state
            if parent == self.goal_state:
                isReached = True
                break
            self.cost += 1
            # iterates through the list of expanded nodes
            for child in self.expand(parent):
                child_string = self.toString(child)
                heuristic_cost = self.h1_value(child) + self.cost
                if self.toString(child) not in reached.keys():
                    reached[child_string] = {"parent": parent, "heuristic + cost": heuristic_cost, "cost": self.cost}
                    frontier.put((heuristic_cost, (self.cost, child_string)))
        if isReached:
            print("Number of nodes:" + str(len(reached.keys())))
            print("Number of moves: " + str(self.cost))
        else:
            print("not found")

    # helper method for solving A star using h2 heuristic
    def solve_h2(self):
        # set initial parent as the original state
        parent = self.state
        # priority queue as frontier
        frontier = PriorityQueue()
        # reached as a HashMap or in this case a dictionary (Python)
        reached = {}
        # frontier's first value for parent, contains heuristic + cost, cost, and parent string
        frontier.put((self.cost + self.h2_value(parent), (self.cost, self.toString(parent))))
        # reached first value for parent
        reached[self.toString(parent)] = {"parent": None, "heuristic + cost": self.h2_value(parent) + self.cost,
                                          "cost": self.cost}
        # checks to see if goal state has been reached
        isReached = False
        # 3 conditions: while the queue is not empty (if its empty, no other values), whether the number
        # of nodes explored is less than the maximum number of nodes allowed to be explored, and if the
        # goal state is not reached yet
        while not frontier.empty() and (len(reached.keys()) < self.max_nodes) and not isReached:
            # the tuple with parent heuristic + cost, the cost, and the parent
            heuristic_cost, (self.cost, parent) = frontier.get()
            print(parent)
            # converts parent string to list to better compare
            parent = list(parent.replace(" ", ""))
            # sees if the parent state is the same as the goal state
            if parent == self.goal_state:
                isReached = True
                break
            self.cost += 1
            # iterates through the list of expanded nodes
            for child in self.expand(parent):
                # the string version of child's state
                child_string = self.toString(child)
                # heuristic + cost of child
                heuristic_cost = self.h2_value(child) + self.cost
                # only adding non explored expanded nodes to the hashmap and queue
                if self.toString(child) not in reached.keys():
                    reached[child_string] = {"parent": parent, "heuristic + cost": heuristic_cost, "cost": self.cost}
                    frontier.put((heuristic_cost, (self.cost, child_string)))
        # if reached, print out the number of nodes explored and number of moves
        if isReached:
            print("Number of nodes explored:" + str(len(reached.keys())))
            print("Number of moves: " + str(self.cost))
        # if not, print not found
        else:
            print("not found")

    # provides the heuristic value for h1: misplaced tiles
    def h1_value(self, state):
        counter = 0
        for i in range(len(state)):
            if state[i] != self.goal_state[i]:
                counter += 1
        return counter

    # provides the heuristic value for h2: Manhattan distance
    def h2_value(self, state):
        # heuristic value
        heuristic = 0
        for value in self.goal_state:
            # finds the index of where it should be in goal state
            goal_state_index = self.goal_state.index(value)
            # finds the index of the actual state
            actual_state_index = state.index(value)
            # adds the row + column distance together
            heuristic += abs(actual_state_index - goal_state_index) // 3 + \
                         abs(actual_state_index - goal_state_index) % 3
        return heuristic

    # expands the parents
    def expand(self, parent):
        # contains the feasible states (not all states are possible)
        feasibleStates = []
        # create a new list for the original state
        original = []
        for val in parent:
            original.append(val)
        # reset the original state for testing the left move
        self.setState(original)
        left = self.move("left")
        # appends the left move if possible
        if left:
            # copies the current state when moving the blank space left
            left_move = []
            for val in self.state:
                left_move.append(val)
            feasibleStates.append(left_move)
        # resets the original state for testing the right move
        original = []
        for val in parent:
            original.append(val)
        self.setState(original)
        right = self.move("right")
        if right:
            # copies the current state when moving the blank space right
            right_move = []
            for val in self.state:
                right_move.append(val)
            feasibleStates.append(right_move)
        #resets the original state for testing the up move
        original = []
        for val in parent:
            original.append(val)
        self.setState(original)
        up = self.move("up")
        # appends the up move if feasible
        if up:
            # copies the current state when moving the blank space up
            up_move = []
            for val in self.state:
                up_move.append(val)
            feasibleStates.append(up_move)
        # resets the original state for testing the down move
        original = []
        for val in parent:
            original.append(val)
        self.setState(original)
        down = self.move("down")
        # appends the down move if feasible
        if down:
            # copies the current state when moving the blank space down
            down_move = []
            for val in self.state:
                down_move.append(val)
            feasibleStates.append(down_move)
        # resets the original state for testing the down move
        original = []
        for val in parent:
            original.append(val)
        self.setState(original)
        return feasibleStates

    # completes local beam search, using h1 as my heuristic
    def solve_beam (self, k):
        # reset the cost
        self.cost = 0
        # sets the parent to the current state
        parent = self.state
        # creates frontier
        frontier = PriorityQueue()
        # tracks whether the goal state has been reached
        isReached = False
        # puts the current parent value into the queue
        frontier.put((self.h2_value(parent), self.toString(parent)))
        # keeps track of nodes explored
        self.nodes = 1
        # 3 conditions: if the queue is not empty, whether the goal state has been reached,
        # if the nodes explored is less than the maximum number of nodes
        while not frontier.empty() and not isReached and self.nodes < self.max_nodes:
            # states we want to explore further
            current_states = []
            # 2 conditions: if the queue size is less than k, we want to keep expanding until we can
            # choose the best k states
            if frontier.qsize() < k:
                # puts all of the values from the queue into the current states list to expand
                while not frontier.empty():
                    value, parent = frontier.get()
                    current_states.append(list(parent.replace(" ", "")))
                # due to the fact that we popped out all values from the queue, we want to add
                # them back with their expanded nodes
                frontier, isReached = self.resetAndExpandQueue(frontier, current_states)
                if isReached:
                    break
                self.cost += 1
            # the queue is larger than k, therefore we can start popping the best k states and expanding those
            else:
                # pops the best k states
                for i in range (k):
                    val, parent = frontier.get()
                    current_states.append(list(parent.replace(" ", "")))
                # due to the fact that we popped out all values from the queue, we want to add
                # them back with their expanded nodes
                frontier, isReached = self.resetAndExpandQueue(frontier, current_states)
                if isReached:
                    break
                self.cost += 1
        if isReached:
            print("Number of nodes:" + str(self.nodes))
            print("Moves: " + str(self.cost))
        else:
            print("Not found")

    # empties the priority queue and adds all initial and expanded states into the queue
    def resetAndExpandQueue (self, frontier, listStates):
        isReached = False
        # resets the queue
        frontier = PriorityQueue()
        # iterates through each beginning state
        for state in listStates:
            # break out of loop if the number of nodes explored is greater than the number of max nodes allowed
            if self.nodes > self.max_nodes:
                break
            print(state)
            # increments node explored
            self.nodes += 1
            # puts value into queue
            frontier.put((self.h2_value(state), self.toString(state)))
            # checks to see if initial state is the goal state
            if state == self.goal_state:
                isReached = True
                break
            # adds expanded nodes into queue
            for child in self.expand(state):
                self.nodes += 1
                print(child)
                # puts child into queue
                frontier.put((self.h2_value(child), self.toString(child)))
                if self.max_nodes == self.nodes:
                    break
        return frontier, isReached

    # sets the maximum number of nodes before declaring the puzzle unsolvable
    def maxNodes(self, n):
        self.max_nodes = n


e = EightPuzzle()
e.readInFile("testing")


