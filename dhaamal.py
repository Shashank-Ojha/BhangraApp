import math
from pickle import load
hashtable=load(open("TegBadDump.pkl","rb"))

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

def almostEqual(x, y, epsilon = 10**-1):
    return abs(x-y) < epsilon

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

def getDhammals(leftKneeDistances,rightKneeDistances,hashtable):
    #one DOUBLE dhammal is left knee up down then right before up again
    for i in range(1,len(leftKneeDistances)): #y distances
        if delta(leftKneeDistances[i-1], leftKneeDistances[i])>0:
            leftKneeDistances[i-1]=1 #means up 
        else:
            leftKneeDistances[i-1]=-1 #down
        # if delta(rightKneeDistances[i-1], rightKneeDistances[i])>0:
        #     rightKneeDistances[i-1]=1
        # else:
        #     rightKneeDistances[i-1]=-1 #down
    leftKneeDistances.pop() #base everything off of left knee
    print("leftKneeDistances=", leftKneeDistances)
    SERIESLEN=6 #longer than punjab because double dhammal
    dhammalList=[]  #this is wack  [ [((),(),()),((),(),())], [((),(),()),((),(),())] ]
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
    for i in range(len(leftKneeDistances)-SERIESLEN):
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
        if (leftKneeDistances[i]==1 and leftKneeDistances[i+1:i+SERIESLEN+1]==[1]*SERIESLEN):
            dhammalList.append([(rightHand, leftHand, rightElbow,leftElbow, rightShoulder, leftShoulder, neck, chest,bund,
                leftHip, leftKnee, leftFoot, rightHip,rightKnee, rightFoot)])
            j=i
            while (j<len(leftKneeDistances)-SERIESLEN): 
                if seenNegOnes and leftKneeDistances[j+1:j+1+SERIESLEN]==[1]*SERIESLEN:
                    #we are done
                    dhammalList.append([(rightHandList[j+1], leftHandList[j+1], rightElbowList[j+1], leftElbowList[j+1], rightShoulderList[j+1], leftShoulderList[j+1], neckList[j+1], chestList[j+1], bundList[j+1],
                leftHipList[j+1], leftKneeList[j+1], leftFootList[j+1], rightHipList[j+1],rightKneeList[j+1], rightFootList[j+1])])
                    seenNegOnes=False
                    continue
                if leftKneeDistances[j:j+SERIESLEN]==[-1]* SERIESLEN:
                    seenNegOnes=True

                dhammalList[-1].append((rightHandList[j], leftHandList[j], rightElbowList[j], leftElbowList[j], rightShoulderList[j], leftShoulderList[j], neckList[j], chestList[j], bundList[j],
                leftHipList[j], leftKneeList[j], leftFootList[j], rightHipList[j],rightKneeList[j], rightFootList[j]))
                j+=1
            dhammalList.pop()
            break
    return dhammalList


def dhammal(hashtable): #want to separate dhammals
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
    leftKneeDistances=[]
    rightKneeDistances=[]
    for i in range(len(leftKneeList)): #for every moment in time
        #(x,y,z,t) tuple
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
        leftKneeToFloor=leftKnee[1] #integer value of y distance
        rightKneeToFloor=rightKnee[1]
        leftKneeDistances.append(leftKneeToFloor)
        rightKneeDistances.append(rightKneeToFloor)
    dhammalList=getDhammals(leftKneeDistances,rightKneeDistances,hashtable)
    return dhammalList


def dhammalArms(dhammalList):
    def almostEqual(x, y, marginError):
        return abs(x-y) < marginError

    penalties=0
    countMoments=0
    MARGINERROR=10**-1
    #grade arms same height
    for oneDhammal in dhammalList:
        for moment in oneDhammal:
            rightHand=moment[0]
            leftHand=moment[1]
            (xr, yr, zr, tr)=rightHand
            (xl, yl, zl, tl)=leftHand
            print("yr=", yr)
            print("yl=", yl)
            print("yr-yl=", yr-yl)
            if not almostEqual(yr, yl,MARGINERROR):
                #penalize
                penalties+=1
            countMoments+=1
    percentageRight=(countMoments-penalties)/countMoments
    return percentageRight

