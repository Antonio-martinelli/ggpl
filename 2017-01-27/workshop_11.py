import src.workshop_10 as house_generator
import src.workshop_09 as roof_generator
import src.workshop_08 as walls_generator
import src.workshop_07 as doors_and_windows_generator
import src.workshop_03 as stairs_generator
import csv
from random import randint
from pyplasm import *

lines = ["_externalWalls_", "_innerWalls_", "_doors_", "_windows_", "_ladders_"]

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

#first model
externalWallsFirstModel = walls_generator.generate_2D_walls("lines/first_model" + lines[0] + "1.lines")
xFactorFirstModel = 15/SIZE([1])(externalWallsFirstModel)[0]
yFactorFirstModel = 15.1/SIZE([2])(externalWallsFirstModel)[0]
zFactorFirstModel = xFactorFirstModel

#second model
externalWallsSecondModel = walls_generator.generate_2D_walls("lines/second_model" + lines[0] + "1.lines")
xFactorSecondModel = 15/SIZE([1])(externalWallsSecondModel)[0]
yFactorSecondModel = 15.1/SIZE([2])(externalWallsSecondModel)[0]
zFactorSecondModel = xFactorSecondModel

def generate_straight_street(streetLength, streetWidth, streetHeight, rotation, transX, transY):
	"""This function generates a CUBOID with input dimensions streetLength, streetWidth, streetHeight, 
	then applies a rotation of rotation degrees and translate it of transX, transY meters."""
	street = CUBOID([streetLength, streetWidth, streetHeight])
	street = R([1,2])(rotation)(street)
	street = T([1,2])([transX, transY])(street)
	return street

def generate_sidewalker(street):
	"""This helper generate sidewalkers for the input street by adding OFFSETs to it and leaving non coloured."""
	leftSidewalker = OFFSET([0.75,0.75])(street)
	leftSidewalker = S([3])([SIZE([3])(street)[0]/2])(leftSidewalker)
	rightSidewalker = OFFSET([-0.75,-0.75])(street)
	rightSidewalker = S([3])([SIZE([3])(street)[0]/2])(rightSidewalker)
	return STRUCT([leftSidewalker, rightSidewalker])

def generate_house(modelNumber, dx, dy, dz, rotation, transX, transY):
	"""This function is used to create the HPC model of an house according to the modelNumber in input 
	(it can be only 1 or 2 as we have only 2 models). The house is scaled to dx x dy x dz dimensions and then 
	is rotated by rotation degrees and translated of transX and transY meters."""
	if (modelNumber == 1):
		house = house_generator.multi_storey_house(2, "first_model", xFactorFirstModel, yFactorFirstModel, zFactorFirstModel, "textures/roof_")([windowX,windowY,windowOccurrency], [doorX,doorY,doorOccurrency])(lines, PI/5., 3/zFactorFirstModel, "textures/exteriors_")
	elif (modelNumber == 2):
		house = house_generator.multi_storey_house(3, "second_model", xFactorSecondModel, yFactorSecondModel, zFactorSecondModel, "textures/roof_")([windowX,windowY,windowOccurrency], [doorX,doorY,doorOccurrency])(lines, PI/5., 3/zFactorSecondModel, "textures/exteriors_")
	house = S([1,2,3])([dx/SIZE([1])(house)[0],dy/SIZE([2])(house)[0],dz/SIZE([3])(house)[0]])(house)
	house = R([1,2])(rotation)(house)
	house = T([1,2,3])([transX, transY, 0.1])(house)
	return house

