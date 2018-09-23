import requests
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO
import os
from cv2 import *
from time import sleep


if __name__ == '__main__':
    cam = VideoCapture(0)
    sleep(1)
    retval, frame = cam.read()
    if retval != True:
       raise ValueError("Can't read frame")
    imwrite(r"/Users/chinar/Desktop/Hackathon/test.jpg", frame)


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
image_path = os.path.join('/Users/chinar/Desktop/Hackathon/test.jpg')
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
for face in faces:
   fr = face["faceRectangle"]
   fa = face["faceAttributes"]
   origin = (fr["left"], fr["top"])
   em=fa['emotion']
   s = [(k, em[k]) for k in sorted(em, key=em.get, reverse=True)]
   p = patches.Rectangle(
       origin, fr["width"], fr["height"], fill=False, linewidth=2, color='g')
   ax.axes.add_patch(p)
   plt.text(origin[0], origin[1]-h*0.1, "%s, %d"%(fa["gender"].capitalize(), fa["age"]), color='#0066CC',
            fontsize=12, weight="bold", va="bottom")
   plt.text(origin[0], origin[1]-h*0.05, "%s, %s"%(s[0][0].capitalize(),"{0:.2f}%".format(s[0][1]*100)), color='#0066CC',
            fontsize=12, weight="bold", va="bottom")
   plt.text(origin[0], origin[1], "%s, %s" % (s[1][0].capitalize(), "{0:.2f}%".format(s[1][1] * 100)), color='#0066CC',
            fontsize=12, weight="bold", va="bottom")
_ = plt.axis("off")
plt.show()
print(faces)