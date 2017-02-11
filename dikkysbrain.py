import math
from pickle import load

def distance(p1, p2):
	(x1, y1, z1, t1) = p1
	(x2, y2, z2, t2) = p2
	dx = (x1-x2)**2
	dy = (y1-y2)**2
	dz = (z1-z2)**2
	return math.sqrt(dx, dy, dz)

def pvector(p1, p2):
	(x1, y1, z1, t1) = p1
	(x2, y2, z2, t2) = p2
	return (x2-x1, y2-y1, z2-z1)

def derivative(v1, v2, t):
	(x1, y1, z1) = v1
	(x2, y2, z2) = v2
	return ((x2-x1)/t, (y2-y1)/t, (z2-z1)/t)

def dot(v1, v2): #p2>p1 and p4>p3
	(x1, y1, z1, t1) = v1
	(x2, y2, z2, t2) = v2
	return (x1*x2 + y1*y2 + z1*z2)

def getVectors(p1, p2, p3, p4): #p2>p1 and p4>p3
    (x1, y1, z1, t1) = p1
    (x2, y2, z2, t2) = p2
    (x3, y3, z3, t3) = p3
    (x4, y4, z4, t4) = p4
    v1=(x2-x1, y2-y1, z2-z1)
    v2=(x4-x3, y4-y3, z4-z3)
    return (v1, v2)

def cross(v1, v2):
	(x1, y1, z1) = v1
	(x2, y2, z2) = v2
	i = y1*z2 - y2*z1
	j = -(x1*z2 - x2*z1)
	k = x1*y2 - x2*y1
	return (i, j, k)

def magnitude(v):
	(x1, y1, z1) = v
	return math.sqrt(x1**2 + y1**2 + z1**2)

def normalize(v):
	(x1, y1, z1) = v
	m = magnitude(v)
	return (x1/m, y1/m, z1/m)


def angle(v1, v2):
	dotp = dot(v1, v2)
	m1 = magnitude(v1)
	m2 = magnitude(v2)
	return acos(dotp/(m1*m2)) #radian


def gradePunjab(punjabList):
    #arms
    for punjab in punjabList: #each punjab
        for moment in punjab:
            #0-rightHand
            #1-leftHand
            #2-rightElbow
            #3-leftElbow
            #4-rightShoulder
            #5-leftShoulder
            #(x,y,z,t)
            rightElbowAngle=angle(getVectors(rightShoulder, rightElbow, rightElbow, rightHand)) #check this ordering later when im not tired af
            leftElbowAngle=angle(getVectors(leftShoulder, leftElbow, leftElbow, leftHand)) #check ordering
            rightElbowAngleDiff=math.abs(rightElbowAngle*(360/(2*math.pi))-170)
            lefttElbowAngleDiff=math.abs(leftElbowAngle*(360/(2*math.pi))-170)
            #margin of error for elbow angles:
                #A - 



def punjab(hashtable):
    #pretend we have init already written
    #pretend we have placeholder init vars
    rightHandList=hashtable[21]
    leftHandList=hashtable[11]
    rightElbowList=hashtable[22]
    leftElbowList=hashtable[12]
    rightShoulderList=hashtable[23]
    leftShoulderList=hashtable[13]
    neckList=hashtable[99]
    chestList=hashtable[98]
    bundList=hashtable[96]
    leftHipList=hashtable[33]
    leftKneeList=hashtable[32]
    leftFootList=hashtable[31]
    rightHipList = hashtable[43]
    rightKneeList = hashtable[42]
    rightFootList = hashtable[41]
    maxDistRightHandToShoulder=-100
    maxDistLeftHandToShoulder=-100
    minDistRightHandToShoulder=1000
    minDistLeftHandToShoulder=1000
    startPunjab=None
    punjabList=[]  #this is wack  [ [((),(),()),((),(),())], [((),(),()),((),(),())] ]
                           #        ^^^                       
                           #       this is one punjab movement
                           #         each point in moment in time for each body pos
                           #           (x,y,z,t) tuple for each body pos
    for i in range(length(rightHandList)-1): #this separates punjabs
        #will be a tuple(x,y,z,t)
        rightHand=rightHandList[i] 
        leftHand=leftHandList[i]
        rightElbow=rightElbowList[i]
        leftElbow=leftElbowList[i]
        rightShoulder=rightShoulderList[i]
        leftShoulder= leftShoulderList[i]
        neckList=neckList[i]
        chestList=chestList[i]
        bund=bundList[i]
        leftHip= leftHipList[i]
        leftKnee= leftKneeList[i]
        leftFoot=leftFootList[i]
        rightHip =rightHipList[i]
        rightKnee = rightKneeList[i]
        rightFoot= rightFootList[i]
        rightHandToElbow=distance(rightHand, rightElbow) #integer value
        rightElbowToShoulder=distance(rightElbow, rightShoulder)
        rightHandToShoulder=distance(rightHand, rightShoulder)
        leftHandToElbow=distance(leftHand, leftElbow) #integer value
        leftElbowToShoulder=distance(leftElbow, leftShoulder)
        leftHandToShoulder=distance(leftHand, leftShoulder)
        if rightHandToShoulder>maxDistRightHandToShoulder or leftHandToShoulder>maxDistLeftHandToShoulder: #might be buggy maybe switch to and?
            rightHandToShoulderNext=distance(rightHandList[i+1],rightShoulderList[i+1])
            leftHandToShoulderNext=distance(leftHandList[i+1],leftShoulderList[i+1])
            maxDistRightHandToShoulder=rightHandToShoulder
            if rightHandToShoulderNext<maxDistRightHandToShoulder or leftHandToShoulderNext<maxDistLeftHandToShoulder: #might be buggy
                maxDistRightHandToShoulder=-100
                if startPunjab==None or startPunjab==False:
                    startPunjab=True
                    punjabList.append([(rightHand, leftHand, rightElbow, leftElbow, rightShoulder, leftShoulder)])
                    continue
                if startPunjab==True:
                    startPunjab=False #end=false
                    punjabList[-1].append((rightHand, leftHand, rightElbow, leftElbow, rightShoulder, leftShoulder))
                    continue
        punjabList[-1].append((rightHand, leftHand, rightElbow, leftElbow, rightShoulder, leftShoulder))
        gradePunjab(punjabList)





              

        # could possibly be used for scoring
        # if rightHandToShoulder<miDistRightHandToShoulder or leftHandToShoulder<minDistLeftHandToShoulder: #might  be buggy
        #     rightHandToShoulderNext=distance(rightHandList[i+1],rightShoulderList[i+1])
        #     leftHandToShoulderNext=distance(leftHandList[i+1],leftShoulderList[i+1])
        #     if rightHandToShoulderNext>minDistRightHandToShoulder or leftHandToShoulderNext> : #might be buggy
        #         #this is the end of punjab


        
        #WRITE THIS HELPER FUNCTION
        startPunjab=isStartPunjab(rightHandList, leftHandList, rightElbowList, leftElbowList, rightShoulderList, leftShoulderList, i) #bool value        
       endPunjab=isEndPunjab(rightHandList, leftHandList, rightElbowList, leftElbowList, rightShoulderList, leftShoulderList, i) #bool value
       
def isStartPunjab(rightHandList, leftHandList, rightElbowList, leftElbowList, rightShoulderList, leftShoulderList, i):
    
def isEndPunjab(rightHandList, leftHandList, rightElbowList, leftElbowList, rightShoulderList, leftShoulderList, i):
    SECONDS=.5
    if i < SECONDS * 10:
    #only look forwards
    if i>SECONDS*10:
    #only look backwards

