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
                    punjabList.append([(rightHandList[j+1], leftHandList[j+1], rightElbowList[j+1], leftElbowList[j+1], rightShoulderList[j+1], leftShoulderList[j+1], neckList[j+1], chestList[j+1], bundList[j+1],
                leftHipList[j+1], leftKneeList[j+1], leftFootList[j+1], rightHipList[j+1],rightKneeList[j+1], rightFootList[j+1])])
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

def punjabKneeAngle(dhammalList):
    MARGINERROR=10 #degrees
    def almostEqual(x, y, marginError):
        return abs(x-y) < marginError
    #need vector from hip knee
    #need vector from knee to foot
    #calculate angle between those vecotrs
    STDEV=6
    penalties=0
    countDhammals=0
    counter = 1
    for oneDhammal in dhammalList:
        #only take first few positions
        #high point happens at 1/3 of oneDhammal
        # for i in range(round(.33*len(oneDhammal)), round(.33*len(oneDhammal))+STDEV):
        if (counter%2 == 1):
            moment=oneDhammal[0]
            leftHip=moment[9]
            leftKnee=moment[10]
            leftFoot=moment[11]
            (v1, v2)=(getVectors(leftHip, leftKnee, leftKnee, leftFoot))
            (x1, y1, z1)=v1
            (x2, y2, z1)=v2
            v1=(x1, y1)
            v2=(x2, y2)
            leftKneeAngle=newAngle(v1, v2) * (360/(2*math.pi))
            if not (almostEqual(leftKneeAngle,90, MARGINERROR)):
                penalties+=1
            countDhammals+=1
        else:
            moment=oneDhammal[0]
            rightHip=moment[12]
            rightKnee=moment[13]
            rightFoot=moment[14]
            (v1, v2)=(getVectors(rightHip, rightKnee, rightKnee, rightFoot))
            (x1, y1, z1)=v1
            (x2, y2, z1)=v2
            v1=(x1, y1)
            v2=(x2, y2)
            rightKneeAngle=newAngle(v1, v2) * (360/(2*math.pi))
            if not (almostEqual(rightKneeAngle,90, MARGINERROR)):
                penalties+=1
            countDhammals+=1
        counter += 1
    percentageRight=(countDhammals-penalties)/countDhammals


    return percentageRight


def angleFeedback(angleScore):
    if angleScore<4:
        feedbackF=["Try to keep your hands in base position and keep pushing your elbows out!", "Keep your elbow angle at around 175 degrees!"]
        feedback=feedbackF[random.randint(0,1)]
    else:
        feedback="Good job with elbow angles!"
    return feedback

def leftArmFeedback(leftAngle):
    if leftAngle<4:
        feedbackF=["Keep your left arm at 45 degrees when at maximum extension!", "Try to fully complete the motion with your left arm!"]
        feedback=feedbackF[random.randint(0,1)]
    else: 
        feedback="Good job keeping your left arm at 45 degrees during punjab!"

def rightArmFeedback(rightAngle):
    if rightAngle<4:
        feedbackF=["Keep your right arm at 45 degrees when at maximum extension!", "Try to fully complete the motion with your right arm!"]
        feedback=feedbackF[random.randint(0,1)]
    else: 
        feedback="Great job keeping your right arm at 45 degrees during punjab!"

def heightDiffFeedback(heightDiffScore):
    if heightDiffScore<4:
        feedbackF=["Your right and left arms extend to different heights during punjab. Try to keep them more even!", "Push out your right and left arms to the same distance during punjab!"]
        feedback=feedbackF[random.randint(0,1)]
    else:
        feedback="Great job coordinating both your punjab arms! Keep up the good form!"


def sameHeightFeedback(sameY):
    if sameY<4:
        feedbackF=["Try to keep your right and left arm extension the same throughout punjab. Try pumping more evenly.", "Your right and left arms are not extending the same distance away from your shoulders. Try to keep it more even!"]
        feedback=feedbackF[random.randint(0,1)]
    else:
        feedback="Good punjab arm form! Nice work gabbroo!"
