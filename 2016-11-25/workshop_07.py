from pyplasm import *

doorY = [.2,.18,.08,.18,.08,.18,.4,.18,.08,.18,.08,.18,.2]
doorX = [.2,.5,.2,1.8,.08,.18,.08,.18,.2]

doorOccurrency = [[True]*13,
					[True, False, True, False, True, False, True, False, True, False, True, False, True],
					[True]*13,
					[True, False, True, False, True, False, True, False, True, False, True, False, True],
					[True, False, True, False, True, True, True, True, True, False, True, False, True],
					[True, False, True, False, False, False, True, False, False, False, True, False, True],
					[True, False, True, True, True, True, True, True, True, True, True, False, True],
					[True, False, False, False, False, False, True, False, False, False, False, False, True],
					[True]*13]

windowY = [0.04,0.04,0.2,0.02,0.16,0.02,0.2,0.04,0.04]
windowX = [0.02,0.8,0.05,0.02,0.4,0.02,0.4,0.05,0.04]

windowOccurrency = [[True]*9,
					[True, False, False, False, False, False, False, False, True],
					[True]*9,
					[True]*9,
					[True, True, False, True, False, True, False, True, True],
					[True]*9,
					[True, True, False, True, False, True, False, True, True],
					[True]*9,
					[True]*9]

def resizeXY(X, Y, occurrency, dx, dz):
	"""This function takes in input X,Y,occurrency, two dimensions dx, dz and scales the values
	contained in X and Y, in such a way that only empty spaces are scaled and filled spaces are mantained fixed"""
	sumY = sum(Y) 
	sumX = sum(X)
	visitedY = [False]*len(Y)
	for y_index in range(len(Y)):
		update = True
		for x_index in range(len(X)):
			if(occurrency[x_index][y_index] == False):
				update = False 
		if(update):
			sumY = sumY - Y[y_index]
			sumX = sumX - X[y_index]
			dx = dx - X[y_index]
			dz = dz - Y[y_index]

	for x_index in range(len(X)):
		modifyX = False
		for y_index in range(len(Y)):
			if(occurrency[x_index][y_index] == False and visitedY[y_index] == False):
				Y[y_index] = (dz * Y[y_index])/sumY
				visitedY[y_index] = True
				modifyX = True
			if(occurrency[x_index][y_index] == False and visitedY[y_index] == True and not modifyX):
				modifyX = True
		if(modifyX):
			X[x_index] = (dx * X[x_index])/sumX


def window(windowX, windowY, occurrency):
	"""This function, given three array, X, Y and occurrency, return the HPC model of the window
	generated according to the three parameters. X and Y contain values of distances calculated on the previous 
	segment of the axis. Occurrency is a matrix containing booleans that map which cell is empty and which cell is filled. 
	The inner function is useful for 'scaling'"""
	def window0(dx, dy, dz):

		resizeXY(windowX,windowY,occurrency, dx, dz)

		model = []
		for xIndex in range(len(windowX)):
			yQuotes = []
			xSum = sum(windowX[:xIndex])
			for yIndex in range(len(windowY)):
				if(occurrency[xIndex][yIndex] == False):
					yQuotes.append(-windowY[yIndex])
				else:
					yQuotes.append(windowY[yIndex])
			model.append(PROD([QUOTE([-xSum, windowX[xIndex]]), QUOTE(yQuotes)]))

		result = STRUCT(model)
		result = MAP([S2,S3,S1])(PROD([result, Q(dy)]))
		windowFrame = STRUCT([result])
		windowFrame = TEXTURE(["iron.jpg"])(windowFrame)

		glass = CUBOID([SIZE([1])(result)[0]*0.98,0.001,SIZE([3])(result)[0]*0.95])
		glass = T([1,2,3])([dx*0.005, dy/2, 0.01])(glass)
		glass = TEXTURE(["glass2.jpg"])(glass) 

		window = STRUCT([windowFrame, glass])
		window = S([1,2,3])([dx/SIZE([1])(window)[0], dy/SIZE([2])(window)[0], dz/SIZE([3])(window)[0]])(window)
		
		return window

	return window0


def door(doorX, doorY, occurrency):
	"""This function takes in input three array, X, Y and occurrency and returns the HPC model of the door
	generated according to the three parameters. X and Y contain values of distances calculated on the previous 
	segment of the axis. Occurrency is a matrix containing booleans that map which cell is empty and which cell is filled. 
	The inner function is useful for scaling the resulting door by the three parameter dx, dy, dz."""
	def door0(dx, dy, dz):

		model = []

		for xIndex in range(len(doorX)):
			yQuotes = []
			xSum = sum(doorX[:xIndex])
			for yIndex in range(len(doorY)):
				if(occurrency[xIndex][yIndex] == False):
					yQuotes.append(-doorY[yIndex])
				else:
					yQuotes.append(doorY[yIndex])
			model.append(PROD([ QUOTE([-xSum, doorX[xIndex]]), QUOTE(yQuotes)]))

		res = PROD([STRUCT(model), Q(dy)])
		res = MAP([S2,S3,S1])(res)
		res = S([1,2,3])([dx/SIZE([1])(res)[0], dy/SIZE([2])(res)[0], dz/SIZE([3])(res)[0]]) (res)

		door = TEXTURE(["wood.jpg", True, False, 1, 1, 0, 1, 1])(STRUCT([res]))

		glass = CUBOID([SIZE([1])(res)[0]*0.94, 0.01, SIZE([3])(res)[0]*0.94])
		glass = T([1,2,3])([dx*0.003, dy/2, dz*0.005])(glass)
		glass = TEXTURE(["glass.jpg"])(glass)

		refiner = CUBOID([0.03, 0.01,dz])
		refiner = T([1,2])([dx/2,dy])(refiner)
		refiner = TEXTURE(["wood.jpg", True, False, 1, 1, 0, 1, 1])(refiner)

		handler1 = T(3)(.15)(CUBOID([.05,.02,.2]))
		handler2 = CUBOID([.05,.02,.05])
		handler3 = T([1,2])([.01,.02])(CUBOID([.03,.02,.2]))
		handler = TEXTURE("bronze.jpg")(STRUCT([handler3, handler2, handler1]))
		handler = T([1,2,3])([dx/2.-2*SIZE([1])(handler)[0],dy, dz/2.-1.5*SIZE([3])(handler)[0]])(handler)

		finalDoor = S([1,2,3])([dx/SIZE([1])(res)[0], dy/SIZE([2])(res)[0], dz/SIZE([3])(res)[0]]) (STRUCT([door, glass, refiner, handler]))

		return finalDoor

	return door0

VIEW(door(doorX, doorY, doorOccurrency)(2.2, .4, 2.8))
VIEW(window(windowX,windowY,windowOccurrency)(.6,.1,1.2))