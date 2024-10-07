"""
Model our creature and wrap it in one class.
First version on 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

----------------------------------

Modified by Daniel Scrivener 09/2023
"""

from Component import Component
from Point import Point
import ColorType as Ct
from Shapes import Cone, Cube, Sphere
from Shapes import Cylinder
import numpy as np


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 
    #
    # In order to simplify the process of constructing your model, the rotational origin of each Shape has been offset by -1/2 * dz,
    # where dz is the total length of the shape along its z-axis. In other words, the rotational origin lies along the smallest 
    # local z-value rather than being at the translational origin, or the object's true center. 
    # 
    # This allows Shapes to rotate "at the joint" when chained together, much like segments of a limb. 
    #
    # In general, you should construct each component such that it is longest in its local z-direction: 
    # otherwise, rotations may not behave as expected.
    #
    # Please see Blackboard for an illustration of how this behavior works.



    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent

        #hood
        hoodsize = .78
        hood = Sphere(Point((0, 1.2, 0)), shaderProg, [hoodsize, hoodsize, hoodsize], Ct.DARKORANGE1)
        self.addChild(hood)
 
        #head
        head = .7
        link1 = Sphere(Point((-0.1, 0, 0)), shaderProg, [head, head, head], Ct.BLACK, limb=False)
        link1.uRange = [-10, 10.0]  # list<float>(2)
        link1.vRange = [-10, 10.0]
        link1.wRange = [-10, 10.0]
        hood.addChild(link1)

        

        #crown 

        #base crown

        crownbase = Cylinder(Point((.3, .7, 0.05)), shaderProg, [.5, .5, .06], Ct.YELLOW)
        crownbase.setDefaultAngle(90, crownbase.vAxis)
        crownbase.setDefaultAngle(115, crownbase.uAxis)
        hood.addChild(crownbase)

        num_spikes = 8  # Number of spikes for the crown
        #.15
        spike_height = .15
        spike_radius = 0.08
        crown_radius = 0.4  # Radius from the center of the hood to the spikes
        z_offset = .13

        # Create and position the spikes around the hood
        for i in range(num_spikes):
            angle = (i / num_spikes) * 360  # Calculate the angle for each spike
            x = crown_radius * np.cos(np.radians(angle))
            y = crown_radius * np.sin(np.radians(angle))

            
            # Create each spike and adjust the z-coordinate
            crown_spike = Cone(Point((x, y, z_offset)), shaderProg, [spike_radius, spike_radius, spike_height], Ct.YELLOW)
            crown_spike.setDefaultAngle(180, crownbase.uAxis)  # Rotate the spike upright

            crownbase.addChild(crown_spike)

        #antennas

        #antennas base
        antennasthickness = .1
        antennasleft = Cylinder(Point((0, .2, -.2)), shaderProg, [antennasthickness, antennasthickness, .3], Ct.BLACK)
        antennasleft.setDefaultAngle(245, antennasleft.uAxis)


        hood.addChild(antennasleft)
        antennasright = Cylinder(Point((0, .2, .8)), shaderProg, [antennasthickness, antennasthickness, .3], Ct.BLACK)
        antennasright.setDefaultAngle(295, antennasright.uAxis)
        hood.addChild(antennasright)

        #antennas ball
        antennasballthickness = .2
        antennasballleft = Sphere(Point((0, 0, 0.2)), shaderProg, [antennasballthickness, antennasballthickness, antennasballthickness], Ct.DARKORANGE1, limb=False)
        antennasballleft.setDefaultAngle(180, antennasballleft.uAxis)
        antennasballleft.setDefaultAngle(180, antennasballleft.wAxis)
        antennasleft.addChild(antennasballleft)
        antennasballright = Sphere(Point((0, 0, 0.2)), shaderProg, [antennasballthickness, antennasballthickness, antennasballthickness], Ct.DARKORANGE1, limb=False)
        antennasballright.setDefaultAngle(180, antennasballright.uAxis)
        antennasright.addChild(antennasballright)

        #antennas tip
        antennastipthickness = antennasballthickness - .04
        antennastipheight = .1
        antennastipleft = Cone(Point((0, 0, 0.03)), shaderProg, [antennastipthickness, antennastipthickness, antennastipheight], Ct.DARKORANGE1)
        antennastipleft.setDefaultAngle(180, antennastipleft.uAxis)
        antennasballleft.addChild(antennastipleft)


        antennastiplright = Cone(Point((0, 0, 0.03)), shaderProg, [antennastipthickness, antennastipthickness, antennastipheight], Ct.DARKORANGE1)
        antennastiplright.setDefaultAngle(180, antennastiplright.uAxis)
        antennasballright.addChild(antennastiplright)

        
        #eyes
        a = .07
        eyeheight = .2
        eyeleft = Cone(Point((-0.516, 0, -.16)), shaderProg, [a, a, eyeheight], Ct.YELLOW)
        eyeleft.setCurrentAngle(15,eyeleft.uAxis)
        eyeleft.setCurrentAngle(-16,eyeleft.vAxis)
        eyeright = Cone(Point((-0.516, 0, .56)), shaderProg, [a, a, eyeheight], Ct.YELLOW)
        eyeright.setCurrentAngle(165,eyeright.uAxis)
        eyeright.setCurrentAngle(16,eyeleft.vAxis)

        link1.addChild(eyeleft)
        link1.addChild(eyeright) 

        #torso top component
        torso = .7
        link2 = Sphere(Point((0, -.7, 0)), shaderProg, [torso, 0.2, torso], Ct.BLACK)
        hood.addChild(link2)
        linktemp = link2
        stackheight = 0.2
        stackmovement = stackheight/2
        div = 17
        for i in range (4):
            rate =(1+i/div)
            if i % 2 == 0:
                link2 = Sphere(Point((0, -stackmovement, 0)), shaderProg, [torso*rate, stackheight, torso*rate], Ct.DARKORANGE1)
            else:
                link2 = Sphere(Point((0, -stackmovement, 0)), shaderProg, [torso*rate, stackheight, torso*rate], Ct.BLACK)
            linktemp.addChild(link2)
            linktemp = link2


        #arms (tied to torso)
        armsthickness = 0.1
        armlength = 0.3
        armleft = Cylinder(Point((0, 0, -torso*rate+.4)), shaderProg, [armsthickness, armsthickness, .2], Ct.DARKORANGE1)
        armleft.setDefaultAngle(180, armleft.uAxis)
        linktemp.addChild(armleft)
        armright = Cylinder(Point((0, 0, torso*rate-.1)), shaderProg, [armsthickness, armsthickness, .2], Ct.DARKORANGE1)
        linktemp.addChild(armright)

        #arms (forarm)
        forarmsthickness = 0.125

        forarmleft = Cylinder(Point((0, 0, +.3)), shaderProg, [forarmsthickness, forarmsthickness, .3], Ct.DARKORANGE1)
        armleft.addChild(forarmleft)
        forarmleft.setDefaultAngle(180, forarmleft.wAxis)
        forarmright = Cylinder(Point((0, 0, .4)), shaderProg, [forarmsthickness, forarmsthickness, .3], Ct.DARKORANGE1)
        armright.addChild(forarmright)

        handthickness = 0.15
        #hand
        handleft = Cylinder(Point((0, 0, +.4)), shaderProg, [handthickness, handthickness, handthickness], Ct.DARKORANGE1)
        forarmleft.addChild(handleft)
        handleft.setDefaultAngle(180, handleft.wAxis)
        handright = Cylinder(Point((0, 0, armlength)), shaderProg, [handthickness, handthickness, handthickness], Ct.DARKORANGE1)
        forarmright.addChild(handright)

        #fingers
        nailthickness = 0.045
        naillength = 0.2

        #right hand fingers
        for i in range(3):
            finger1 = Cone(Point((0, armsthickness - i*.1, armlength)), shaderProg, [nailthickness, nailthickness, naillength], Ct.BLACK)
            handright.addChild(finger1)
            

        finger1 = Cone(Point((0, armsthickness, armlength)), shaderProg, [nailthickness, nailthickness, naillength], Ct.BLACK)
        finger1.setDefaultAngle(270, finger1.uAxis)
        handright.addChild(finger1)

        #left hand fingers 
        for i in range(3):
            finger1 = Cone(Point((0, armsthickness - i*.1, armlength -0.05)), shaderProg, [nailthickness, nailthickness, naillength], Ct.BLACK)
            handleft.addChild(finger1)
           # finger1.setDefaultAngle(180, finger1.vAxis)
            #finger1.setCurrentAngle(180, finger1.wAxis)

        finger1 = Cone(Point((0, armsthickness-.2, armlength-.17)), shaderProg, [nailthickness, nailthickness, naillength], Ct.BLACK)
      #  finger1.setDefaultAngle(180, finger1.vAxis)
        finger1.setDefaultAngle(90, finger1.uAxis)
        handleft.addChild(finger1)

        #torso bottom
        for i in reversed (range (4)):
            rate =(1+i/div)
            if i % 2 == 0:
                link2 = Sphere(Point((0, -stackmovement, 0)), shaderProg, [torso*rate, stackheight, torso*rate], Ct.BLACK)
            else:
                link2 = Sphere(Point((0, -stackmovement, 0)), shaderProg, [torso*rate, stackheight, torso*rate], Ct.DARKORANGE1)
            linktemp.addChild(link2)
            linktemp = link2

        #legs

        legthickness = 0.15
        leglength = 0.2
        legleft = Cylinder(Point((0, 0, -.15)), shaderProg, [legthickness, legthickness, leglength], Ct.DARKORANGE1)
        legleft.setDefaultAngle(90, legleft.uAxis)
        legleft.setDefaultAngle(180, legleft.vAxis)
        linktemp.addChild(legleft)
        legright = Cylinder(Point((0, 0, .55)), shaderProg, [legthickness, legthickness, leglength], Ct.DARKORANGE1)
        legright.setDefaultAngle(90, legright.uAxis)
        linktemp.addChild(legright)

        #feet 

        feetleft = Cylinder(Point((0.2, 0, .4)), shaderProg, [.5, .3, .1], Ct.BLACK)
        legleft.addChild(feetleft)
        feetleft.setDefaultAngle(180, feetleft.vAxis)
        feetleft.setDefaultAngle(180, feetleft.wAxis)
        feetright = Cylinder(Point((-0.2, 0, .2)), shaderProg, [.5, .3, .1], Ct.BLACK)
        legright.addChild(feetright)

        
        self.componentList = [link1, hood, self, feetright, legright, antennasballright, antennasright, armright, forarmright, handright,  feetleft, handleft, legleft, antennasballleft, antennasleft, armleft, forarmleft]


 # Use dictionary for component reference
        self.anglelist = [
            {14,  15, 11},
            {14, 13, 15, 16, 12},
            {13, 16, 10}  
        ]
                    
                
        self.componentDict = {
            "link1": link1,
        }

    

        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.
