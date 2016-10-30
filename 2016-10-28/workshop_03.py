from pyplasm import *
import math

def generate_steps(stepNumber, tread, riser, stepWidth):
    step2d = MKPOL([[[tread, 0],[tread, riser*2], [tread*2, riser*2], [tread*2, riser]], [[1,2,3,4]], None])
    steps = []
    firstStep2d = CUBOID([stepWidth,tread])
    firstStep = PROD([firstStep2d, QUOTE([riser])])
    steps.append(firstStep)
    for i in range(int(stepNumber-1)):
        steps.append(T([2,3])([(tread*i), riser*i])(PROD([Q(stepWidth), step2d])))
 
    return steps

def ggpl_u_shaped_stairs(dx, dy, dz):
    wallThickness = 0.3
    riser = 0.2
    stairsHeight = dz / 2.0
    stepNumbers = math.ceil(stairsHeight / riser)
    tread = dy / (stepNumbers+4)
    lengthOfFlight = tread * stepNumbers
    platformX = dx - (wallThickness*2.0)
    stairsX = (dx/2.0) - wallThickness
    firstStairs = generate_steps(stepNumbers, tread, riser, stairsX)
    secondStairs = generate_steps(stepNumbers, tread, riser, stairsX)[1:]
    lastStep2d = MKPOL([[[tread, 0],[tread, riser*2], [tread*2, riser*2], [tread*2, riser]], [[1,2,3,4]], None])
    lastStep = T([2,3])([(tread*(stepNumbers-1.0)), riser*(stepNumbers-1.0)])(PROD([Q(stairsX), lastStep2d]))
    secondStairs.append(lastStep)
    secondStairs = R([1,2])(PI)(STRUCT(secondStairs))
    secondStairs = T([1,2,3])([platformX+wallThickness,tread+lengthOfFlight,stairsHeight-riser])(secondStairs)
    
    stairs = STRUCT(firstStairs)

    stairs = T(1)([wallThickness])(stairs)
    platform = CUBOID([platformX, (tread*4) - wallThickness, riser])
    firstWall = CUBOID([wallThickness, dy, dz])
    secondWall = CUBOID([dx - (wallThickness*2), wallThickness, dz])
    secondWall = T([1,2])([wallThickness, dy - wallThickness])(secondWall)
    thirdWall = CUBOID([wallThickness, dy, dz])
    thirdWall = T([1])([dx - wallThickness])(thirdWall)
    traslatedPlatform = T([1,2,3])([wallThickness, tread*stepNumbers, riser*stepNumbers-riser])(platform)
   
    result = STRUCT([firstWall, secondWall, thirdWall, stairs, traslatedPlatform, secondStairs])
    box = SKEL_1(BOX([1,2,3])(CUBOID([dx, dy, dz])))
    return STRUCT([result, box]) 

VIEW(ggpl_u_shaped_stairs(3.0,3.4,4.0))