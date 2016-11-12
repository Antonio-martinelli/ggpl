from pyplasm import *
import random

def ggpl_children_table(dx,dy,dz):
	"""This function takes in input three dimensions dx, dy, dz
    and returns a VIEW of a children table with randomly generated colours"""
	structure = []
	tableThickness = .05
	chairThickness = .02
	supportDiameter = .03
	chairSeat = .175
	structureColor = Color4f([184/255., 186/255., 186/255., 1])
	seatHeight = (dz - tableThickness - chairThickness - supportDiameter)/2.
	seat = CYLINDER([chairSeat,chairThickness])(100)
	box = SKEL_1(CUBOID([dx,dy,dz]))
	box = T([1,2])([-dx/2.,-dy/2.])(box)
	structure.append(box)
	
	table = CYLINDER([dx/2. - chairSeat, tableThickness])(100)
	table = T([3])([dz - tableThickness])(table)
	table = COLOR(Color4f([38/255.,226/255.,189/255.,1]))(table)
	structure.append(table)

	traslations = [(COS(2*PI/16*x) * (dx - 2*chairSeat)/2. , SIN(2*PI/16*x) * (dx - 2*chairSeat)/2. ) for x in range(0,16+1)][::2]
	
	chairSupport = CYLINDER([.03, seatHeight + supportDiameter])(100)
	chairSupport = COLOR(structureColor)(chairSupport)
	
	mainSupport = CYLINDER([.15, dz - tableThickness])(100)
	mainSupport = COLOR(structureColor)(mainSupport)
	structure.append(mainSupport)	
	support = CYLINDER([supportDiameter/2., dx/2. - 2*chairSeat/2.])(100)
	support = MAP([S3,S2,S1])(support)
	support = T([3])(seatHeight/2.)(support)
	support = COLOR(structureColor)(support)
	supports = [support, R([1,2])(2*PI/8.)]*8
	structure = structure + supports

	for elem in traslations:
		temp = T([1,2,3])([elem[0],elem[1],seatHeight + supportDiameter])(seat)
		structure.append(COLOR(Color4f([random.random()*255/255.,random.random()*255/255.,random.random()*255/255.,1]))(temp))
		structure.append(T([1,2])([elem[0],elem[1]])(chairSupport))
	
	VIEW(STRUCT(structure))

def ggpl_teacher_desk(dx, dy, dz):
	"""This function, with three dimensions dx, dy and dz as inputs, 
	returns a VIEW of a simple teacher desk."""
	desk = []
	footRadius = .05
	deskThickness = .03
	supportOffset = dx/30
	knobRadius = .02
	box = SKEL_1(CUBOID([dx,dy,dz]))
	desk.append(box)
	
	feetModel = [[0 + footRadius + supportOffset,0 + footRadius + supportOffset],[dx - footRadius - supportOffset,0 + footRadius + supportOffset], 
	[dx - footRadius - supportOffset, dy - footRadius -supportOffset], [0 + footRadius + supportOffset, dy - footRadius - supportOffset]]
	for footModel in feetModel:
		foot = CYLINDER([footRadius, dz - deskThickness])(100)
		foot = T([1,2])([footModel[0],footModel[1]])(foot)
		desk.append(foot)

	deskPlane = CUBOID([dx, dy, deskThickness])
	deskPlane = T([3])(dz- deskThickness)(deskPlane)
	deskPlane = COLOR(Color4f([229/255., 217/255., 203/255., 1]))(deskPlane)
	desk.append(deskPlane)

	firstDeskSupport = CUBOID([dx - 2*supportOffset - 2* footRadius, footRadius, 2*deskThickness])
	deskFirstSupport = T([1,2,3])([supportOffset+footRadius/2., supportOffset + footRadius/2., dz - 3*deskThickness])(firstDeskSupport)
	firstDeskSupports = [deskFirstSupport, T([1,2,3])([supportOffset+footRadius/2., dy-SIZE([2])(firstDeskSupport)[0]-supportOffset-footRadius/2, dz - 3*deskThickness])(firstDeskSupport)]

	secondDeskSupport =  CUBOID([footRadius, dy - 2*supportOffset - 2*footRadius, 2*deskThickness])
	secondDeskFirstSupport = T([1,2,3])([supportOffset + footRadius/2, supportOffset + footRadius/2, dz - 3*deskThickness])(secondDeskSupport)
	secondDeskSupports = [secondDeskFirstSupport, T([1,2,3])([dx - SIZE([1])(secondDeskSupport)[0]-supportOffset-footRadius/2 ,supportOffset + footRadius/2, dz - 3*deskThickness])(secondDeskSupport)]

	drawer = CUBOID([dx/3-supportOffset-2*footRadius, dy/2., dz/10 + footRadius])
	drawer = T([1,2,3])([supportOffset + 2*footRadius, 2*supportOffset + footRadius, dz - deskThickness - 2*deskThickness - dz/10])(drawer)
	drawerWall = CUBOID([dx/3-supportOffset-2*footRadius, footRadius, dz/10])
	drawerWall = T([1,2,3])([supportOffset + 2*footRadius, 2*supportOffset, dz - deskThickness - 2*deskThickness - dz/10])(drawerWall)
	drawerWall = COLOR(Color4f([187/255., 127/255., 65/255., 1]))(drawerWall)

	knob = SPHERE(knobRadius)([40,40])
	knob = JOIN(SKEL_1(knob))
	knob = COLOR(Color4f([255/255., 215/255., 0/255., 1]))(knob)
	knob = T([1,2,3])([supportOffset + 2*footRadius + SIZE([1])(drawerWall)[0]/2, supportOffset + footRadius*.65, dz - deskThickness - 2*deskThickness - SIZE([3])(drawerWall)[0]/2])(knob)
	drawers = [drawer, drawerWall, knob, T([1])([dx - 2*supportOffset - 4*footRadius - SIZE([1])(drawer)[0]]), drawer, drawerWall, knob]

	desk = desk + firstDeskSupports + secondDeskSupports + drawers
	VIEW(COLOR(BLACK)(STRUCT(desk)))
 
