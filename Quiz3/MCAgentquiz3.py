from collections import deque


class MCAgent:

    def __init__(self):
        pass

    def solve(self, initial_missionaries, initial_cannibals):
        # Add your code here! Your solve method should receive
        # the initial number of missionaries and cannibals as integers,
        # and return a list of 2-tuples that represent the moves
        # required to get all missionaries and cannibals from the left
        # side of the river to the right.
        #
        # If it is impossible to move the animals over according
        # to the rules of the problem, return an empty list of
        # moves.

        class States:
            def __init__(self, left_missionaries, left_cannibals, right_missionaries, right_cannibals, boat_position):
                self.left_missionaries = left_missionaries
                self.left_cannibals = left_cannibals
                self.right_missionaries = right_missionaries
                self.right_cannibals = right_cannibals
                self.boat_position = boat_position
                self.parent = None

            def __eq__(self, other):
                return (self.left_missionaries == other.left_missionaries and self.left_cannibals == other.left_cannibals and
                        self.right_missionaries == other.right_missionaries and self.right_cannibals == other.right_cannibals and
                        self.boat_position == other.boat_position)

            def goal_state(self):
                if self.left_missionaries == 0 and self.left_cannibals == 0 and self.right_missionaries == initial_missionaries \
                        and self.right_cannibals == initial_cannibals and self.boat_position == "right":
                    return True
                else:
                    return False

            def valid_state(self):
                if (self.left_missionaries != 0 and self.left_cannibals > self.left_missionaries) \
                        or (self.right_missionaries != 0 and self.right_cannibals > self.right_missionaries) \
                        or self.left_missionaries < 0 or self.left_cannibals < 0 or self.right_missionaries < 0 \
                        or self.right_cannibals < 0:
                    return False
                else:
                    return True

        def successors(curr_state):
            successor = []
            # Five possible moves: Move 2 Missionaries, or 2 Cannibals, or 1 M + 1 C, or 1 M only, or 1 C only
            possible_moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
            if curr_state.boat_position == "left":  # boat moves from left to right
                for move in possible_moves:
                    new_state = States(curr_state.left_missionaries - move[0], curr_state.left_cannibals - move[1],
                                       curr_state.right_missionaries + move[0], curr_state.right_cannibals + move[1], "right")
                    if new_state.valid_state():
                        successor.append(new_state)
                        new_state.parent = curr_state
            else:  # boat moves from right to left
                for move in possible_moves:
                    new_state = States(curr_state.left_missionaries + move[0], curr_state.left_cannibals + move[1],
                                       curr_state.right_missionaries - move[0], curr_state.right_cannibals - move[1], "left")
                    if new_state.valid_state():
                        successor.append(new_state)
                        new_state.parent = curr_state
            return successor

        def dfs():
            start = States(initial_missionaries, initial_cannibals, 0, 0, "left")
            if not start.valid_state():
                return None
            if start.goal_state():
                return start
            
            stack = [start]
            explored = []
            
            while stack:
                node = stack.pop()
                if node.goal_state():
                    return node
                explored.append(node)
                for child in successors(node):
                    if (child not in explored) and (child not in stack):
                        stack.append(child)
            return None
        def find_moves(goal_state):
            path = []
            node = goal_state
            
            while node.parent is not None:
                parent = node.parent
                moved_m = abs(node.left_missionaries - parent.left_missionaries)
                moved_c = abs(node.left_cannibals - parent.left_cannibals)
                path.append((moved_m, moved_c))
                node = parent
                
            return path
        goal = dfs()
        if goal is None:
            return []
        else:
            return find_moves(goal)
            