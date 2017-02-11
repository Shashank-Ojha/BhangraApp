import math
from pickle import load
hashtable=load(open("RiyaDD2.pkl","rb"))

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

def almostEqual(x, y, epsilon = 10**-2):
    return abs(x-y) < epsilon


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
                    dhammalList.append([(rightHandList[j], leftHandList[j], rightElbowList[j], leftElbowList[j], rightShoulderList[j], leftShoulderList[j], neckList[j], chestList[j], bundList[j],
                leftHipList[j], leftKneeList[j], leftFootList[j], rightHipList[j],rightKneeList[j], rightFootList[j])])
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




def gradeDhammal(dhammalList):
    #first grade if knee is over hip
    #f : 0 to negative
    #d: 0 to 5
    #c: 5-10
    #b: 10-15
    #a: 15-30


    #grade arms same height
purpl=dhammal(hashtable)
print(purpl)
print("length of dhammal=", len(purpl))



