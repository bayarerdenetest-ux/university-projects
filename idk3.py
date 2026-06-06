# LAB2 - Face Alignment
# File: idk6.py it means idk version 6
# Date: 2026-06-06
# Python: 3.10 or newer
# Tested with: Python 3.11.15
# Environment: Local Python interpreter, no virtual environment
# Purpose: Align CelebA face images using eye, nose, and mouth landmark points.
# Input: CelebA image folder and landmarks.txt.
# Output: Aligned face images saved in the output folder.
#the fastest and high accuracy version between idk1.py-idk6.py because it used dlib 
import cv2
import dlib
import numpy as np
import os
import argparse
from tqdm import tqdm

DEFAULT_INPUT_DIR   = r"test_image.jpg"
DEFAULT_OUTPUT_DIR  = r"test_image.jpg"
DEFAULT_PREDICTOR   = r"test_image.jpg"
DEFAULT_OUTPUT_SIZE = 256
DEFAULT_EYE_RATIO   = 0.35
DEFAULT_EXT         = (".jpg", ".jpeg", ".png", ".bmp", ".webp")



def get_eye_centers(landmarks):
    left_eye_pts  = np.array([[landmarks.part(i).x, landmarks.part(i).y]
                               for i in range(36, 42)], dtype=np.float64)
    right_eye_pts = np.array([[landmarks.part(i).x, landmarks.part(i).y]
                               for i in range(42, 48)], dtype=np.float64)
    return left_eye_pts.mean(axis=0), right_eye_pts.mean(axis=0)


def align_face(image, left_eye, right_eye, output_size=256, eye_ratio=0.35):
    dx = right_eye[0] - left_eye[0]
    dy = right_eye[1] - left_eye[1]
    angle = np.degrees(np.arctan2(dy, dx))

    eye_dist = np.sqrt(dx**2 + dy**2)
    desired_eye_dist = (1.0 - 2 * eye_ratio) * output_size
    scale = desired_eye_dist / (eye_dist + 1e-6)

    eyes_center = ((left_eye[0] + right_eye[0]) / 2,
                   (left_eye[1] + right_eye[1]) / 2)

    M = cv2.getRotationMatrix2D(eyes_center, angle, scale)

    tX = output_size * 0.5
    tY = output_size * eye_ratio
    M[0, 2] += (tX - eyes_center[0])
    M[1, 2] += (tY - eyes_center[1])

    aligned = cv2.warpAffine(image, M, (output_size, output_size),
                             flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_REPLICATE)
    return aligned


def process_directory(input_dir, output_dir, predictor_path,
                       output_size=256, eye_ratio=0.35):

    if not os.path.isfile(predictor_path):
        raise FileNotFoundError(f"Загвар олдсонгүй: {predictor_path}")

    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Хавтас олдсонгүй: {input_dir}")

    detector  = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)

    os.makedirs(output_dir, exist_ok=True)

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
        print(f"[!] {input_dir} хавтаст зураг олдсонгүй.")
        return

    print(f"[✓] {len(image_files)} зураг олдлоо. Тэгшилж эхэлж байна...")
    success = skip = fail = 0

    for fname in tqdm(image_files, desc="Тэгшилж байна", unit="зураг"):
        src_path = os.path.join(input_dir, fname)
        
        out_name = fname if fname.lower().endswith(DEFAULT_EXT) else fname + ".jpg"
        dst_path = os.path.join(output_dir, out_name)

        img_bgr = cv2.imread(src_path)
        if img_bgr is None:
            fail += 1
            continue

        img_rgb  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        faces = detector(img_gray, 1)
        if len(faces) == 0:
            resized = cv2.resize(img_bgr, (output_size, output_size))
            cv2.imwrite(dst_path, resized)
            skip += 1
            continue

        face  = max(faces, key=lambda r: r.width() * r.height())
        shape = predictor(img_gray, face)

        left_eye, right_eye = get_eye_centers(shape)

        aligned_rgb = align_face(img_rgb, left_eye, right_eye,
                                  output_size=output_size,
                                  eye_ratio=eye_ratio)

        aligned_bgr = cv2.cvtColor(aligned_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(dst_path, aligned_bgr)
        success += 1

    print(f"\n✅ Дууслаа!")
    print(f"   Амжилттай тэгшилсэн  : {success}")
    print(f"   Нүүр олдоогүй (resize): {skip}")
    print(f"   Алдаатай             : {fail}")
    print(f"   Гаралт хавтас        : {os.path.abspath(output_dir)}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Нүдний байрлалаар нүүрний зургийг тэгшилнэ."
    )
    parser.add_argument("--input",     default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output",    default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--predictor", default=DEFAULT_PREDICTOR)
    parser.add_argument("--size",      type=int,   default=DEFAULT_OUTPUT_SIZE)
    parser.add_argument("--eye_ratio", type=float, default=DEFAULT_EYE_RATIO)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process_directory(
        input_dir      = args.input,
        output_dir     = args.output,
        predictor_path = args.predictor,
        output_size    = args.size,
        eye_ratio      = args.eye_ratio,
    )