def dhammalKneeAngle(dhammalList):
    MARGINERROR=10 #degrees
    def almostEqual(x, y, marginError):
        return abs(x-y) < marginError
    #need vector from hip knee
    #need vector from knee to foot
    #calculate angle between those vecotrs
    STDEV=6
    penalties=0
    countDhammals=0
    for oneDhammal in dhammalList:
        #only take first few positions
        #high point happens at 1/3 of oneDhammal
        for i in range(round(.33*len(oneDhammal)), round(.33*len(oneDhammal))+STDEV):
            moment=oneDhammal[i]
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
    percentageRight=(countDhammals-penalties)/countDhammals
    return percentageRight

def kneeAboveHip(dhammalList):
    maxPos = []
    score = 0
    for dhammal in dhammalList:
        x = round(len(dhammal)/3)
        maxPos.append(dhammal[x])
    print(maxPos)
    for i in maxPos:
        hipCoordsL = i[9]
        kneeCoordsL = i[10]
        hip_y = hipCoordsL[1]
        knee_y = kneeCoordsL[1]
        if knee_y>hip_y:
            score+=1
        elif almostEqual(knee_y, hip_y):
            score +=0.5
        else:
            continue
    return score/len(maxPos)
    

def giveKneeAngleFeedback(percentageKneeAngle):
    if percentageKneeAngle<.75:
        feebackF=["Try to drive up with your knee more!", 
        "Try to keep your feet directly below your knee at the max point of dhaamal!",
         "Keep trying for the 90 degree angle between your knee and your foot!"]
        feedback=feebackF[random.randint(0,2)]
    if percentageKneeAngle<.92:
        feedbackA = ["Your knee is almost there! Keep trying for 90 degrees!", "Good job! Continue driving up with your knees!"]
        feedback=feedbackA[random.randint(0,1)]
    else: 
        feedback="Great work! Your dhammal knee angle looks great! Keep it up!"
    return feedback
def giveKneeHeightFeedback(percentageKneeHeight):
    if percentageKneeHeight<.75:
        feedbackF=["Try to get your knee above your hips--it might help to lean backwards a bit!", "Drive with your knee to get it above your hip!"]
        feedback=feedbackF[random.randint(0,1)]
    if percentageKneeHeight<.92:
        feedbackA=[ "Your knee height is almost there! Try to keep it consistently above your hip.", "Keep driving with your knee to keep it above your hip!"]
        feedback=feedbackA[random.randint(0,1)]
    else: 
        feedback="Your dhaamal knee height is good! Keep up the good form!"

def feedbackDhammal(percentageKneeAngle, percentageDhammalArms,percentageKneeHeight):
    kneeAngleFeedback=giveKneeAngleFeedback(percentageKneeAngle)
    armFeedback=giveArmFeedback(percentageDhammalArms)
    kneeHeightFeedback=giveKneeHeightFeedback(percentageKneeHeight)
    shouldersFeedback="Don't forget to always get that shoulder bounce!"
    proTipFeedback="Pro Tip: On double dhammal, try to get a dip on every odd beat!"
    return (kneeAngleFeedback + "\n" + armFeedback + "\n" +kneeHeightFeedback+"\n"+ shouldersFeedback+"\n"+proTipFeedback)
def gradeDhammal(dhammalList): 
    #reutnrs a percentage like .95
    percentageKneeAngle=dhammalKneeAngle(dhammalList) #weight 2
    percentageDhammalArms=dhammalArms(dhammalList)  #weight 1
    percentageKneeHeight=kneeAboveHip(dhammalList) #weight 2
    
    feedbackDhammal(percentageKneeAngle, percentageDhammalArms,percentageKneeHeight)

    #give weights
    total=round((2*percentageKneeAngle+percentageDhammalArms+2*percentageKneeHeight)*2, 1) #will give a number like 9.8
    return total

purpl=dhammal(hashtable)
print(purpl)
print("length of dhammal=", len(purpl))
print(gradeDhammal(purpl))





