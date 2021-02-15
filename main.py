from pathfinder.maze import Maze
import cv2 as cv
import numpy as np

fileName = input("Path to maze file: ")

img = cv.imread(fileName,cv.IMREAD_GRAYSCALE)

_, img = cv.threshold(img,127,255,cv.THRESH_BINARY)

ms = Maze(img)

ms.build_graph()

discovered = np.full(ms.adjList.shape,0)


file = cv.VideoWriter('plots/search.avi',
                         cv.VideoWriter_fourcc(*'MJPG'), 
                         20, (ms.width+1,ms.height+1))

plot_img = cv.imread('plots/GraphasMaze.png')

ms.search(ms.start, discovered, file, plot_img)

file.release()
