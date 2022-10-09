import cv2
import mediapipe as mp
import pyautogui

# to turn on the camera.
cam = cv2.VideoCapture(0)
# to detect the face and eyes.
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

while True:
    _, frame= cam.read()
    #to flip the frame
    frame = cv2.flip(frame, 1)
    # selecting and changing the color we want to be shown.
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # creating the output from this rgb frame by using face_mesh.
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    #to get the frame width and hieght
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        #why putting enumerate? 1. it will give the id or the index; 2.the element or the landmark. because we mneed to pick one land mark to detect the movement and connect to the curser.
        for id, landmark in enumerate(landmarks[474:478]):
            #when you give a range of landmarks it will only show the things inside that range.
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            #asking cv2 to draw the cirsle around the face which is detected. ( where to draw-in the frame, where is the center, radius of the circle, what id the color of the landmark)
            cv2.circle(frame, (x,y) , 3 , (0,255,0))

            if id == 1:
                #to get the curser to move on the whole screen with the eye
                screen_x = int(screen_w/ frame_w * x)
                screen_y = int(screen_h / frame_h * y)
                pyautogui.moveTo(screen_x, screen_y)

        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left[0].y - left[1],y) < 0.004:
            print("click")
        print(left[0].y - left[1].y)

    cv2.imshow("Eyes Control The Mouse", frame)
    cv2.waitKey(1)
