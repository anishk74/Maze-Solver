import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

class Maze:
	def __init__(self,img):
		self.img=img
		self.height, self.width = img.shape
		self.start=None
		self.exit=None
		self.sepWidth=0
		self.cellWidth=0
		self.adjList=None

	#finding start and exit
	def findSnE(self):
		openCells=np.array([],dtype='int')
		for i in [0,self.width-1]:
			indices = np.where(self.img[:,i]==255)[0]
			if(len(indices)==0):
				continue
			else:
				openCells = np.append(openCells,[0,indices[0],i])

		for i in [0,self.height-1]:
			indices = np.where(self.img[i,:]==255)[0]
			if(len(indices)==0):
				continue
			else:
				openCells = np.append(openCells,[1,i,indices[0]])
		return openCells.reshape(2,3)



	def build_graph(self,save_search=True):
		
		openCells=self.findSnE()
		if len(openCells)<2:
			print('Cannot find start and exit')
			return

		if openCells[0][0]==0:
			self.cellWidth = len(np.where(self.img[:,openCells[0,2]] == 255)[0])
			self.sepWidth = len(np.where(self.img[self.cellWidth//2,:self.cellWidth//2] == 0)[0])

		else:
			self.cellWidth = len(np.where(self.img[openCells[0,1],:] == 255)[0])
			self.sepWidth = len(np.where(self.img[self.cellWidth//2,:self.cellWidth//2] == 0)[0])


		img=cv.cvtColor(self.img,cv.COLOR_GRAY2RGB)
		for i in range(2):
			if openCells[i,0] == 0:
				img[openCells[i,1]:openCells[i,1]+self.cellWidth,openCells[i,2]] = [0, 0 ,255]
			else:
				img[openCells[i,1],openCells[i,2]:openCells[i,2]+self.cellWidth] = [0, 0 ,255]

		print('Found start and exit.')
		if(save_search==True):
			cv.imwrite('plots/StartandExit.png',img)

		#Locating cells and finding openings between them
		unitWidth = self.sepWidth + self.cellWidth
		img[self.sepWidth+self.cellWidth//2::unitWidth, self.sepWidth+self.cellWidth//2::unitWidth] = [255,0,255]
		print('Located cells.')
		if(save_search==True):
			cv.imwrite('plots/MazeCells.png',img)
		

		for c in openCells:
			if c[1]==0 or c[2] == 0:
				continue
			if c[1] == self.height-1:
				c[1]-=unitWidth
			else:
				c[2]-=unitWidth
		#print(unitWidth,openCells)


		self.start=[openCells[0][1]//unitWidth,openCells[0][2]//unitWidth]
		self.exit=[openCells[1][1]//unitWidth,openCells[1][2]//unitWidth]

		nCols = self.width//(self.cellWidth+self.sepWidth)
		nRows = self.height//(self.cellWidth+self.sepWidth)
		#print(nRows,nCols)
		self.adjList=np.full((nRows,nCols), "", dtype='<U4')
		
		
		for i in range(nRows):
			for j in range(nCols):
				#print('(',i,j,')',end="")
				if i<nRows-1 and self.img[unitWidth*(i+1), unitWidth*j + unitWidth//2] == 255:
					self.adjList[i,j]+='D'
					self.adjList[i+1,j]+='U'
					if(save_search==True):
						ref_point=[unitWidth*(i+1), self.sepWidth + unitWidth*(j)]
						img[ref_point[0]:ref_point[0]+self.sepWidth, ref_point[1]:ref_point[1]+self.cellWidth] = [0, 255, 0]
				if j<nCols-1 and self.img[unitWidth*i + unitWidth//2, unitWidth*(j+1)] == 255:
					self.adjList[i,j]+='R'
					self.adjList[i,j+1]+='L'
					if(save_search==True):
						ref_point=[self.sepWidth + unitWidth*(i), unitWidth*(j+1)]
						img[ref_point[0]:ref_point[0]+self.cellWidth, ref_point[1]:ref_point[1]+self.sepWidth] = [0, 255, 0]
				
		print('Constructed Adjacency-List.',end='\n\n')
		
		if(save_search==True):
			cv.imwrite('plots/GraphasMaze.png',img)
		

	def search(self,curNode,discovered,file,img,save_search=True):
		if curNode==self.exit:
			cv.imshow('Solution',img)
			cv.waitKey(0)
			cv.destroyAllWindows()
			print('Found Solution-path.',end='\n\n')
			cv.imwrite('plots/solution.png', img)
			return True
	
		discovered[curNode[0],curNode[1]]=1
		for i in self.adjList[curNode[0],curNode[1]]:
			#print(curNode,end='')
			res=False
			if i=='L':
				if discovered[curNode[0],curNode[1]-1]==0:
					if save_search==True:
						unitWidth = self.sepWidth + self.cellWidth
						mid = self.sepWidth + self.cellWidth//2
						orig = img[curNode[0]*unitWidth + mid,
							(curNode[1]-1)*unitWidth + mid:curNode[1]*unitWidth + mid].copy()
						img[curNode[0]*unitWidth + mid,
							(curNode[1]-1)*unitWidth + mid:curNode[1]*unitWidth + mid] = [0,0,255]
						file.write(img)
					res=self.search([curNode[0],curNode[1]-1],discovered,file,img,save_search=True)
					if save_search==True and res==False:
						unitWidth = self.sepWidth + self.cellWidth
						mid = self.sepWidth + self.cellWidth//2
						img[curNode[0]*unitWidth + mid,
							(curNode[1]-1)*unitWidth + mid:curNode[1]*unitWidth + mid] = orig
						file.write(img)
			elif i=='R':
				if discovered[curNode[0],curNode[1]+1]==0:
					if save_search==True:
						unitWidth = self.sepWidth + self.cellWidth
						mid = self.sepWidth + self.cellWidth//2
						orig = img[curNode[0]*unitWidth + mid,
							curNode[1]*unitWidth + mid:(curNode[1]+1)*unitWidth + mid].copy()
						img[curNode[0]*unitWidth + mid,
							curNode[1]*unitWidth + mid:(curNode[1]+1)*unitWidth + mid] = [0,0,255]
						file.write(img)
					res=self.search([curNode[0],curNode[1]+1],discovered,file,img,save_search=True)
					if save_search==True and res==False:
						unitWidth = self.sepWidth + self.cellWidth
						mid = self.sepWidth + self.cellWidth//2
						img[curNode[0]*unitWidth + mid,
							curNode[1]*unitWidth + mid:(curNode[1]+1)*unitWidth + mid] = orig
						file.write(img)
					
			elif i=='U':
				if discovered[curNode[0]-1,curNode[1]]==0:
					if save_search==True:
						unitWidth = self.sepWidth + self.cellWidth
						mid = self.sepWidth + self.cellWidth//2
						orig = img[(curNode[0]-1)*unitWidth + mid:curNode[0]*unitWidth + mid,
							curNode[1]*unitWidth + mid].copy()
						img[(curNode[0]-1)*unitWidth + mid:curNode[0]*unitWidth + mid,
							curNode[1]*unitWidth + mid] = [0,0,255]
						file.write(img)
					res=self.search([curNode[0]-1,curNode[1]],discovered,file,img,save_search=True)
					if save_search==True and res==False:
						unitWidth = self.sepWidth + self.cellWidth
						mid = self.sepWidth + self.cellWidth//2
						img[(curNode[0]-1)*unitWidth + mid:curNode[0]*unitWidth + mid,
							curNode[1]*unitWidth + mid] = orig
						file.write(img)
					
			else:
				if discovered[curNode[0]+1, curNode[1]]==0:
					if save_search==True:
						unitWidth = self.sepWidth + self.cellWidth
						mid = self.sepWidth + self.cellWidth//2
						orig = img[curNode[0]*unitWidth + mid:(curNode[0]+1)*unitWidth + mid,
								curNode[1]*unitWidth + mid].copy()
						img[curNode[0]*unitWidth + mid:(curNode[0]+1)*unitWidth + mid,
							curNode[1]*unitWidth + mid] = [0,0,255]
						file.write(img)
					res=self.search([curNode[0]+1, curNode[1]],discovered,file,img,save_search=True)
					if save_search==True and res==False:
						unitWidth = self.sepWidth + self.cellWidth
						mid = self.sepWidth + self.cellWidth//2
						img[curNode[0]*unitWidth + mid:(curNode[0]+1)*unitWidth + mid,
							curNode[1]*unitWidth + mid] = orig
						file.write(img)
			if res==True:
				#print(i,end='')
				return res
			
		return False
