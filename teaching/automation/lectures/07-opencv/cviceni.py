# %%

import cv2 as cv
from matplotlib import pyplot as plt
 # %%

microskop = cv.imread(r'C:\Users\cermak\Downloads\potato\positive\L_6.jpg')
microskop = cv.cvtColor(microskop, cv.COLOR_BGR2RGB)
gray = cv.cvtColor(microskop, cv.COLOR_BGR2GRAY)

# %%
#gray = cv.equalizeHist(gray)
haar_cascade = cv.CascadeClassifier(r'C:\Users\cermak\Downloads\potato\cascade\cascade.xml')
faces_rect = haar_cascade.detectMultiScale(
  gray, scaleFactor=1.06, minNeighbors=2)
for (x,y,w,h) in faces_rect:
    cv.rectangle(microskop, (x,y), (x+w,y+h), 
                 (0,255,0), thickness=2)

print(f'Nalezeno {len(faces_rect)} objektů.')
plt.figure(figsize=(8,6)); 
plt.imshow(microskop)
plt.axis('off')
plt.show()


# %%
