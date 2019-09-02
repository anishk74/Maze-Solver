import cv2
import numpy as np

#global endFound
def dfs(s0,s1,adjList,e0,e1,discovered):
	global endFound
	global s
	if endFound==0:
		
		discovered[s0][s1]=1
		for i in adjList[s0][s1]:

			s+=i
			if i=='l':
				if s0==e0 and s1-1==e1:
					endFound=1
					return
				if discovered[s0][s1-1]==0:
					dfs(s0,s1-1,adjList,e0,e1,discovered)
					
			if i=='r':
				if s0==e0 and s1+1==e1:
					endFound=1
					return
				if discovered[s0][s1+1]==0:
					dfs(s0,s1+1,adjList,e0,e1,discovered)	
					
			if i=='u':
				if s0-1==e0 and s1==e1:
					endFound=1
					return
				
				if discovered[s0-1][s1]==0:
					dfs(s0-1,s1,adjList,e0,e1,discovered)
					
			if i=='d':
				if s0+1==e0 and s1==e1:
					endFound=1
					return
				if discovered[s0+1][s1]==0:
					dfs(s0+1,s1,adjList,e0,e1,discovered)
					
			if endFound==0:
				s=s[:-1]
			else:
				return
	

fileName=input("Enter the name of image file: ")
originalimage=cv2.imread(fileName)
img=cv2.imread(fileName,cv2.IMREAD_GRAYSCALE)
totalHeight,totalWidth=img.shape
l=[]
unitWidth=0
count=0
checkWhite=0
s0=0
s1=0
e0=0
e1=0

for i in range(totalWidth):
	if img[0,i]>=128:
		checkWhite=1
		break
if checkWhite==1:
	l.append([0,i])
	while img[0,i]>=128:
		i+=1
		unitWidth+=1
	count+=1
	l.append([0,i])



if count<2:
	checkWhite=0
	unitWidth=0
	for i in range(totalWidth):
		if img[totalHeight-1,i]>=128:
			checkWhite=1
			break
	if checkWhite==1:	
		l.append([totalHeight-1,i])
		while img[totalHeight-1,i]>=128:
			i+=1
			unitWidth+=1
		count+=1
		l.append([totalHeight-1,i])

if count<2:
	checkWhite=0
	unitWidth=0
	for i in range(totalHeight):
		if img[i,0]>=128:
			checkWhite=1
			break
	if checkWhite==1:
		l.append([i,0])
		while img[i,0]>=128:
			i+=1
			unitWidth+=1
		count+=1
		l.append([i,0])

if count<2:
	checkWhite=0
	unitWidth=0
	for i in range(totalHeight):
		if img[i,totalWidth-1]>=128:
			checkWhite=1
			break

	if checkWhite==1:
		l.append([i,totalWidth-1])
		while img[i,totalWidth-1]>=128:
			i+=1
			unitWidth+=1
		l.append([i,totalWidth-1])




i=0
cellWidth=unitWidth
seperatorWidth1=0
firstCell=unitWidth//2
while img[i,firstCell]<=128:
	seperatorWidth1+=1
	i+=1
seperatorWidth2=0
i=0
nextCell=unitWidth+unitWidth//2
while img[i,nextCell]<=128:
	seperatorWidth2+=1
	i+=1
seperatorWidth=max(seperatorWidth1,seperatorWidth2)

adjList=[]
rowpixel=seperatorWidth+cellWidth//2
columnpixel=seperatorWidth+cellWidth//2
unitWidth=cellWidth+seperatorWidth

#Calculating the start (s0,s1)
if l[0][0]==l[1][0]:
	if l[0][0]==0:
		s0=0
	else:
		l[0][0]-=unitWidth//2
		s0=l[0][0]//unitWidth
	l[1][1]-=unitWidth//2
	s1=l[1][1]//unitWidth
else:
	if l[0][1]==0:
		s1=0
		
	else:
		l[0][1]-=unitWidth//2
		s1=l[0][1]//unitWidth
	l[1][0]-=unitWidth//2
	s0=l[1][0]//unitWidth

#Calculating the end (e0,e1)
if l[2][0]==l[3][0]:
	if l[2][0]==0:
		e0=0
	else:
		l[2][0]-=unitWidth//2
		e0=l[2][0]//unitWidth
	l[3][1]-=unitWidth//2
	e1=l[3][1]//unitWidth
else:
	if l[2][1]==0:
		e1=0
		
	else:
		l[2][1]-=unitWidth//2
		e1=l[2][1]//unitWidth
	l[3][0]-=unitWidth//2
	e0=l[3][0]//unitWidth



nRows=totalHeight//(unitWidth)
nCols=totalWidth//(unitWidth)
discovered=[]
for i in range(nRows):
	adjList.append([])
	discovered.append([])
	for j in range(nCols):
		adjList[i].append("")
		discovered[i].append(0)

for i in range(nRows):
	for j in range(nCols):
		if columnpixel+unitWidth<totalWidth:
			flag=0
			for k in range(unitWidth):
				if img[rowpixel,columnpixel+k]<128:
					flag=1
					break
			if flag==0:
				adjList[i][j]+='r'
				adjList[i][j+1]+='l'

		if rowpixel+unitWidth<totalHeight:
			flag=0
			for k in range(unitWidth):
				if img[rowpixel+k,columnpixel]<128:
					flag=1
					break
			if flag==0:
				adjList[i][j]+='d'
				adjList[i+1][j]+='u'
		columnpixel+=unitWidth
	columnpixel=seperatorWidth+unitWidth//2
	rowpixel+=unitWidth

s=""
endFound=0
dfs(s0,s1,adjList,e0,e1,discovered)


rowpixel=s0*unitWidth+unitWidth//2
columnpixel=s1*unitWidth+unitWidth//2

for i in s:
	if i=='l':
		for k in range(unitWidth):
			originalimage[rowpixel,columnpixel]=[0,0,255]
			columnpixel-=1
	if i=='u':
		for k in range(unitWidth):
			originalimage[rowpixel,columnpixel]=[0,0,255]
			rowpixel-=1
	if i=='r':
		for k in range(unitWidth):
			originalimage[rowpixel,columnpixel]=[0,0,255]
			columnpixel+=1
	if i=='d':
		for k in range(unitWidth):
			originalimage[rowpixel,columnpixel]=[0,0,255]
			rowpixel+=1
cv2.imshow('Solution',originalimage)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('solution.png',originalimage)
print('Solution of the maze is saved as solution.png')