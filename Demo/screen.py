import numpy as np
import cv2
from PIL import ImageGrab

#four character code object for video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,5.0,(1920,1080))

while True:
    img = ImageGrab.grab()
    img_np = np.array(img)

    frame = cv2.cvtColor(img_np,cv2.COLOR_BGR2RGB)
    cv2.imshow('Screen',frame)
    out.write(frame)

    if cv2.waitKey(1) == ord('q'):
        break
