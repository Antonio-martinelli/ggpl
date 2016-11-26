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

def door(doorX,doorY,occurrency):

	def door0(dx,dy,dz):

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