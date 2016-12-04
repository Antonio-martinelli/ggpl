from pyplasm import *
from larlib import *
from random import randint
import os.path
import csv

def generate_2D_walls(linesFileName):
	"""This function takes in input a .lines filename and returns the 2D HPC model of a set of walls"""
	with open("lines/"+linesFileName +  ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		polylineList = []
		for row in reader:
			polylineList.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
	wall = STRUCT(polylineList)
	return wall


def create_holes(linesFileName):
	"""This function, given a .lines filename, returns the 2D HPC model of a set of rectangles, placed
	where we need to open an hole in the wall to insert doors and windows"""
	with open("lines/"+ linesFileName + ".lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		holeModels = []
		poly = []
		acc = 0
		for row in reader:
			acc = acc + 1
			poly.append([float(row[0]),float(row[1])])
			if(acc == 4):
				holeModels.append(MKPOL([poly,[[1,2,3,4]],None]))
				poly = []
				acc = 0
	holeModels = STRUCT(holeModels)
	return holeModels


def texturize_floors():
	"""This function returns a list of HPC models, in particular models of the different floors that are 
	present in the building, including the external floors, adding to them also a randomly picked texture from a
	specified set for each type of room"""
	res = []
	def build_floor(roomType):
		counter = 1
		result = []
		while True:
			if os.path.isfile("lines/" + roomType + str(counter) + ".lines"):
				with open("lines/" + roomType+str(counter)+".lines", "rb") as file:
					reader = csv.reader(file, delimiter=",")
					polylineList = []
					for row in reader:
						polylineList.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
				result.append(TEXTURE("textures/" + roomType+str(randint(1,4))+".jpg")(SOLIDIFY(STRUCT(polylineList))))
				counter = counter + 1
			else: 
				counter = 1
				break
		return result
	res = res + build_floor("bedroom")
	res = res + build_floor("bathroom")
	res = res + build_floor("livingroom")
	res = res + build_floor("terrace")
	return res


def build_house():
	"""This function generates all house's walls and floors. It takes no argument, due to the fact
	that it's parameterized thanks to the data files used in its body. This function also applies a scaling factor in order 
	to transform the units of measure used in inkscape (pixels) into meters, to have a more realistic render."""
	externalWalls = generate_2D_walls("externalWalls")

	xScale = 15/SIZE([1])(externalWalls)[0]
	yScale = 15.1/SIZE([2])(externalWalls)[0]
	zScale = xScale
	outerWallOffset = 12
	innerWallOffset = 7
	terraceWallOffset = 5

	#building walls
	walls = OFFSET([outerWallOffset, outerWallOffset])(externalWalls)
	walls = PROD([walls, Q(3/zScale)])
	innerWalls = generate_2D_walls("innerWalls")
	innerWalls = OFFSET([innerWallOffset, innerWallOffset])(innerWalls)
	innerWalls = PROD([innerWalls, Q(3/zScale)])
	terraceWalls = generate_2D_walls("terraceWalls")
	terraceWalls = OFFSET([terraceWallOffset, terraceWallOffset])(terraceWalls)
	terraceWalls = PROD([terraceWalls, Q(1.5/zScale)])
	terraceWalls = TEXTURE(["textures/terraceWalls.jpg",True,True,10,10,PI/2.,20,20,10,10])(terraceWalls)

	#generating holes in walls
	doors = create_holes("doors")
	doors = PROD([doors, Q(2.5/zScale)])
	windows = create_holes("windows")
	windows = PROD([windows, Q(SIZE([3])(walls)[0]/2.)])
	windows = T(3)(SIZE([3])(walls)[0]/4.)(windows)

	#removing holes from walls
	exteriors = DIFFERENCE([walls, windows, doors])
	interiors = DIFFERENCE([innerWalls, doors, windows])

	#adding textures to the walls and floor
	exteriors = TEXTURE(["textures/exteriors.jpg",True,True,10,10,PI/2.,20,20,10,10])(exteriors)
	interiors = TEXTURE(["textures/interiors.jpg",True,True,1,1,PI/2.,5,5])(interiors)
	floor = STRUCT(texturize_floors())

	house = S([1,2,3])([xScale,yScale, zScale])(STRUCT([interiors, exteriors, terraceWalls, floor]))

	return house

VIEW(build_house())