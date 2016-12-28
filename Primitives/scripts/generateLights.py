import maya.cmds as cmds
import random

random.seed(0)

sphereList = []
cubeList = []

sphereTransform = cmds.polySphere(r=2, name='lightSphere#')
cubeTransform = cmds.polyCube( w=1, h=1, d=1, name='lightCube#')
sphereName = sphereTransform[0]
cubeName = cubeTransform[0]

# instantiate light spheres
for i in range (0, 5):
    # create light group
    lightGroup = cmds.group(empty=True, name=sphereName+'_grp')

    sphereInstance = cmds.instance(sphereName, name=sphereName+'_instance#')
    cmds.parent(sphereInstance, lightGroup)
    sphereList.append(sphereInstance)

    # create group to contain cubes
    cubeGroup = cmds.group(empty=True, name=cubeName+'_grp#')
    cmds.parent(cubeGroup, lightGroup)

    # create locator group for cube locators
    locatorGroupName = cmds.group(empty=True, name='expansion_locator_grp#')
    cmds.parent(locatorGroupName, lightGroup)
    maxExpansion = 100
    newAttributeName = 'expansion'

    # instantiate cubes
    for i in range(0, 50):
        cubeInstance = cmds.instance(cubeName, name=cubeName+'_instance#')
        cubeList.append(cubeInstance)
        cmds.parent(cubeInstance, cubeGroup)

        x = random.uniform(-10, 10)
        y = random.uniform(0, 20)
        z = random.uniform(-10, 10)

        cmds.move(x, y, z, cubeInstance)

        xRot = random.uniform(0, 360)
        yRot = random.uniform(0, 360)
        zRot = random.uniform(0, 360)

        cmds.rotate(xRot, yRot, zRot, cubeInstance)
        scalingFactor = random.uniform(0.3, 1.5)

        cmds.scale(scalingFactor, scalingFactor, scalingFactor, cubeInstance)

        # aim cubes to sphere
        objectName = cubeInstance[0]
        targetName = sphereInstance[0]

        if not cmds.objExists('%s.%s' % (targetName, newAttributeName)):
            cmds.select(targetName)
            cmds.addAttr(longName=newAttributeName, shortName='exp',
                        attributeType='double', min=0, max=maxExpansion,
                        defaultValue=maxExpansion, keyable=True)

        coords = cmds.getAttr('%s.translate' % (objectName))[0]
        locatorName = cmds.spaceLocator(position=coords, name='%s_loc#' % (objectName))[0]
        cmds.xform(locatorName, centerPivots=True)
        cmds.parent(locatorName, locatorGroupName)

        pointConstraintName = cmds.pointConstraint([targetName, locatorName], objectName, name='%s_pointConstraints#' % (objectName))[0]
        cmds.expression(alwaysEvaluate=True, name='%s_attractWeight' % (objectName),
                        object=pointConstraintName, string='%sW0=%s-%s.%s' % (targetName,
                        maxExpansion, targetName, newAttributeName) )

        cmds.connectAttr('%s.%s' % (targetName, newAttributeName),
                        '%s.%sW1' % (pointConstraintName, locatorName))

        cmds.xform(locatorGroupName, centerPivots=True)
    cmds.xform(cubeGroup, centerPivots=True)

cmds.delete(sphereTransform)
cmds.delete(cubeTransform)