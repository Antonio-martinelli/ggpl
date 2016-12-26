from pyplasm import *
from sympy import *
import numpy as np

def list_to_coupled_list(startList):
	"""This function, given a starting list, returns a list containing, for every element in the 
    starting list, a couple (list) made by the original element and its successor. If the original element
    is the last of the original list, the first element of the original list is used as successor"""
	coupledList = []
	for index in range(len(startList)-1):
		coupledList.append([startList[index],startList[index+1]])
	coupledList.append([startList[-1], startList[0]])
	return coupledList

def plane_from_segment(angle, line):
	"""This function, given an angle and a line, returns the 4 coefficients that describe a plane passing
    by the line and has angle angulation."""
	partialPlane = PROD([POLYLINE(line), QUOTE([2])])
	partialPlane = T([1,2])([-line[0][0], -line[0][1]])(partialPlane)
	partialPlane = ROTN([-angle, [line[1][0] - line[0][0], line[1][1]-line[0][1],0]])(partialPlane)
	partialPlane = T([1,2])([+line[0][0], +line[0][1]])(partialPlane)

	points = []
	points.append(UKPOL(partialPlane)[0][0])
	points.append(UKPOL(partialPlane)[0][1])
	points.append(UKPOL(partialPlane)[0][2])

	x1 = points[0][0]
	x2 = points[1][0]
	x3 = points[2][0]
	y1 = points[0][1]
	y2 = points[1][1]
	y3 = points[2][1]
	z1 = points[0][2]
	z2 = points[1][2]
	z3 = points[2][2]

	p1 = np.array([x1, y1, z1])
	p2 = np.array([x2, y2, z2])
	p3 = np.array([x3, y3, z3])

	v1 = p3 - p1
	v2 = p2 - p1

	cp = np.cross(v1, v2)
	a, b, c = cp
	d = np.dot(cp, p3)
	return [a,b,c,d]

def ggpl_generate_structure(segments, angle, roofHeight):
	"""This function takes in input a list of vertices, an angle and an height, 
	and returns the VIEW of an HPC model of a roof."""
	lines = list_to_coupled_list(segments)
	planes = []
	for line in lines:
		planes.append(plane_from_segment(angle, line))
	couplePlanes = list_to_coupled_list(planes)

	roofTop = []
	linesEquations = []
	for couple in couplePlanes:
		x, y, z = symbols('x y z')
		solved = solve([Eq(couple[0][0]*x+couple[0][1]*y+couple[0][2]*z, couple[0][3]),
			Eq(couple[1][0]*x+couple[1][1]*y+couple[1][2]*z, couple[1][3])])
		linesEquations.append(solved)
		roofTop.append([round(float(solved[x].subs(z,roofHeight)),2), round(float(solved[y].subs(z,roofHeight)),2)])
	roofTop.append(roofTop[0])

	coupleLines = list_to_coupled_list(linesEquations)
	roofPitch = []

	for couple in coupleLines:
		firstBasePoint = [round(float((couple[0])[x].subs(z,0)),2),round(float((couple[0])[y].subs(z,0)),2),0]
		secondBasePoint = [round(float((couple[1])[x].subs(z,0)),2),round(float((couple[1])[y].subs(z,0)),2),0]
		firstTopPoint = [round(float((couple[0])[x].subs(z,roofHeight)),2),round(float((couple[0])[y].subs(z,roofHeight)),2),roofHeight]
		secondTopPoint = [round(float((couple[1])[x].subs(z,roofHeight)),2),round(float((couple[1])[y].subs(z,roofHeight)),2),roofHeight]
		points = [firstBasePoint, secondBasePoint, secondTopPoint, firstTopPoint, firstBasePoint]
		faces = [[1,2,3,4]]
		roofPitch.append(TEXTURE("roof.jpg")(MKPOL([points, faces, 1])))

	roofPitch = STRUCT(roofPitch)
	roofBase = SOLIDIFY(POLYLINE(segments + [segments[0]]))
	terrace = T([3])([roofHeight])(SOLIDIFY(POLYLINE(roofTop)))

	return VIEW(STRUCT([TEXTURE("surface.jpg")(terrace), roofBase, roofPitch]))

#First exec
"""
p1 = [0,0]
p2 = [4,0]
p3 = [4,4]
p4 = [0,4]
segments = [p1, p2, p3, p4]
angle = PI/4.
roofHeight = 1
"""
#Second exec
v1 = [0,0] 
v2 = [6,0] 
v3 = [6,6] 
v4 = [3,6] 
v5 = [3,3]  
v6 = [0,3]
segments = [v1, v2, v3, v4, v5, v6]
angle = PI/6.
roofHeight = 1.5
ggpl_generate_structure(segments, angle, roofHeight)