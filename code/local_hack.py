import requests
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO
import os
from cv2 import *
from time import sleep
import pygame
from Tkinter import *
import random


def helloCallBack(): 
    cam = VideoCapture(0)
    sleep(1)
    retval, frame = cam.read()
    if retval != True:
       raise ValueError("Can't read frame")
    imwrite(r"/Users/kendallmccormick/documents/hackathon/test.jpg", frame)


    # If you are using a Jupyter notebook, uncomment the following line.
    #%matplotlib inline

    # Replace <Subscription Key> with your valid subscription key.
    subscription_key = "cc259cf192144247b87f31f0fa16adbb" #DSFace API
    assert subscription_key
    face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
    headers = {'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    image_path = os.path.join('/Users/kendallmccormick/documents/hackathon/test.jpg')
    image_data = open(image_path, "rb")
    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    faces = response.json()
    # Display the original image and overlay it with the face information.
    image_read = open(image_path, "rb").read()
    image = Image.open(BytesIO(image_read))
    w,h=image.size
    plt.figure(figsize=(8, 8))
    ax = plt.imshow(image, alpha=1)

    anger = 0
    contempt = 0
    disgust = 0
    fear = 0
    happiness = 0
    neutral = 0
    sadness = 0
    surprise = 0

    for face in faces:
        fr = face["faceRectangle"]
        fa = face["faceAttributes"]
        origin = (fr["left"], fr["top"])
        em=fa['emotion']
        s = [(k, em[k]) for k in sorted(em, key=em.get, reverse=True)]

        anger+= em['anger']
        contempt+= em['contempt']
        disgust+= em['disgust']
        fear+= em['fear']
        happiness+= em['happiness']
        sadness+= em['sadness']
        surprise+= em['surprise']

        if em['neutral']>0.9:
            x=1
        else:
            x=0
        p = patches.Rectangle(
            origin, fr["width"], fr["height"], fill=False, linewidth=2, color='g')
        ax.axes.add_patch(p)
        plt.text(origin[0], origin[1]-h*0.15, "%s, %d"%(fa["gender"].capitalize(), fa["age"]), color='#0066CC',
                    fontsize=12, weight="bold", va="bottom")
        #plt.text(origin[0]+fr["width"], origin[1]-h*0.05, "%s, %s"%(s[0][0].capitalize(),"{0:.2f}%".format(s[0][1]*100)), color='#0066CC',
        #         fontsize=12, weight="bold", va="bottom")
        #plt.text(origin[0]+fr["width"], origin[1], "%s, %s" % (s[1][0].capitalize(), "{0:.2f}%".format(s[1][1] * 100)), color='#0066CC',
        #         fontsize=12, weight="bold", va="bottom")
        plt.text(origin[0], origin[1]-h*0.1, "%s"%(s[x][0].capitalize()), color='#0066CC',
                    fontsize=12, weight="bold", va="bottom")
        plt.text(origin[0], origin[1]-h*0.05, "%s" % (s[x+1][0].capitalize()), color='#0066CC',
                    fontsize=12, weight="bold", va="bottom")
        plt.text(origin[0], origin[1], "%s" % (s[x + 2][0].capitalize()), color='#0066CC',
                    fontsize=12, weight="bold", va="bottom")
        _ = plt.axis("off")
        plt.show()

    ems = [anger, contempt, disgust, fear, happiness, neutral, sadness, surprise]
    highest_index = 0
    highest = 0
    for i in range (0,len(ems)):
        if(ems[i]>highest):
            highest = ems[i]
            highest_index = i
    print("highest_index: ", highest_index)
    print("highest:", highest)

    seed = 0
    happy_file_paths = ["/Users/kendallmccormick/documents/hackathon/music/happy1.mp3", "/Users/kendallmccormick/documents/hackathon/music/happy2.mp3", "/Users/kendallmccormick/documents/hackathon/music/happy3.mp3", "/Users/kendallmccormick/documents/hackathon/music/happy4.mp3"]
    sad_file_paths = ["/Users/kendallmccormick/documents/hackathon/music/sad1.mp3"]
    angry_file_paths = ["/Users/kendallmccormick/documents/hackathon/music/angry1.mp3", "/Users/kendallmccormick/documents/hackathon/music/angry2.mp3"]
    contempt_file_paths = ["/Users/kendallmccormick/documents/hackathon/music/contempt1.mp3"]
    disgust_file_paths = ["/Users/kendallmccormick/documents/hackathon/music/disgust1.mp3"]
    surprise_file_paths = ["/Users/kendallmccormick/documents/hackathon/music/surprise1.mp3"]
    fear_file_paths = ["/Users/kendallmccormick/documents/hackathon/music/fear1.mp3"]

    #indices: 0:anger, 1: contempt, 2:disgust, 3:fear, 4:happiness, 5:neutral, 6:sadness, 7:surprise

    def play_song(seed, category_index):
        pygame.init()
        pygame.mixer.init()
        file = ""
        if(category_index==0):
            file = angry_file_paths[seed]
        elif(category_index == 1):
            file = contempt_file_paths[seed]
        elif(category_index == 2):
            file = disgust_file_paths[seed]
        elif(category_index == 3):
            file = fear_file_paths[seed]
        elif(category_index == 4 or category_index == 5):
            file = happy_file_paths[seed]
        elif(category_index == 6):
            file = sad_file_paths[seed]
        elif(category_index == 7):
            file = surprise_file_paths[seed]
        else:
            print("error", category_index)

        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


    play_song(seed= seed, category_index = highest_index)
    #print(faces)


root = Tk()

B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()
root.mainloop()