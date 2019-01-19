import numpy as np
from heapq import heappush, heappop
from animation import draw
import argparse
from operator import itemgetter, attrgetter, methodcaller
# Mohammadali Saffary
class Node():
    """
    cost_from_start - the cost of reaching this node from the starting node
    state - the state (row,col)
    parent - the parent node of this node, default as None
    """
    def __init__(self, state, cost_from_start, parent = None):
        self.state = state
        self.parent = parent
        self.cost_from_start = cost_from_start


class Maze():
    
    def __init__(self, map, start_state, goal_state, map_index):
        self.start_state = start_state
        self.goal_state = goal_state
        self.map = map
        self.visited = [] # state
        self.m, self.n = map.shape 
        self.map_index = map_index


    def draw(self, node):
        path=[]
        while node.parent:
            path.append(node.state)
            node = node.parent
        path.append(self.start_state)
    
        draw(self.map, path[::-1], self.map_index)


    def goal_test(self, current_state):
        # your code goes here:
        return np.array_equal(current_state, self.goal_state)


    def get_cost(self, current_state, next_state):
        # your code goes here:
        return 1

    def get_successors(self, state):
        # your code goes here:
        successors = []
        # your code goes here:
        row = [1, -1, 0, 0]
        col = [0, 0, -1, 1]
        rows = state[0]
        columns = state[1]
        for k in range (4):
            newi = rows + row[k]
            newj = columns + col[k]
            if self.map[newi,newj] == 1:
                new = (newi,newj)
                successors.append(new)
        return successors


    # heuristics function
    def heuristics(self, state):
        # your code goes here:
        x = abs(self.goal_state[0]-state[0])
        y = abs(self.goal_state[1]-state[1])
        return x+y


    # priority of node 
    def priority(self, node):
        # your code goes here:
        return self.get_cost(node.parent,node)

    
    # solve it
    def solve(self):
        # your code goes here:
        container = []
        count = 1
        state = self.start_state
        node = Node(state, 0, None)
        self.visited = []
        self.visited.append(state)
        container.append((0,0,node))
        while container:
            current = (container.pop())[2]
            if self.goal_test(current.state):
                print("found it")
                self.draw(current)
                break
            successors = self.get_successors(current.state)
            for next_state in successors:
                if next_state not in self.visited:
                    next_heur = self.heuristics(next_state)
                    next_cost = current.cost_from_start + self.get_cost(current.state, next_state)
                    next_node = Node(next_state, next_cost, current)
                    container.append((next_heur + next_cost, count, next_node))
                    container = sorted(container, key=itemgetter(0,1), reverse = True)
                    self.visited.append(next_node.state)
                    count += 1


            
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='maze')
    parser.add_argument('-index', dest='index', required = True, type = int)
    index = parser.parse_args().index

    # Example:
    # Run this in the terminal solving map 1
    #     python maze_astar.py -index 1
    
    data = np.load('map_'+str(index)+'.npz')
    map, start_state, goal_state = data['map'], tuple(data['start']), tuple(data['goal'])

    game = Maze(map, start_state, goal_state, index)
    game.solve()
    