def punjabFeedback(angleScore,leftAngle,rightAngle,heightDiffScore,sameY, finalPunjabScore):
    angle=angleFeedback(angleScore)
    leftArm=leftArmFeedback(leftAngle)
    rightArm=rightArmFeedback(rightAngle)
    heightDiff=heightDiffFeedback(heightDiffScore)
    sameHeight=sameHeightFeedback(sameY)
    score=str(finalPunjabScore)
    return ("Your score: " + score +"\n" +angle+"\n"+leftArm+"\n"+rightArm+"\n"+heightDiff+"\n"+sameHeight)

def gradePunjab(punjabList): # Master Grading Function for Punjab, will return score
    #arms
    #for punjab in punjabList: #each punjab - involved 
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
    regScore = 0
    # @max length, the angle between shoulder and hand should be (Fairly) consistent
    # we assume the first large tuple of each small list is the max length
    maxPosList = []
    for punjab in punjabList:
        maxPosList.append(punjab[0])
    # for each maxlength, calculate the angle between shoulder height and elbow
    calcPosList = list() # the output of angle calculations
    for bigtuple in maxPosList: 
        #right elbow angle 
        rightShoulderHeightP1 = (bigtuple[2][0], bigtuple[4][1], bigtuple[4][2], bigtuple[4][3]) #takes everything  of right shoulder except x value, which is from right elbow
        rightElbowP4 = (bigtuple[2][0], bigtuple[2][1], bigtuple[4][2], bigtuple[2][3])
        #(v1,v2) = getVectors(rightShoulderHeightP1, bigtuple[4], bigtuple[4], rightElbowP4)
        (v1,v2) = getVectors(bigtuple[4], rightShoulderHeightP1, bigtuple[4], rightElbowP4)
        print (v1)
        print (v2)
        rightAngle = newAngle(v1,v2) # in radians
        #left elbow hangle
        leftShoulderHeightP1 = (bigtuple[3][0], bigtuple[5][1], bigtuple[5][2], bigtuple[5][3]) #takes everything  of right shoulder except x value, which is from right elbow
        leftElbowP4 = (bigtuple[3][0], bigtuple[3][1], bigtuple[5][2], bigtuple[3][3])
        # (v1,v2) = getVectors(leftShoulderHeightP1, bigtuple[5], bigtuple[5], leftElbowP4)
        (v1,v2) = getVectors(bigtuple[5], leftShoulderHeightP1, bigtuple[5], leftElbowP4)
        leftAngle = angle(v1,v2) # in radians

        # leftShoulderHeightP1 = (bigtuple[3][0], bigtuple[5][1], bigtuple[5][2], bigtuple[5][3]) #takes everything  of right shoulder except x value, which is from right elbow
        # leftElbowP4 = (bigtuple[3][0], bigtuple[3][1], bigtuple[5][2], bigtuple[3][3])
        # # (v1,v2) = getVectors(leftShoulderHeightP1, bigtuple[5], bigtuple[5], leftElbowP4)
        # (v1,v2) = getVectors(bigtuple[5], leftShoulderHeightP1, bigtuple[5], leftElbowP4)
        # leftAngle = angle(v1,v2) # in radians
        #print(math.degrees(rightAngle), math.degrees(leftAngle))
        calcPosList.append((math.degrees(leftAngle), math.degrees(rightAngle))) # (left angle, right angle)

    angleRightSum = 0
    angleLeftSum = 0
    counter = 0
    for angleTuple in calcPosList:
        angleLeftSum += angleTuple[0]
        angleRightSum += angleTuple[1]
        counter += 1

    angleLeftAvg = angleLeftSum/counter
    angleRightAvg = angleRightSum/counter
    angleDiff = abs(angleLeftAvg - angleRightAvg)


# grade: give angle similarity score. #elbow angles
    if (angleDiff <= 5): 
        regScore += 5
        angleScore=5
    elif (angleDiff <= 10): 
        regScore += 4
        angleScore=4
    elif (angleDiff <= 15): 
        regScore += 3
        angleScore=3
    elif (angleDiff <= 20): 
        regScore += 2
        angleScore=2
    elif (angleDiff <= 25): 
        regScore += 1
        angleScore=1
    else:
        regScore += 0
        angleScore=0


