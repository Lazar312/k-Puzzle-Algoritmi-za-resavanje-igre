import random
import time
from collections import deque
import config


def reconstruct_path(start, goal, parent, parent_nodes):
    path = [goal]
    while parent != start:
        path.insert(0, parent)
        parent = parent_nodes[parent]
    path.insert(0, start)
    return path


class Algorithm:
    def __init__(self, heuristic=None):
        self.heuristic = heuristic
        self.nodes_evaluated = 0
        self.nodes_generated = 0

    def get_legal_actions(self, state):
        self.nodes_evaluated += 1
        max_index = len(state)
        zero_tile_ind = state.index(0)
        legal_actions = []
        if 0 <= (up_ind := (zero_tile_ind - config.N)) < max_index:
            legal_actions.append(up_ind)
        if 0 <= (right_ind := (zero_tile_ind + 1)) < max_index and right_ind % config.N:
            legal_actions.append(right_ind)
        if 0 <= (down_ind := (zero_tile_ind + config.N)) < max_index:
            legal_actions.append(down_ind)
        if 0 <= (left_ind := (zero_tile_ind - 1)) < max_index and (left_ind + 1) % config.N:
            legal_actions.append(left_ind)
        return legal_actions

    def apply_action(self, state, action):
        self.nodes_generated += 1
        copy_state = list(state)
        zero_tile_ind = state.index(0)
        copy_state[action], copy_state[zero_tile_ind] = copy_state[zero_tile_ind], copy_state[action]
        return tuple(copy_state)

    def get_steps(self, initial_state, goal_state):
        pass

    def get_solution_steps(self, initial_state, goal_state):
        begin_time = time.time()
        solution_actions = self.get_steps(initial_state, goal_state)
        print(f'Execution time in seconds: {(time.time() - begin_time):.2f} | '
              f'Nodes generated: {self.nodes_generated} | '
              f'Nodes evaluated: {self.nodes_evaluated}')
        return solution_actions


class ExampleAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        while state != goal_state:
            legal_actions = self.get_legal_actions(state)
            action = legal_actions[random.randint(0, len(legal_actions) - 1)]
            solution_actions.append(action)
            state = self.apply_action(state, action)
        return solution_actions


class BreadthFirstSearch(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        visited = set()
        queue = deque([(state, None)])
        parent_nodes = {}
        path = []
        while queue:
            state, parent = queue.popleft()
            legal_actions = self.get_legal_actions(state)
            if state == goal_state:
                path = reconstruct_path(initial_state, goal_state, parent, parent_nodes)
                break
            if state not in visited:
                parent_nodes[state] = parent
                visited.add(state)
                queue.extend((self.apply_action(state, action), state) for action in legal_actions)

        for i in range(0, len(path) - 1):
            state = path[i]
            statenext = path[i + 1]
            temp = state
            for action in self.get_legal_actions(state):
                if self.apply_action(temp, action) == statenext:
                    solution_actions.append(action)
                    break
                temp = state
        return solution_actions


class FirstBestSearch(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        visited = set()
        queue = deque([(state, None, self.heuristic.get_evaluation(state))])
        parent_nodes = {}
        path = []
        heuristicValue = 0
        while queue:
            state, parent, heuristicValue = queue.popleft()
            legal_actions = self.get_legal_actions(state)
            if state == goal_state:
                path = reconstruct_path(initial_state, goal_state, parent, parent_nodes)
                break
            if state not in visited:
                parent_nodes[state] = parent
                visited.add(state)
                for action in legal_actions:
                    nextState = self.apply_action(state, action)
                    nextHeuristic = self.heuristic.get_evaluation(nextState)
                    tupleToInsert = (nextState, state, nextHeuristic)
                    if not queue:
                        queue.extend([tupleToInsert])
                    else :
                        i = 0
                        for i in range(len(queue)):
                            if nextHeuristic < queue[i][2]:
                                queue.insert(i, (tupleToInsert))
                                break
                            if nextHeuristic == queue[i][2]:
                                if nextState < queue[i][0]:
                                    queue.insert(i, (tupleToInsert))
                                    break
                        if i == len(queue) - 1:
                            queue.extend([tupleToInsert])
        for i in range(10):
            print(queue[i])
        for i in range(0, len(path) - 1):
            state = path[i]
            statenext = path[i + 1]
            temp = state
            for action in self.get_legal_actions(state):
                if self.apply_action(temp, action) == statenext:
                    solution_actions.append(action)
                    break
                temp = state
        return solution_actions


class AStarSearch(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        visited = set()
        queue = deque([(state, None, self.heuristic.get_evaluation(state))])
        parent_nodes = {}
        path = []
        g = 1
        heuristicValue = 0
        while queue:
            state, parent, heuristicValue = queue.popleft()
            legal_actions = self.get_legal_actions(state)
            if state == goal_state:
                path = reconstruct_path(initial_state, goal_state, parent, parent_nodes)
                break
            if state not in visited:
                parent_nodes[state] = parent
                visited.add(state)
                self.heuristic.get_evaluation(state)
                for action in legal_actions:
                    nextState = self.apply_action(state, action)
                    nextHeuristic = self.heuristic.get_evaluation(nextState) + heuristicValue - self.heuristic.get_evaluation(state) + g
                    tupleToInsert = (nextState, state, nextHeuristic)
                    if not queue:
                        queue.extend([tupleToInsert])
                    else:
                        for i in range(len(queue)):
                            if nextHeuristic < queue[i][2]:
                                queue.insert(i, (tupleToInsert))
                                break
                            if nextHeuristic == queue[i][2]:
                                if nextState < queue[i][0]:
                                    queue.insert(i, (tupleToInsert))
                                    break
                        if i == len(queue) - 1:
                            queue.extend([tupleToInsert])

        for i in range(0, len(path) - 1):
            state = path[i]
            statenext = path[i + 1]
            temp = state
            for action in self.get_legal_actions(state):
                if self.apply_action(temp, action) == statenext:
                    solution_actions.append(action)
                    break
                temp = state
        return solution_actions
