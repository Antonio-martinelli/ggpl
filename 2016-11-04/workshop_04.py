from pyplasm import *
import numpy

def round_vertices(verts):
	"""This function round the coordinates of a given list of vertices: if the vertex has a coordinate 
		smaller than 0.001 it will be rounded to 0, alternatively it will be rounded to the first decimal.
	"""
	for i in range(len(verts)):
		for j in range(len(verts[i])):
			if(abs(verts[i][j]) < 0.001):
				verts[i][j] = 0
			else:
				verts[i][j] = round(verts[i][j],1)

def compute_incident_faces(listUkpol):
	"""This function takes in input the result of UKPOL() function and 
		returns a dictionary that has keyvalue as the coordinates of a vertex and 
		as value a list of the cells incident in that point
	"""
	dictionary = {}
	verts = listUkpol[0]
	round_vertices(verts)
	cells = listUkpol[1]
	for cell in cells:
		for elem in cell:
			point = str(verts[int(elem)-1])
			if(point not in dictionary):
				dictionary[point] = []
			dictionary[point].append(elem)
	return dictionary

def check_complanarity(verts, cells):
	"""This function takes a list of vertices and a list of cells
	   in input and return True if all the cells are complanar, False elsewhere"""
	round_vertices(verts)
	for cell in cells:
		if(len(cell) > 3):
			matrix = []
			lastPoint = cell[-1]
			for elem in cell:
				point = verts[int(elem)-1]
				row = []
				for i in range(len(point)):
					row.append(point[i]-verts[lastPoint-1][i])
				matrix.append(row)
			A = numpy.matrix(matrix)
			dim = numpy.linalg.matrix_rank(A)
			if(dim > 2):
				return False
	return True

def clean_cells(cells, verts):
	"""This function takes in input a list of vertices and a list of cells and returns the cells from the former list that doesn't remains
	   with coordinate z = 0"""
	cleaned = []
	for i in range(len(cells)-1):
		isBaseCell = True
		for pointIndex in cells[i]:
			print "point: " + str(pointIndex)
			if(verts[pointIndex-1][2] != 0):
				isBaseCell = False
		if(not isBaseCell):
			cleaned.append(cells[i])
	return cleaned


def ggpl_L_and_U_roof_builder(verts, cells):
	"""This function takes in input a list of vertices and a list of
		cells and returns an HPC model of an L/U roof and its frame."""
	frameOffset = 0.1
	if(not check_complanarity(verts, cells)):
		return None
	roofModel = MKPOL([verts,cells, None])
	cleanedCells = clean_cells(cells,verts)

	roof = MKPOL([verts, cleanedCells, None])
	roof = OFFSET([frameOffset, frameOffset, frameOffset])(roof)
	roof = T([3])([frameOffset])(roof)
	roof = COLOR(Color4f([68/255., 85/255., 51/255.,1]))(roof)

	roofFrame = OFFSET([.1,.1,.1])(SKEL_1(roofModel))
	roofFrame = S([3])(.95)(roofFrame)
	roofFrame = COLOR(Color4f([48/255., 28/255., 24/255.,1]))(roofFrame)

	return STRUCT([roof,roofFrame])

#first execution
verts1 = [[0,0,0],[9,0,0],[9,7,0],[6,7,0],[6,4,0],[0,4,0],[2,2,2],[7.5,2,2],[7.5,5.5,2]]
cells1 = [[1,7,6],[1,2,8,7],[2,3,9,8],[3,9,4],[4,9,8,5],[5,8,7,6],[6,5,2,1],[2,5,4,3]]

#second execution
verts2 = [[0,0,0],[3,0,0],[3,6,0],[8,6,0],[8,4,0],[10,4,0],[10,9,0],[0,9,0],[1.5,1.5,2],[1.5,7.5,2],[9,7.5,2],[9,5,2]]
cells2 = [[1,2,9],[2,3,10,9],[3,4,11,10],[4,5,12,11],[5,6,12],[6,7,11,12],[7,8,10,11],[8,1,9,10],[1,2,3,8],[3,4,7,8],[4,5,6,7]]

VIEW(ggpl_L_and_U_roof_builder(verts1, cells1))
VIEW(ggpl_L_and_U_roof_builder(verts2, cells2))
