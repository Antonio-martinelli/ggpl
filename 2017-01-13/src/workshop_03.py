from pyplasm import *
import math

def generate_steps(stepNumber, tread, riser, stepWidth):
	"""This function, given a stepNumber representing the number of the step, tread representing the depth of the step, 
	riser representing the height of the step and stepWidth that represents the width of the step, return a list of steps."""
	step2d = MKPOL([[[tread, 0],[tread, riser*2], [tread*2, riser*2], [tread*2, riser]], [[1,2,3,4]], None])
	steps = []
	firstStep = CUBOID([tread, riser, stepWidth])
	steps.append(firstStep)
	for i in range(int(stepNumber-1)):
		steps.append(T([1,2])([(tread*i), riser*i])(PROD([step2d, Q(stepWidth)])))
	return steps

def ggpl_single_stair(dx, dy, dz):
	"""This function generate am HPC model of a simple stair given dx, dy, dz that represent the X, Y and Z value of the box that contain the stairs."""
	riser = dz/20.
	stepNumber = 20
	if(dx > dy):
		firstTread = dx / (stepNumber)
		stepWidth = dy
	else:
		firstTread = dy / (stepNumber)
		stepWidth = dx
	stairs = generate_steps(stepNumber, firstTread, riser, stepWidth)
	quarterTurnStairs = MAP([S1,S3,S2])(STRUCT(stairs))
	quarterTurnStairs = COLOR(Color4f([193/255., 154/255., 107/255., 1]))(quarterTurnStairs)
	return quarterTurnStairs