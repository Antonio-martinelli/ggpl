from larlib import *
from pyplasm import *

def generate_segment(p1, p2):
	line = POLYLINE([[p1[0],p1[1],p1[2]],[p2[0],p2[1], p2[2]]])
	lineDirection = [p1[0] - p2[0], p1[1] - p1[1], p1[2] - p2[2]]
	return line

def ggpl_generate_structure(segments, angle):
	model = []
	for segment in segments:
		model.append(generate_segment(segment[0],segment[1]))
	VIEW(STRUCT(model))

p1 = (1.,1.,0.)
p2 = (1.,5.,0.)
p3 = (3.,5.,0.)
p4 = (3.,1.,0.)
segments = [[p1,p2], [p2,p3], [p3,p4], [p4,p1]]

ggpl_generate_structure(segments, 90)