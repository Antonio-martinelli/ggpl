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

def multi_storey_house(nFloors, modelString, xFactor, yFactor, zFactor, roofTexture):
	"""multi_storey_house is a function that returns the function that calculates the model of the house."""
	def build_windows_and_doors(window, door):
		""""This function accepts the list of data structures to generate the windows"""
		def build_floors(lines, angle, height, exteriorTexture):
			"""This function gets in input the .lines filepath, the angle of the roof and its height and returns a VIEW
			of the resulting model"""
			all_floor = []
			with open("lines/" + modelString + "_externalWalls_1.lines") as file:
				reader = csv.reader(file, delimiter=",")
				new_verts = []
				for row in reader:
					new_verts.append([float(row[0]), float(row[1])])
				if (modelString == "second_model"):
					roofModel = roof_generator.ggpl_generate_structure(list(reversed(new_verts)), angle, height, roofTexture)
				else:
					roofModel = roof_generator.ggpl_generate_structure(new_verts, angle, height, roofTexture)
				roofModel = T([3])([nFloors*3/zFactor])(roofModel)
				roofModel = S([1,2,3])([xFactor*1.09, yFactor*1.09, zFactor])(roofModel)
				roofModel = T([1,2])([-SIZE([1])(roofModel)[0]*0.05, -SIZE([2])(roofModel)[0]*0.05])(roofModel)

			exteriorTexture = exteriorTexture + str(randint(1,3)) +".jpg"
			for i in range(nFloors):
				floor_lines = ["lines/"+modelString + lines[0] + str(i+1) + '.lines', "lines/" + modelString + lines[1] + str(i+1) + '.lines', 
				"lines/" + modelString + lines[2] + str(i+1) + '.lines', "lines/" + modelString + lines[3] + str(i+1) + '.lines', 
				"lines/" + modelString + lines[4] + str(i) + '.lines', "lines/" + modelString + lines[4] + str(i+1) + '.lines']
				floor = walls_generator.ggpl_building_house(floor_lines, 
					doors_and_windows_generator.window(window[0], window[1], window[2]), 
					doors_and_windows_generator.door(door[0], door[1], door[2]), 
					stairs_generator, i, nFloors-1, exteriorTexture)
				all_floor.append(floor)
				
			all_floor = STRUCT(all_floor)
			return VIEW(STRUCT([all_floor, roofModel]))
		return build_floors
	return build_windows_and_doors

multi_storey_house(2, "first_model", xFactorFirstModel, yFactorFirstModel, zFactorFirstModel, "textures/roof_")([windowX,windowY,windowOccurrency], [doorX,doorY,doorOccurrency])(lines, PI/5., 3/zFactorFirstModel, "textures/exteriors_")
#multi_storey_house(3, "second_model", xFactorSecondModel, yFactorSecondModel, zFactorSecondModel, "textures/roof_")([windowX,windowY,windowOccurrency], [doorX,doorY,doorOccurrency])(lines, PI/5., 3/zFactorSecondModel, "textures/exteriors_")
