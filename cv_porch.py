import cv2 as cv
import numpy as np
import os
import send_text
import time
import sys
import gpiozero

cap = cv.VideoCapture(0, cv.CAP_DSHOW)

whT = 320
confThreshold = 0.5
nmsThreshold = 0.2
pTime = 0

classModelWeightPath = "classes_models_weights/"
classPath = "classes/"
modelPath = "models/"
weightPath = "weights/"

# initialize the variables for 'watching' for situations
sentText = 0
watchFor = ['person', 'dog']

# Build classes
classesFiles = []
for files in os.walk(classModelWeightPath + classPath):
    #print(files)
    classesFiles.extend(files[2][:])

#append the full path
classesFiles = [classModelWeightPath + classPath + x for x in classesFiles]
#print(classesFiles)

# Build Models
modelsFiles = []
for files in os.walk(classModelWeightPath + modelPath):
    #print(files)
    modelsFiles.extend(files[2][:])

#append the full path
modelsFiles = [classModelWeightPath + modelPath + x for x in modelsFiles]
#print(modelsFiles)

# Build Weights
weightsFiles = []
for files in os.walk(classModelWeightPath + weightPath):
    #print(files)
    weightsFiles.extend(files[2][:])

#append the full path
weightsFiles = [classModelWeightPath + weightPath + x for x in weightsFiles]
#print(weightsFiles)

# create the class names files
classNames = []
for i in range(len(classesFiles)):
    with open(classesFiles[i], 'rt') as f:
        classNames.append(f.read().rstrip('\n').split('\n'))

#print(classNames)

# create the model and weight config files
modelConfiguration = []
modelConfiguration.extend(modelsFiles[:])
#print(modelConfiguration)

weightConfiguration = []
weightConfiguration.extend(weightsFiles[:])
#print(weightConfiguration)

## SET THE NETS
nets = []

for i in range(len(classesFiles)):
    nets.append(cv.dnn.readNetFromDarknet(modelConfiguration[i], weightConfiguration[i]))
    nets[i].setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    nets[i].setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# flash LED lights to indicate it is working
led = gpiozero.LED(17)

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)

def findObjects(outputs, img, classIndex):


    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []

    for det in outputs[0]:
        #print(det)
        scores = np.array(det[5:])
        classId = np.argmax(scores)
        confidence = scores[classId]
        if confidence > confThreshold:
            w, h = int(det[2] * wT), int(det[3] * hT)
            x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
            bbox.append([x, y, w, h])
            classIds.append(classId)
            confs.append(float(confidence))

    indices = cv.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

    # prints the rectangle and text on the found object
    for i in indices:
        i = i[0]
        box = np.array(bbox[i])
        x, y, w, h = box[0], box[1], box[2], box[3]
        # print(x,y,w,h)
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        cv.putText(img, f'{classNames[classIndex][classIds[i]].upper()} {int(confs[i] * 100)}%',
                   (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        # declare sentText as the global value
        if classNames[classIndex][classIds[i]] in watchFor:
            global sentText
            if sentText < 1:
                #print(classNames[classIndex][classIds[i]])
                # send the text message
                #newText = send_text.sendSMS()
                #newText.sendIt()
                sentText = 1
                cv.imwrite('photos/test.png', img)


while True:

    # take the current time
    cTime = time.time()
    # calculate the fms
    time_elapsed = cTime - pTime

    #capture the image
    success, img = cap.read()

    fps = 1 / (cTime - pTime)

    blob = cv.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)

    # loop through models
    for net in nets:
        net.setInput(blob)
        layersNames = net.getLayerNames()
        outputNames = [(layersNames[i[0] - 1]) for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(outputNames)

        findObjects(outputs, img, nets.index(net))

    cv.putText(img, str(int(fps)), (70, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    #set the previous time stamp
    pTime = cTime

    #print(int(fps))

    #show the image
    cv.imshow('Image', img)

    # break the loop if press 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break