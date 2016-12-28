import maya.cmds as cmds

# selection
result = cmds.ls(orderedSelection=True)
print 'result: %s' % (result)

# aim constrain
if len(selectionList) >= 2:
	targetName = selectionList[0]
	selectionList.remove(targetName)

	for objectName in selectionList:
		cmds.aimConstraint(targetName, objectName, aimVector = [0, 1, 0])

# set keyframes
startTime = cmds.playbackOptions(query=True, minTime=True)
endTime = cmds.playbackOptions(query=True, maxTime=True)

for objectName in selectionList:
	cmds.cutKey(objectName, time=(startTime, endTime), attribute='rotateY')
	cmds.setKeyframe(objectName, time=startTime, attribute='rotateY', value=0)
	cmds.setKeyframe(objectName, time=endTime, attribute='rotateY', value=360)#
	cmds.keyTangent(inTangentType='linear', outTangentType='linear')

	