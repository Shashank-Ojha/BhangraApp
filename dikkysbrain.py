import math
from pickle import load
hashtable=load(open("PunjabTesting2.pkl","rb"))
def distance(p1, p2):
    (x1, y1, z1, t1) = p1
    (x2, y2, z2, t2) = p2
    dx = (x1-x2)**2
    dy = (y1-y2)**2
    dz = (z1-z2)**2
    return math.sqrt(dx+dy+ dz)

def pvector(p1, p2):
    (x1, y1, z1, t1) = p1
    (x2, y2, z2, t2) = p2
    return (x2-x1, y2-y1, z2-z1)

def derivative(v1, v2, t):
    (x1, y1, z1) = v1
    (x2, y2, z2) = v2
    return ((x2-x1)/t, (y2-y1)/t, (z2-z1)/t)

def dot(v1, v2): #p2>p1 and p4>p3
	(x1, y1, z1) = v1
	(x2, y2, z2) = v2
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
	return math.acos(dotp/(m1*m2)) #radian

def delta(x1, x2):
    return (x2-x1)


# def gradePunjab(punjabList):
#     #arms
#     for punjab in punjabList: #each punjab
#         for moment in punjab:
#             #0-rightHand
#             #1-leftHand
#             #2-rightElbow
#             #3-leftElbow
#             #4-rightShoulder
#             #5-leftShoulder
#             #(x,y,z,t)
#             rightElbowAngle=angle(getVectors(rightShoulder, rightElbow, rightElbow, rightHand)) #check this ordering later when im not tired af
#             leftElbowAngle=angle(getVectors(leftShoulder, leftElbow, leftElbow, leftHand)) #check ordering
#             rightElbowAngleDiff=math.abs(rightElbowAngle*(360/(2*math.pi))-170)
#             lefttElbowAngleDiff=math.abs(leftElbowAngle*(360/(2*math.pi))-170)
#             #margin of error for elbow angles:
#                 #A - 


def getPunjabs(rightHandToShoulderDistances, leftHandToShoulderDistances, hashtable):
    for i in range(1,len(rightHandToShoulderDistances)):
        if delta(rightHandToShoulderDistances[i], rightHandToShoulderDistances[i-1])>0:
            rightHandToShoulderDistances[i-1]=1 #means up 
        else:
            rightHandToShoulderDistances[i-1]=-1 #means down
        if delta(leftHandToShoulderDistances[i], leftHandToShoulderDistances[i-1])>0:
            leftHandToShoulderDistances[i-1]=1
        else:
            leftHandToShoulderDistances[i-1]=-1
    rightHandToShoulderDistances.pop()
    leftHandToShoulderDistances.pop()
    SERIESLEN=3
    punjabList=[]  #this is wack  [ [((),(),()),((),(),())], [((),(),()),((),(),())] ]
                           #        ^^^                       
                           #       this is one punjab movement
                           #         each point in moment in time for each body pos
                           #           (x,y,z,t) tuple for each body pos
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
    seenNegOnes=False
    #look for pattern
    for i in range(len(rightHandToShoulderDistances)-SERIESLEN):
        rightHand=rightHandList[i] 
        leftHand=leftHandList[i]
        rightElbow=rightElbowList[i]
        leftElbow=leftElbowList[i]
        rightShoulder=rightShoulderList[i]
        leftShoulder= leftShoulderList[i]
        neck=neckList[i]
        chest=chestList[i]
        bund=bundList[i]
        leftHip= leftHipList[i]
        leftKnee= leftKneeList[i]
        leftFoot=leftFootList[i]
        rightHip =rightHipList[i]
        rightKnee = rightKneeList[i]
        rightFoot= rightFootList[i]

        if ((rightHandToShoulderDistances[i]==1 and rightHandToShoulderDistances[i+1:i+SERIESLEN+1]==[1]*SERIESLEN) or 
            (leftHandToShoulderDistances[i]==1 and leftHandToShoulderDistances[i+1:i+SERIESLEN+1]==[1]*SERIESLEN)):
            punjabList.append([(rightHand, leftHand, rightElbow,leftElbow, rightShoulder, leftShoulder, neck, chest,bund,
                leftHip, leftKnee, leftFoot, rightHip,rightKnee, rightFoot)])
            j=i
            while (j<len(rightHandToShoulderDistances)-SERIESLEN): 
                if seenNegOnes and rightHandToShoulderDistances[j+1:j+1+SERIESLEN]==[1]*SERIESLEN:
                    #we are done
                    punjabList.append([(rightHandList[j], leftHandList[j], rightElbowList[j], leftElbowList[j], rightShoulderList[j], leftShoulderList[j], neckList[j], chestList[j], bundList[j],
                leftHipList[j], leftKneeList[j], leftFootList[j], rightHipList[j],rightKneeList[j], rightFootList[j])])
                    seenNegOnes=False
                    continue
                if rightHandToShoulderDistances[j:j+SERIESLEN]==[-1]* SERIESLEN:
                    seenNegOnes=True
                punjabList[-1].append((rightHandList[j], leftHandList[j], rightElbowList[j], leftElbowList[j], rightShoulderList[j], leftShoulderList[j], neckList[j], chestList[j], bundList[j],
                leftHipList[j], leftKneeList[j], leftFootList[j], rightHipList[j],rightKneeList[j], rightFootList[j]))
                j+=1
            punjabList.pop()
            break
    return punjabList

