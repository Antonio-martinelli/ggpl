from pyplasm import *
import csv
from ast import literal_eval as make_tuple

def intersperse(seq, value):
    """This function intersperse an input list with the input value. If the resultant list has odd length, another given value is appended
    intersperse is a function that, given a list and a value, intersperse the list with the value."""
    res = [value] * (2 * len(seq) - 1)
    res[::2] = seq
    if (len(res)%2 != 0):
        res.append(value)
    return res
 
def buildFrame(beamDimensions, pillarDimensions, pillarDistances, interstoryHeights):
    """This function returns an HPC model of a concrete space frame with given beam's and pillar's dimensions, 
    distances between the pillars, and interstories."""
 	
    pillarDistances = [0] + pillarDistances
    linearPillars = intersperse(pillarDistances, pillarDimensions[1])
    pillars3D = INSR(PROD)([QUOTE([pillarDimensions[0], -3]),QUOTE(linearPillars), QUOTE(intersperse([-interstory for interstory in interstoryHeights], -beamDimensions[1]))])
    horizontalBeamXYAxis = [pillarDimensions[0],-3]
    horizontalBeamYYAxis = intersperse([-beam for beam in pillarDistances], pillarDimensions[1])
    horizontalBeamYYAxis[0] = -horizontalBeamYYAxis[0]
    beamsY3D = INSR(PROD)([QUOTE(horizontalBeamXYAxis), QUOTE(horizontalBeamYYAxis), QUOTE(intersperse(interstoryHeights,beamDimensions[1]))])
    frameModel = STRUCT([pillars3D, beamsY3D])
    return frameModel

def buildBeams(file_name):
	"""This function returns the beams that connect the frames by reading the input file"""
	with open(file_name, 'rb') as file:
		reader = csv.reader(file, delimiter=';')
		beamlengthX = []
		fileValues = []
		rowAcc = 0
		for row in reader:
			rowAcc = rowAcc + 1
			fileValues.append(row)
			if(rowAcc == 2):
				if(float(fileValues[0][0]) == 0):
					beamlengthX.append(-(make_tuple(fileValues[1][1])[0]))
				else:
					beamlengthX.append(float(fileValues[0][0])-make_tuple(fileValues[1][1])[0])
					beamlengthX.append(-(make_tuple(fileValues[1][1])[0]))
				rowAcc = 0
				fileValues = []
	with open(file_name, 'rb') as file:
		reader = csv.reader(file, delimiter=';')
		beamlengthY = []
		beamlengthZ = []
		fileValues = []
		rowAcc = 0
		for row in reader:
			beamlengthY = []
			rowAcc += 1
			fileValues.append(row)
			if(rowAcc == 2):
				beamlengthZ = intersperse(make_tuple(row[3]), make_tuple(row[0])[1])
				beamlengthY.append(make_tuple(fileValues[1][1])[0])
				for element in make_tuple(fileValues[1][2]):
					beamlengthY.append(element)
					beamlengthY.append(make_tuple(fileValues[1][1])[0])
				rowAcc = 0
				fileValues = []
	return INSR(PROD)([QUOTE(beamlengthX), QUOTE(beamlengthY), QUOTE(beamlengthZ)])

 
def ggpl_bone_structure(file_name):
	"""This function takes in input a file_name string that is the path of a file that contains 3D coordinates and parameters for a planar frame
	and returns the VIEW of the STRUCT required."""
	with open(file_name, 'rb') as file:
		reader = csv.reader(file, delimiter = ';')
		finalModel = []
		xCoord = 0
		yCoord = 0 
		zCoord = 0
		fileValues = []
		rowAcc = 0
		for row in reader:
			rowAcc += 1
			fileValues.append(row)
			if(rowAcc == 2):
				beamlengthY = []
				xCoord += float(fileValues[0][0])
				yCoord += float(fileValues[0][1])
				zCoord += float(fileValues[0][2])
				frameModel = buildFrame(make_tuple(fileValues[1][0]), make_tuple(fileValues[1][1]), make_tuple(fileValues[1][2]), make_tuple(fileValues[1][3]))
				frameElement = STRUCT([T(1)(xCoord), T(2)(yCoord), T(3)(zCoord), frameModel])
				finalModel.append(STRUCT([frameElement]))
				rowAcc = 0
				fileValues = []
		finalModel.append(buildBeams(file_name))
		VIEW(STRUCT(finalModel))

 
ggpl_bone_structure("frame_data_461981.csv")