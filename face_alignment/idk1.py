import cv2
import dlib
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

image_path = r"test_image.jpg"
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = detector(gray)

for face in faces:
    landmarks = predictor(gray, face)

    left_eye = np.array([landmarks.part(36).x, landmarks.part(36).y])
    right_eye = np.array([landmarks.part(45).x, landmarks.part(45).y])
    
    dY = right_eye[1] - left_eye[1]
    dX = right_eye[0] - left_eye[0]
    angle = np.degrees(np.arctan2(dY, dX))

    center_x = int((left_eye[0] + right_eye[0]) / 2)
    center_y = int((left_eye[1] + right_eye[1]) / 2)
    eye_center = (center_x, center_y)
    
    M = cv2.getRotationMatrix2D(eye_center, angle, scale=1.0)
    rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)

    cv2.imshow("Original", img)
    cv2.imshow("Tegshilsen Tsarai", rotated_img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
