import cv2
import dlib
import numpy as np
import os 

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

input_folder = r"test_image_folder.jpg"
output_folder = r"test_image_folder.jpg"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
all_files = os.listdir(input_folder)

counter = 0
for filename in all_files:
    if filename.lower().endswith(image_extensions):
        counter += 1

        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) ==0:
            save_path = os.path.join(output_folder, filename)
            cv2.imwrite(save_path, img)
            print(f"[{counter}] no face detected, saved originals: {filename}")
            continue

        face = faces [0]
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
        save_path = os.path.join(output_folder, filename)
        cv2.imwrite(save_path, rotated_img)
        
        if counter % 100 == 0:
            print (f"amjilttai tegshilee: {counter} zurag tegshilsen")
print ("buh zurag tegshilsen! suuliin havtasaa shalga.")
