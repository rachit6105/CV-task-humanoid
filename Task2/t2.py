import cv2
import numpy as np
# from google.colab.patches import cv2_imshow

ball = []
speeds = []
cap = cv2.VideoCapture(r'C:\Users\91820\OneDrive\Desktop\huma\newtas\hehe.mp4')
cap.set(cv2.CAP_PROP_FPS, 10)
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
   
size = (frame_width, frame_height) 
out = cv2.VideoWriter('newtas/output.avi',cv2.VideoWriter_fourcc(*'MJPG'),cap.get(cv2.CAP_PROP_FPS), size) 


def fit_circle(centers):
    centers = np.array(centers)
    (x, y), radius = cv2.minEnclosingCircle(centers)
    return (int(x), int(y)), int(radius)


while cap.isOpened():
  ret, frame = cap.read()
  if ret is False:
    print("Error")
    break
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  lower_hue = np.array([78,158,124])
  upper_hue = np.array([138,255,255])
  mask = cv2.inRange(hsv,lower_hue, upper_hue)

  (contours,_)=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  center = None

  if len(contours)>0:
    c = max(contours, key=cv2.contourArea)
    ((x,y),radius) = cv2.minEnclosingCircle(c)
    try:
      cv2.circle(frame, (int(x), int(y)),10, (255,0,0),-1)
      ball.append((int(x), int(y)))
    except:
      print('No circle')
      pass


    if len(ball)>2:
      for i in range(1,len(ball)):
        cv2.line(frame, ball[i-1], ball[i],(0,0,255),1)
    a,c=fit_circle(ball)
    cv2.circle(frame,a,c, (255,0,0),10)
    time_interval=1/10


    if len(ball)>2:
        prev_center=ball[-2]
        current_center=ball[-1]
    # Calculate distance between current center and previous center
        distance = np.sqrt((current_center[0] - prev_center[0])**2 + (current_center[1] - prev_center[1])**2)
        # Calculate speed
        speed = distance / (c*time_interval)
        speeds.append(speed)
    else:
        speeds.append(0)  # Speed is zero for the first frame
    for i, speed in enumerate(speeds):
        backspaces = '\b' * 80
        print(f"{backspaces}\rFrame: {i}, Speed: {speeds[-1]:.2f} rad/sec", end='', flush=True)
  cv2.imshow('hehe',frame)
  cv2.waitKey(10)
  out.write(frame)
out.release()
  