# grade: how close is the angle to 45 degrees? LEFT ARM
    angleGradeL = angleLeftAvg - 45
    if (angleGradeL <= 5): 
        regScore += 5
        leftAngle=5
    elif (angleGradeL <= 10): 
        regScore += 4
        leftAngle=4
    elif (angleGradeL <= 15): 
        regScore += 3
        leftAngle=3
    elif (angleGradeL <= 20): 
        regScore += 2
        leftAngle=2
    elif (angleGradeL <= 25): 
        regScore += 1
        leftAngle=1
    else:
        regScore += 0
        leftAngle=0

# grade: how close is the angle to 45 degrees? RIGHT ARM
    angleGradeR = angleRightAvg - 45
    if (angleGradeR <= 5): 
        regScore += 5
        rightAngle=5
    elif (angleGradeR <= 10): 
        regScore += 4
        rightAngle=4
    elif (angleGradeR <= 15): 
        regScore += 3
        rightAngle=3
    elif (angleGradeR <= 20): 
        regScore += 2
        rightAngle=2
    elif (angleGradeR <= 25): 
        regScore += 1
        rightAngle=1
    else:
        regScore += 0
        rightAngle=0


    ##### HEIGHT OF HANDS GRADE #####
    yLeftList = list()
    yRightList = list()
    for bigtuple in maxPosList:
        yLeftList.append(bigtuple[1][1])
        yRightList.append(bigtuple[0][1])

    sum1 = 0
    for k in range(0, len(yLeftList)):
        sum1 += abs(yLeftList[k] - yRightList[k])

    heightDiffAvg = (sum1 / len(yLeftList))*100 #in cm

# grade: HeightDifference between your two hands - gotta be consistent (#4)
    if (heightDiffAvg <= 10): 
        regScore += 5
        heightDiffScore=5
    elif (heightDiffAvg <= 15): 
        regScore += 4
        heightDiffScore=4
    elif (heightDiffAvg <= 20): 
        regScore += 3
        heightDiffScore=3
    elif (heightDiffAvg <= 25): 
        regScore += 2
        heightDiffScore=2
    elif (heightDiffAvg <= 30): 
        regScore += 1
        heightDiffScore=1
    else:
        regScore += 0
        heightDiffScore=0

    ##### CHECK IF HANDS GO UP TO ROUGHLY SAME Y EACH TIME GRADE #####
    # remove abnormalities (if difference is greater thatn 40 cm just ignore the value)
    # for k in range(0, len(yLeftList)):
       
    #     if ((len(yLeftList) - k) < 0):

    #     if (abs(max(yLeftList) - yLeftList[len(yLeftList) - k]) >= 0.4):
    #         yLeftList.remove(yLeftList[k])

    while (abs(max(yLeftList) - min(yLeftList)) > 0.4):
        yLeftList.remove(min(yLeftList))
    while (abs(max(yRightList) - min(yRightList)) > 0.4):
        yRightList.remove(min(yRightList))
    
    leftDiff = (abs(max(yLeftList) - min(yLeftList)))*100
    rightDiff = (abs(max(yRightList) - min(yRightList)))*100

# grade: are your hands going to the same areas? (#5)
    if (leftDiff <= 15 and rightDiff <= 15): 
        regScore += 5
        sameY=5
    elif (leftDiff <= 20 and rightDiff <= 20): 
        regScore += 4
        sameY=4
    elif (leftDiff <= 25 and rightDiff <= 25): 
        regScore += 3
        sameY=3
    elif (leftDiff <= 30 and rightDiff <= 30): 
        regScore += 2
        sameY=2
    elif (leftDiff <= 35 and rightDiff <= 35): 
        regScore += 1
        sameY=1
    else:
        regScore += 0
        sameY=0

    ##### HANDS SHOULD BE OUTSIDE ELBOW GRADE #####

    ##### KNEE GOES UP AT SAME TIME AS HAND GRADE #####

    punjabKneeScore = punjabKneeAngle(punjabList) #currently not in use! Bit too inaccurate

    ###### Overall Score ######
    finalPunjabScore = (regScore/5)*2
    everything=punjabFeedback(angleScore,leftAngle,rightAngle,heightDiffScore,sameY, finalPunjabScore)
    return everything

def main():
    punjabList=punjab(hashtable)
    final=gradePunjab(punjabList)
    return final

# print(yello)  
# print ("length of punjab=", len(yello))      

# print("start of test")
# print(gradePunjab(yello))
# print("it worked")






