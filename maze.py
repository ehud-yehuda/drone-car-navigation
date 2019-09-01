import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Queue
import operator
import itertools
import sys
import os
import math

DEBUG = True
Plot = True



def getNeighboors(position):
    i,j = position
    if i > 0 and j > 0:
        return [(i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j), (i-1, j), (i+1, j+1), (i, j+1), (i-1, j+1)]
    elif i > 0:
        return [(i + 1, j), (i - 1, j), (i + 1, j + 1), (i, j + 1), (i - 1, j + 1)]
    elif j > 0:
        return [(i, j - 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
    else:
        return [(i + 1, j), (i + 1, j + 1), (i, j + 1)]


def canMove(maze, i, j):
    if(i >= 0 and j >= 0 and i < maze.shape[0] and j < maze.shape[1]):
        Val = maze[i,j]
        if all(Val == [0, 0, 0]) or all(Val == [255, 0, 0]):
            return True
    return False


def BFS(maze, start, end, visited):
    #queue = Queue()
    #queue.put([start])

    frontier = []
    frontier.append([start])
    maze[start] = [127, 127, 127]

    while frontier:

        path = frontier.pop(0)
        position = path[-1]

        if position == end:
            return path

        for d in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nextposition = list(map(operator.add, position, d))
            if canMove(maze, nextposition[0], nextposition[1]):
                new_path = list(path)
                new_path.append(nextposition)
                maze[nextposition] = [127, 127, 127]
                frontier.append(new_path)


    return visited


def main():
    path = 'C:\\Users\\owner\\Desktop\\maze\\maze.txt'
    #load data
    with open(path) as f:
        width, heighet, numObstacle  = [int(x) for x in next(f).split()]
        SourceI, SourceJ, destinationI, destinationJ = [int(x) for x in next(f).split()]
        obstacle = [[int(x) for x in line.split()] for line in f]
    f.close()

    maze = np.zeros((width, heighet, 3))
    for ObstacleIdx in range(numObstacle):
        maze[obstacle[ObstacleIdx][0]:obstacle[ObstacleIdx][2] + 1, obstacle[ObstacleIdx][1]:obstacle[ObstacleIdx][3] + 1] = [0, 255, 0] #green

    maze[SourceI:, SourceJ,:] = [255, 0, 0] #red
    maze[destinationI, destinationJ, :] = [255, 0, 0] #red

    maze2solve = maze
    if Plot:
        plt.figure(1)
        plt.imshow(maze)
        plt.text(SourceJ, SourceI, 'Source')
        plt.text(destinationJ, destinationI, 'Destination')
        plt.title('Maze to solve- Good Luck!')
        plt.show()

    path = BFS(maze2solve, [SourceI, SourceJ], [destinationI, destinationJ], [])

    if Plot:
        plt.figure(2)
        plt.imshow(maze2solve)
        plt.text(SourceJ, SourceI, 'Source')
        plt.text(destinationJ, destinationI, 'Destination')
        plt.title('used maze!')
        plt.show()

    a=1



if __name__ == '__main__':
      #main(sys.argv[1], sys.argv[2])
    main()

""" while not queue.empty():

        path = queue.get()
        position = path[-1]

        if position == end:
            return path

        for neighboor in getNeighboors(position):
            i,j = neighboor
            if canMove(maze, i, j):
                maze[i,j] = [127, 127, 127]
                new_path = list(path)
                new_path.append(neighboor)
                queue.put(new_path)"""