def ggpl_suburban_neighborhood():
	"""This function generates a realistic suburban neighborhood inspired by a 60x45 meters image 
consisting in streets and houses. The function returns the VIEW of the model generated."""
	base = CUBOID([62, 47, -5])
	base = MATERIAL([.05,.05,.05,.05,  .4,.2,0,1,  0,0,0,0, 0,0,0,1, 100])(base)
	grass = CUBOID([60,45,0.1])
	grass = MATERIAL([0,0,0,1,  0,.1,0,1,  0,.1,0,1, 0,0,0,1, 0])(grass)
	streetsHeight = .5
	streetsWidth = 4
	curveStreetsWidth = streetsWidth - 0.7

	meterX = CUBOID([0.1,100,1])
	meterY = CUBOID([100, 0.1,1])
	meterX = T([1])(15)(meterX)
	meterY = T([2])(30)(meterY)

	straightStreet_1 = generate_straight_street(15.5, streetsWidth, streetsHeight, -PI/3.5, -3, 26)
	straightStreet_2 = generate_straight_street(15, streetsWidth, streetsHeight, -PI/8, 47, 7)
	straightStreet_3 = generate_straight_street(15, streetsWidth, streetsHeight, 0, 22, 30)
	straightStreet_4 = generate_straight_street(8, streetsWidth -1, streetsHeight, PI/4, 9.5, 20)

	curveStreet_1 = MAP(BEZIERCURVE([[9.5, 16], [15, 13], [27, 10], [35,11], [41, 12], [45,11], [50, 8.5]]))(INTERVALS(1)(32))
	curveStreet_1 = OFFSET([curveStreetsWidth, curveStreetsWidth])(curveStreet_1)
	curveStreet_1 = T([1,2])([-3.1,-1.9])(curveStreet_1)
	curveStreet_1 = PROD([curveStreet_1, Q(streetsHeight)])

	curveStreet_2 = MAP(BEZIERCURVE([[50,8.3], [49,9], [47, 12], [49,18], [47,19], 
		[47,20],[46,22], [45,24], [44,26],[43,28], [41,31], [39,32.5], [36,32.6]]))(INTERVALS(1)(32))
	curveStreet_2 = OFFSET([curveStreetsWidth, curveStreetsWidth])(curveStreet_2)
	curveStreet_2 = T([1,2])([-2,-2])(curveStreet_2)
	curveStreet_2 = PROD([curveStreet_2, Q(streetsHeight)])

	curveStreet_3 = MAP(BEZIERCURVE([[22,32],[21,31.5], [20,31], [20,30.5]]))(INTERVALS(1)(32))
	curveStreet_3 = OFFSET([curveStreetsWidth, curveStreetsWidth])(curveStreet_3)
	curveStreet_3 = T([1,2])([-2,-1.5])(curveStreet_3)
	curveStreet_3 = PROD([curveStreet_3, Q(streetsHeight)])

	rotary = CYLINDER([5, streetsHeight])(100)
	rotary_center = CYLINDER([1, streetsHeight])(100)
	rotary = DIFFERENCE([rotary, rotary_center])
	rotary = T([1,2])([16,29])(rotary)

	#generating houses
	house_1 = generate_house(1, 6,6,6, PI/4, 7,22)
	house_2 = generate_house(2, 8,8,8, PI/2.3, 24,14)
	house_3 = generate_house(2, 8,14,8, PI/2, 43,13)
	house_4 = generate_house(2, 8,13,8, PI/16, 51,9)
	house_5 = generate_house(1, 8,8,6, PI/6, 48, 24)
	house_6 = generate_house(1, 8,8,6, -PI/6, 36.5, 36.5)			
	house_7 = generate_house(2, 8,14,8, PI/2, 37, 35)
	house_8 = generate_house(2, 8,8,8, PI/1.35, 16, 36)

	#adding sidewalkers
	straightStreet_1_sidewalker = generate_sidewalker(straightStreet_1)
	straightStreet_2_sidewalker = generate_sidewalker(straightStreet_2)
	straightStreet_3_sidewalker = generate_sidewalker(straightStreet_3)
	curveStreet_1_sidewalker = generate_sidewalker(curveStreet_1)
	curveStreet_2_sidewalker = generate_sidewalker(curveStreet_2)
	curveStreet_3_sidewalker = generate_sidewalker(curveStreet_3)

	#cleaning borders
	cleanerLeftBorder = CUBOID([-5, 30, streetsHeight])
	cleanerRightBorder = CUBOID([5, 10, streetsHeight])
	cleanerRightBorder = T([1])([60])(cleanerRightBorder)
	straightStreet_1 = DIFFERENCE([straightStreet_1, cleanerLeftBorder])
	straightStreet_1_sidewalker = DIFFERENCE([straightStreet_1_sidewalker, cleanerLeftBorder])
	straightStreet_2 = DIFFERENCE([straightStreet_2, cleanerRightBorder])
	straightStreet_2_sidewalker = DIFFERENCE([straightStreet_2_sidewalker, cleanerRightBorder])

	#assembling
	streets = STRUCT([straightStreet_1, straightStreet_2, straightStreet_3, straightStreet_4, curveStreet_1, curveStreet_2, curveStreet_3, rotary])
	sidewalkers = STRUCT([straightStreet_1_sidewalker, straightStreet_2_sidewalker, straightStreet_3_sidewalker, curveStreet_1_sidewalker, curveStreet_2_sidewalker, curveStreet_3_sidewalker])
	streets = MATERIAL([.1,.1,.1,.2,  0,0,0,1,  0,0,0,1, 0,0,0,1, 10])(streets)
	houses = STRUCT([house_1, house_2, house_3, house_4, house_5, house_6, house_7, house_8])
	model = STRUCT([streets, grass, sidewalkers, houses])
	model = T([1,2])([1,1])(model)
	VIEW(STRUCT([model, base]))

ggpl_suburban_neighborhood()