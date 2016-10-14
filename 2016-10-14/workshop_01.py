from pyplasm import *

def space_frame(beamHeigth, pillarLength, pillarHeigth, pillarDistances, interstoryHeights, buildingSequence):
	"""This function takes the needed parameters to build a reinforced concrete frame.
		The @param buildingSequence indicates to build continuous pillars or beams"""
	if (buildingSequence == "b"):
		return VIEW(space_frame_continuous_beams(beamHeigth, pillarLength, pillarHeigth, pillarDistances, interstoryHeights))
	elif (buildingSequence == "p"):
		return VIEW(space_frame_continuous_pillars(beamHeigth, pillarLength, pillarHeigth, pillarDistances, interstoryHeights))
	else:
		print("Wrong input. Choose p to create pillars before, b for beams")

def space_frame_continuous_beams(beamHeigth, pillarLength, pillarHeigth, pillarDistances, interstoryHeights):
	"""This function return the model of the frame by building continuous beams and interrupted pillars"""
	pillarNumber = len(pillarDistances) + 1
	floorsNumber = len(interstoryHeights)

	pillarsList = []
	beamLength = 0
	for elem in pillarDistances:
		pillarsList.append(pillarLength)
		pillarsList.append(-elem)
		beamLength += elem
	pillarsList.append(pillarLength)
	beamLength += pillarLength * pillarNumber

	heightsList = []
	beamsList = []
	for elem in interstoryHeights:
		heightsList.append(elem - beamHeigth)
		heightsList.append(-beamHeigth)
		beamsList.append(-(elem-beamHeigth))
		beamsList.append(beamHeigth)

	pillars = PROD([QUOTE(pillarsList), QUOTE([pillarLength])])
	pillars3d = PROD([pillars, QUOTE(heightsList)])
	VIEW(pillars3d)
	beams = PROD([QUOTE([beamLength]), QUOTE([pillarLength])])
	
	beams3d = PROD([beams, QUOTE(beamsList)])
	VIEW(beams3d)
	model = STRUCT([pillars3d, beams3d])
	return model

def space_frame_continuous_pillars(beamHeigth, pillarLength, pillarHeigth, pillarDistances, interstoryHeights):
	"""This function return the model of the frame by building continuous pillars and interrupted beams"""
	pillarNumber = len(pillarDistances) + 1
	floorsNumber = len(interstoryHeights)

	pillarsList = []
	beamsList = []
	for elem in pillarDistances:
		pillarsList.append(pillarLength)
		pillarsList.append(-elem)
		beamsList.append(-pillarLength)
		beamsList.append(elem)
	pillarsList.append(pillarLength)

	pillarsHeight = 0
	beamsDistances = []
	for elem in interstoryHeights:
		pillarsHeight += elem
		beamsDistances.append(-(elem-beamHeigth))
		beamsDistances.append(beamHeigth)

	pillars = PROD([QUOTE(pillarsList), QUOTE([pillarLength])])
	pillars3d = PROD([pillars, QUOTE([pillarsHeight])])
	VIEW(pillars3d)

	beamsList.append(-pillarLength)

	beams = PROD([QUOTE(beamsList), QUOTE([pillarLength])])

	beams3d = PROD([beams, QUOTE(beamsDistances)])
	VIEW(beams3d)
	model = STRUCT([pillars3d, beams3d])
	return model

model = space_frame(0.2, 0.2, 5, [1,2,4,5,6], [2,1,4,3], "b")