def ggpl_chair(dx,dy,dz):
	"""This function, given the three dimensions dx, dy and dz, 
	returns the VIEW of a simple wooden chair."""
	chair = []	
	footRadius = .05
	seatHeight = .015
	seatBackThickness = .015
	seatBackHeight = dz/6.
	box = SKEL_1(CUBOID([dx,dy,dz]))
	chair.append(box)
	supportTop = SPHERE(footRadius)([40,40])
	supportTop = JOIN(SKEL_1(supportTop))

	feetModel = [[0 + footRadius,0 + footRadius],[dx - footRadius,0 + footRadius], [dx - footRadius, dy - footRadius], [0 + footRadius, dy - footRadius]]
	support = CYLINDER([1.3*footRadius/2.,dy - 2*footRadius])(100)
	support = MAP([S1,S3,S2])(support)
	sideSupport = T([1,2,3])([footRadius,footRadius,dz/4. - footRadius])(support)
	sideSupports = [sideSupport, T([1])([dx - 2*footRadius])(sideSupport)]
	support = S(1)(.75)(support)
	support = T([1,2,3])([footRadius,footRadius,dz/2. - footRadius/2.])(support)
	supports = [support, T([1])([dx - 2*footRadius])(support)]
	
	otherSideSupport = CYLINDER([1.3*footRadius/2.,dx - 2*footRadius])(100)
	otherSideSupport = MAP([S1,S3,S2])(otherSideSupport)
	otherSideSupport = R([1,2])(-PI/2.)(otherSideSupport)
	otherSideSupport = T([1,2,3])([footRadius,footRadius,7*dz/20.])(otherSideSupport)
	otherSideSupports = [otherSideSupport, T([2])([dy-2*footRadius])(otherSideSupport)]
	
	seat = CUBOID([dx - 2*footRadius, dy - 2*footRadius, seatHeight])
	seat = T([1,2,3])([footRadius, footRadius, dz/2.-footRadius/2.])(seat)
	chair.append(seat)
	seatBack = CUBOID([dx - 2*footRadius, seatBackThickness, seatBackHeight])
	seatBack = T([1,2,3])([footRadius, footRadius, dz - 2*footRadius - seatBackHeight])(seatBack)
	chair.append(seatBack)

	for footModel in feetModel:
		if(footModel[1] != footRadius):
			solidFoot = CYLINDER([footRadius, dz/2.])(100)
			footSphere = T([1,2,3])([footModel[0],footModel[1],dz/2.])(supportTop)
		else:
			solidFoot = CYLINDER([footRadius, dz - footRadius])(100)
			footSphere = T([1,2,3])([footModel[0],footModel[1],dz - footRadius])(supportTop)
		solidFoot = T([1,2])([footModel[0],footModel[1]])(solidFoot)
		chair.append(solidFoot)
		chair.append(footSphere)

	chair = chair + supports + sideSupports + otherSideSupports
	VIEW(COLOR(Color4f([193/255., 154/255., 107/255., 1]))(STRUCT(chair)))


ggpl_children_table(4,4,1.25)
ggpl_teacher_desk(1.5, 1, 1.25)
ggpl_chair(.75,.75,1.25)