def punjab(hashtable):
    #pretend we have init already written
    #pretend we have placeholder init vars
    rightHandList=hashtable[21]
    leftHandList=hashtable[11]
    rightElbowList=hashtable[22]
    leftElbowList=hashtable[12]
    rightShoulderList=hashtable[23]
    leftShoulderList=hashtable[13]
    rightHandToShoulderDistances=[]
    leftHandToShoulderDistances=[]
    for i in range(len(rightHandList)): #this separates punjabs
        #will be a tuple(x,y,z,t)
        rightHand=rightHandList[i] 
        leftHand=leftHandList[i]
        rightElbow=rightElbowList[i]
        leftElbow=leftElbowList[i]
        rightShoulder=rightShoulderList[i]
        leftShoulder= leftShoulderList[i]
        rightHandToShoulder=distance(rightHand, rightShoulder)
        leftHandToShoulder=distance(leftHand, leftShoulder)
        rightHandToShoulderDistances.append(rightHandToShoulder)
        leftHandToShoulderDistances.append(leftHandToShoulder)
    punjabList=getPunjabs(rightHandToShoulderDistances, leftHandToShoulderDistances, hashtable)
    return punjabList

    #     if rightHandToShoulder>maxDistRightHandToShoulder or leftHandToShoulder>maxDistLeftHandToShoulder: #might be buggy maybe switch to and?
    #         rightHandToShoulderNext=distance(rightHandList[i+1],rightShoulderList[i+1])
    #         leftHandToShoulderNext=distance(leftHandList[i+1],leftShoulderList[i+1])
    #         maxDistRightHandToShoulder=rightHandToShoulder
    #         if rightHandToShoulderNext<maxDistRightHandToShoulder or leftHandToShoulderNext<maxDistLeftHandToShoulder: #might be buggy
    #             maxDistRightHandToShoulder=-100
    #             if startPunjab==None or startPunjab==False:
    #                 startPunjab=True
    #                 punjabList.append([(rightHand, leftHand, rightElbow, leftElbow, rightShoulder, leftShoulder)])
    #                 continue
    #             if startPunjab==True:
    #                 startPunjab=False #end=false
    #                 punjabList[-1].append((rightHand, leftHand, rightElbow, leftElbow, rightShoulder, leftShoulder)) #adding a tuple to the last 
    #                 continue
    #     punjabList[-1].append((rightHand, leftHand, rightElbow, leftElbow, rightShoulder, leftShoulder))
    # return (punjabList)
    
    # gradePunjab(punjabList)





              

        # could possibly be used for scoring
        # if rightHandToShoulder<miDistRightHandToShoulder or leftHandToShoulder<minDistLeftHandToShoulder: #might  be buggy
        #     rightHandToShoulderNext=distance(rightHandList[i+1],rightShoulderList[i+1])
        #     leftHandToShoulderNext=distance(leftHandList[i+1],leftShoulderList[i+1])
        #     if rightHandToShoulderNext>minDistRightHandToShoulder or leftHandToShoulderNext> : #might be buggy
        #         #this is the end of punjab

