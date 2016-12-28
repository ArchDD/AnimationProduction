import maya.cmds as cmds
import random

random.seed(0)

result = cmds.polyCube( w=1, h=1, d=1, name='lightCube#')
transformName = result[0]

instanceGroup = cmds.group(empty=True, name=transformName+'_grp#')

for i in range(0, 50):
	instanceResult = cmds.instance(transformName, name=transformName+'_instance#')
	cmds.parent(instanceResult, instanceGroup)

	x = random.uniform(-10, 10)
	y = random.uniform(0, 20)
	z = random.uniform(-10, 10)

	cmds.move(x, y, z, instanceResult)

	xRot = random.uniform(0, 360)
	yRot = random.uniform(0, 360)
	zRot = random.uniform(0, 360)

	cmds.rotate(xRot, yRot, zRot, instanceResult)
	scalingFactor = random.uniform(0.3, 1.5)

	cmds.scale(scalingFactor, scalingFactor, scalingFactor, instanceResult)

cmds.delete(result)
cmds.xform(instanceGroup, centerPivots=True)