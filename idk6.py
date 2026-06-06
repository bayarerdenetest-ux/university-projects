# LAB2 - Face Alignment
# File: idk6.py it means idk version 6
# Date: 2026-06-06
# Python: 3.10 or newer
# Tested with: Python 3.11.15
# Environment: Local Python interpreter, no virtual environment
# Purpose: Align CelebA face images using eye, nose, and mouth landmark points.
# Input: CelebA image folder and landmarks.txt.
# Output: Aligned face images saved in the output folder.
import cv2
import numpy as np
import os
import argparse 
from tqdm import tqdm

# INPUT_DIR is a string path to the CelebA image folder.
# Use CELEBA_INPUT_DIR so a personal local path is not saved in GitHub. But it might be already saved when you read this
DEFAULT_INPUT_DIR   = r"test_image.jpg"
# OUTPUT_DIR is a string path to the aligned output images folder.
DEFAULT_OUTPUT_DIR  = r"test_image.jpg"
# PREDICTOR_PATH is a string path to the LBF facial landmark model file.
DEFAULT_PREDICTOR = r"test_image.jpg"
# OUTPUT_SIZE is an integer pixel dimension for the output square image.
DEFAULT_OUTPUT_SIZE = 256
# EYE_RATIO is a float controlling vertical eye position in the output image.
DEFAULT_EYE_RATIO   = 0.35
# DEFAULT_EXT is a tuple of valid image file extensions to process.
DEFAULT_EXT         = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

# it was writen by Bayar-Erdene and that project is one of his first projects. Therefore it might be messy and confusing 

def get_eye_centers_cv2(landmarks):
    left_eye_pts  = landmarks[36:42] 
    right_eye_pts = landmarks[42:48]
    return left_eye_pts.mean(axis=0), right_eye_pts.mean(axis=0)

def align_face(image, left_eye, right_eye, output_size=256, eye_ratio=0.35):
    dx = right_eye[0] - left_eye[0]
    dy = right_eye[1] - left_eye[1]
    angle = np.degrees(np.arctan2(dy, dx))
    eye_dist = np.sqrt(dx**2 + dy**2)
    desired_eye_dist = (1.0 - 2 * eye_ratio) * output_size
    scale = desired_eye_dist / (eye_dist + 1e-6)
    eye_center = ((left_eye[0] + right_eye[0])/2, (left_eye[1] + right_eye[1])/2)
    M = cv2.getRotationMatrix2D(eye_center, angle, scale)
    tX = output_size * 0.5
    tY = output_size * eye_ratio
    M[0, 2] += (tX - eye_center[0])
    M[1, 2] += (tY - eye_center[1])
    aligned = cv2.warpAffine(image, M, (output_size, output_size), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return aligned

def process_directory(input_dir,out_dir, predictor_path, output_size = 256, eye_ratio = 0.35):
    if not os.path.isfile(predictor_path):
        raise FileNotFoundError(f"Zagvar oldsongui: {predictor_path}")
        
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"havtas oldsongui: {input_dir}")
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    facemark = cv2.face.createFacemarkLBF()
    facemark.loadModel(predictor_path)

    os.makedirs(out_dir, exist_ok=True )
    image_files = []
    for f in os.listdir(input_dir):
        full_path = os.path.join(input_dir, f)
        if not os.path.isfile(full_path):
            continue
        if f.lower().endswith(DEFAULT_EXT):
            image_files.append(f)
        elif '.' not in f:
            img_test = cv2.imread(full_path)
            if img_test is not None:
                image_files.append(f)
    
    if not image_files:
        print(f"[!] {input_dir} havtas zurag oldsongui.")
        return
    print(f"[]{len(image_files)} zurag oldloo. tegshilj bain huleene uu ")
    success = skip = fail = 0
    
    for fname in tqdm(image_files, desc="tegshilj bain ", unit="zurag"):
        src_path = os.path.join(input_dir, fname)
        out_name = fname if fname.lower().endswith(DEFAULT_EXT) else fname + ".jpg"
        dst_path = os.path.join(out_dir, out_name)  
        img_bgr = cv2.imread(src_path)
        if img_bgr is None:
            fail += 1
            continue
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            skip += 1
            continue
        ok, landmarks = facemark.fit(img_gray, np.array([faces[0:1]]))
        left_eye, right_eye = get_eye_centers_cv2(landmarks[0][0])

        aligned_rgb = align_face(img_rgb, left_eye, right_eye, output_size=output_size, eye_ratio=eye_ratio)
        aligned_bgr = cv2.cvtColor(aligned_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(dst_path, aligned_bgr)
        success += 1
    print(f"\n duuslaa!")
    print(f"   amjilttai tegshilee: {success}")
    print(f"   no face detected: {skip}")
    print(f"   aldaa: {fail}")
    print(f"   garalt havtas : {os.path.abspath(out_dir)}")

def parse_args():
    parser = argparse.ArgumentParser(description="nudnii bairlalaar zurgiig tegshilne")
    parser.add_argument("--input", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--predictor", default=DEFAULT_PREDICTOR)
    parser.add_argument("--size", type=int, default=DEFAULT_OUTPUT_SIZE)
    parser.add_argument("--eye_ratio", type=float, default=DEFAULT_EYE_RATIO)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    process_directory(
        input_dir      = args.input,
        out_dir     = args.output,
        predictor_path = args.predictor,
        output_size    = args.size,
        eye_ratio      = args.eye_ratio,
    )