yello=punjab(hashtable)
print(yello)  
print ("length of punjab=", len(yello))      
    

def newDot(v1,v2):
    # (x1,y1) = (v1[0],v1[1])
    # (x2,y2) = (v1[0],v1[1])
    # length1 = (x1**2 + y1**2)**0.5
    # length2 = (x2**2 + y2**2)**0.5
    v1n = (v1[0], v1[1], 0)
    v2n = (v2[0], v2[1], 0)
    return (v1n[0]*v2n[0] + v1n[1]*v2n[1])


def newAngle(v1,v2):
    v1n = (v1[0], v1[1], 0)
    v2n = (v2[0], v2[1], 0)
    newDotp = newDot(v1n, v2n)
    m1 = magnitude(v1n)
    m2 = magnitude(v2n)
    return math.acos(newDotp/(m1*m2)) #rad




def gradePunjab(punjabList): # Master Grading Function for Punjab, will return score
    #arms
    # for punjab in punjabList: #each punjab - involved 
    #    for moment in punjab:
            #0-rightHand
            #1-leftHand
            #2-rightElbow
            #3-leftElbow
            #4-rightShoulder
            #5-leftShoulder
            #(x,y,z,t)

            # rightElbowAngle=angle(getVectors(rightShoulder, rightElbow, rightElbow, rightHand)) #check this ordering later when im not tired af
            # leftElbowAngle=angle(getVectors(leftShoulder, leftElbow, leftElbow, leftHand)) #check ordering
            # rightElbowAngleDiff=math.abs(rightElbowAngle*(360/(2*math.pi))-170)
            # lefttElbowAngleDiff=math.abs(leftElbowAngle*(360/(2*math.pi))-170)

            #margin of error for elbow angles:
                #A - 

    ##### REGULARITY GRADE #####
    # @max length, the angle between shoulder and hand should be (Fairly) consistent
    # we assume the first large tuple of each small list is the max length
    maxPosList = list()
    for punjab in punjabList:
        maxPosList.append(punjab[0])
    # for each maxlength, calculate the angle between shoulder height and elbow
    for bigtuple in maxPosList: 
        #right elbow angle 
        rightShoulderHeightP1 = (bigtuple[2][0], bigtuple[4][1], bigtuple[4][2], bigtuple[4][3]) #takes everything  of right shoulder except x value, which is from right elbow
        rightElbowP4 = (bigtuple[2][0], bigtuple[2][1], bigtuple[4][2], bigtuple[2][3])
        #(v1,v2) = getVectors(rightShoulderHeightP1, bigtuple[4], bigtuple[4], rightElbowP4)
        (v1,v2) = getVectors(bigtuple[4], rightShoulderHeightP1, bigtuple[4], rightElbowP4)
        rightAngle = newAngle(v1,v2) # in radians
        #left elbow hangle
        # leftShoulderHeightP1 = (bigtuple[3][0], bigtuple[5][1], bigtuple[5][2], bigtuple[5][3]) #takes everything  of right shoulder except x value, which is from right elbow
        # leftElbowP4 = (bigtuple[3][0], bigtuple[3][1], bigtuple[5][2], bigtuple[3][3])
        # # (v1,v2) = getVectors(leftShoulderHeightP1, bigtuple[5], bigtuple[5], leftElbowP4)
        # (v1,v2) = getVectors(bigtuple[5], leftShoulderHeightP1, bigtuple[5], leftElbowP4)
        # leftAngle = angle(v1,v2) # in radians

        #print(180-math.degrees(rightAngle))
        #print(180-math.degrees(leftAngle))
        print(rightShoulderHeightP1)
        print(bigtuple[4])
        print(bigtuple[4])
        print(rightElbowP4)
        print(v1,v2)
        print(math.degrees(rightAngle))


print("start of test")
print(gradePunjab(yello))
print("it worked")


    # rightHandList=hashtable[21]
    # leftHandList=hashtabble[11]
    # rightElbowList=hashtable[22]
    # leftElbowList=hashtable[12]
    # rightShoulderList=hashtable[23]
    # leftShoulderList=hashtable[13]






