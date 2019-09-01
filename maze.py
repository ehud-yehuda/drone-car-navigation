import numpy as np
import matplotlib.pyplot as plt
import operator


DEBUG = False
Plot = True

def load_Data(path, Plot):

    with open(path) as f:
        width, heighet, numObstacle  = [int(x) for x in next(f).split()]
        SourceI, SourceJ, destinationI, destinationJ = [int(x) for x in next(f).split()]
        obstacle = [[int(x) for x in line.split()] for line in f]
    f.close()

    maze = np.zeros((width, heighet, 3))
    for ObstacleIdx in range(numObstacle):
        maze[obstacle[ObstacleIdx][0]:obstacle[ObstacleIdx][2] + 1, obstacle[ObstacleIdx][1]:obstacle[ObstacleIdx][3] + 1] = [0, 255, 0] #green

    maze[SourceI, SourceJ, :] = [255, 0, 0] #red
    maze[destinationI, destinationJ, :] = [255, 0, 0] #red



    if Plot:
        plt.figure(1)
        plt.imshow(maze)
        plt.text(SourceJ, SourceI, 'Source')
        plt.text(destinationJ, destinationI, 'Destination')
        plt.title('Maze to solve- Good Luck!')
        plt.show(block=False)

    return maze, [SourceI, SourceJ], [destinationI, destinationJ]

def canMove(maze, i, j):
    if(i >= 0 and j >= 0 and i < maze.shape[0] and j < maze.shape[1]):
        Val = maze[i,j]
        if all(Val == [0, 0, 0]) or all(Val == [255, 0, 0]):
            return True
    return False


def BFS(maze, start, end):

    queue = []

    queue.append([start])
    maze[start[0], start[1], :] = [127, 127, 127]

    while queue:

        path = queue.pop(0)
        position = path[-1]

        if position == end:
            return path

        for neighboor in [(0, -1), (-1, 0), (1, 0), (0, 1), (1, -1), (1, 1), (-1, 1), (-1, -1)]:
            nextposition = list(map(operator.add, position, neighboor))
            if canMove(maze, nextposition[0], nextposition[1]):
                new_path = list(path)
                new_path.append(nextposition)
                maze[nextposition[0], nextposition[1], :] = [127, 127, 127] # mark as visited
                queue.append(new_path)


    print("I'm exahusted and didn't found my way...")
    return start.append(end)

def main():
    #path = 'C:\\Users\\owner\\Desktop\\maze\\maze.txt'
    path = 'maze.txt'
    #outputPath = 'C:\\Users\\owner\\Desktop\\maze\\ShortestPath.txt'
    outputPath = 'ShortestPath.txt'
    #load data

    maze, start, destination = load_Data(path, Plot)

    shortestpath = BFS(maze, start, destination)

    if(shortestpath):
        maze, start, destination = load_Data(path, Plot) #The maze got dirty because all the visiting, therfore loading a new one

        for point in shortestpath:
            maze[point[0], point[1], :] = [0, 0, 255] #blue is the shortest path

        if Plot:
            plt.figure(2)
            plt.imshow(maze)
            plt.text(start[1], start[0], 'Source')
            plt.text(destination[1], destination[0], 'Destination')
            plt.title('maze with the shortes path!')
            plt.show (block=False)

        distance = len(shortestpath)
        shortestpath.append(distance)

        with open(outputPath, 'w') as f:
            for point in shortestpath:
                f.write("%s\n" % point)
        f.close()
    else:
        with open(outputPath, 'w') as f:
                f.write("%s\n" % "Didn't found any solution")
        f.close()

if __name__ == '__main__':
    main()

