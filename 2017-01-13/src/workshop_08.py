from pyplasm import *
import csv

def build_ladder(fileLadder, xfactor, ladderBuilder):
	"""This function generates a ladder to insert in the multy storey house."""
	with open(fileLadder, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		ladderX = 0
		ladderY = 0
		minX = 1000000
		minY = 1000000
		for row in reader:
			if(minX > float(row[0])):
				minX = float(row[0])
			elif(minX > float(row[2])):
				minX = float(row[2])
			elif(minY > float(row[1])):
				minY = float(row[1])
			elif(minY > float(row[3])):
				minY = float(row[3])
			if(float(row[0]) == float(row[2])):
				ladderY = float(row[1]) - float(row[3])
			elif(float(row[1]) == float(row[3])):
				ladderX = float(row[0]) - float(row[2])
		if(ladderX < 0):
			ladderX = -ladderX
		elif(ladderY < 0):
			ladderY = -ladderY
		ladder = ladderBuilder.ggpl_single_stair(ladderX, ladderY, 3/xfactor)
		ladder = T([1,2])([minX, minY])(ladder)
		return ladder

def build_doors_and_windows(fileOpen, offset, xfactor, type, externalWalls, windowsFunction, doorsFunction): 
	"""This function generate a list of windows or doors according to the input type and the function passed."""
	with open(fileOpen, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		concreteList = []
		for row in reader:
			width = 0
			if(float(row[0]) == float(row[2])):
				width = float(row[3]) - float(row[1])
			if(float(row[1]) == float(row[3])):
				width = float(row[2]) - float(row[0])
			#add the cuboid offset.
			width = width + offset 
			if(type == "window"):
				objectConcrete = windowsFunction(width - offset, offset, (SIZE([3])(externalWalls)[0]/2.))
			elif(type == "door"):
				objectConcrete = doorsFunction(width - offset, offset, float(2.5/xfactor))
			if(float(row[0]) == float(row[2])):
				objectConcrete = R([1,2])(-PI/2.)(objectConcrete)
				objectConcrete = T([2])(width - offset)(objectConcrete)
			if(type == "window" and float(row[1]) == float(row[3])):
				objectConcrete = T([1,2,3])([float(row[0]), float(row[1]) + offset/2, (SIZE([3])(externalWalls)[0]/4.)])(objectConcrete)
			elif(type == "window" and float(row[0]) == float(row[2])):
				objectConcrete = T([1,2,3])([float(row[0]) + offset/2, float(row[1]), (SIZE([3])(externalWalls)[0]/4.)])(objectConcrete)
			elif(type == "door"):
				objectConcrete = T([1,2])([float(row[0]), float(row[1])])(objectConcrete)
			concreteList.append(objectConcrete)
		return concreteList

def generate_2D_walls(fileOpen):
	"""This function generates the STRUCT of the walls given a .lines file."""
	with open(fileOpen, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		listWalls = []
		for row in reader:
			listWalls.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
		listWalls = STRUCT(listWalls)
		return listWalls

def create_holes(linesFileName, offset):
	"""This function, given a .lines filename, returns the the STRUCT of a set of 3D models placed
	where we need to open an hole in the wall to insert doors and windows"""
	with open(linesFileName, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		holeModels = []
		for row in reader:
			lineModel = POLYLINE([[float(row[0]), float(row[1])], [float(row[2]), float(row[3])]])
			if (row[1] == row[3]):
				holeModel = OFFSET([0,offset*2])(lineModel)
				holeModel = T([2])([-offset/2.])(holeModel)
			else:
				holeModel = OFFSET([offset*2,0])(lineModel)
				holeModel = T([1])([-offset/2.])(holeModel)
			holeModels.append(holeModel)
	holeModels = STRUCT(holeModels)
	return holeModels

def ggpl_building_house(lines, windowsFunction, doorsFunction, ladderBuilder, floorNumber, totalNumberOfFloors, texture):
	"""This function generates the HPC Model represent the floorNumber floor of the storey structure."""
	wallOffset = 12

	#create external walls 
	externalWalls = generate_2D_walls(lines[0])

	#create floor
	floor = SOLIDIFY(externalWalls)
	floor = PROD([floor, Q(1)])

	#define scale factor
	xfactor = 15/SIZE([1])(externalWalls)[0]
	yfactor = 15.1/SIZE([2])(externalWalls)[0]

	#apply offset to external walls
	externalWalls = OFFSET([wallOffset,wallOffset])(externalWalls)
	externalWalls = PROD([externalWalls, Q(3/xfactor)])

	#create internal walls
	internalWalls = generate_2D_walls(lines[1])
	internalWalls = OFFSET([wallOffset,wallOffset])(internalWalls)
	internalWalls = PROD([internalWalls, Q(3/xfactor)])

	#remove the space of the ladder from second to the last floor	
	if(floorNumber != 0):
		with open(lines[4], "rb") as file:
			reader = csv.reader(file, delimiter=",")
			minX = 100000
			minY = 100000
			xValue = 0
			yValue = 0
			for row in reader:
				if(minX > float(row[0])):
					minX = float(row[0])
				elif(minX > float(row[2])):
					minX = float(row[2])
				elif(minY > float(row[1])):
					minY = float(row[1])
				elif(minY > float(row[3])):
					minY = float(row[3])
				if(float(row[0]) == float(row[2])):
					yValue = float(row[1]) - float(row[3])
				elif(float(row[1]) == float(row[3])):
					xValue = float(row[0]) - float(row[2])
				if(xValue<0):
					xValue = -xValue
				elif(yValue<0):
					yValue = -yValue
			
			diffCuboid = CUBOID([xValue, yValue, 10])
			diffCuboid = T([1,2])([minX, minY])(diffCuboid)
			floor = DIFFERENCE([floor,diffCuboid])

	#create cuboids to remove doors space.
	doors = create_holes(lines[2], 14)
	doors = PROD([doors, Q(2.5/xfactor)])

	#create cuboids to remove windows space
	windows = create_holes(lines[3], 14)
	windows = PROD([windows, Q(SIZE([3])(externalWalls)[0]/2.)])
	windows = T(3)(SIZE([3])(externalWalls)[0]/4.)(windows)
	
	externalWalls = DIFFERENCE([externalWalls, doors, windows])
	internalWalls = DIFFERENCE([internalWalls, externalWalls, doors, windows])
	externalWalls = TEXTURE(texture)(externalWalls)
	internalWalls = TEXTURE("textures/interiors.jpg")(internalWalls)
	frame = STRUCT([externalWalls, internalWalls])

	#insert the concrete doors
	doorsConcreteList = build_doors_and_windows(lines[2], wallOffset, xfactor, "door", externalWalls, windowsFunction, doorsFunction)
	doorsConcreteList = STRUCT(doorsConcreteList)
	#insert the concrete windows
	windowsConcreteList = build_doors_and_windows(lines[3], wallOffset, xfactor, "window", externalWalls, windowsFunction, doorsFunction)
	windowsConcreteList = STRUCT(windowsConcreteList)

	#insert the ladder
	if(floorNumber != totalNumberOfFloors):
		ladder = build_ladder(lines[5], xfactor, ladderBuilder)
		frame = STRUCT([frame, windowsConcreteList, doorsConcreteList, ladder])
	else:
		frame = STRUCT([frame, windowsConcreteList, doorsConcreteList])

	frame = T([3])((3/xfactor)*floorNumber)(frame)
	floor = T([3])((3/xfactor)*floorNumber)(floor)
	frame = (S([1,2,3])([xfactor,yfactor, xfactor])(frame))
	floor = (S([1,2,3])([xfactor,yfactor, xfactor])(floor))
	floor = TEXTURE("textures/floor.jpg")(floor)
	result = STRUCT([floor, frame])
	VIEW(result)
	return result
