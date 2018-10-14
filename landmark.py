from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

PREDICTOR = "shape_predictor_68_face_landmarks.dat"

def get_face_landmarks(image):

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 1)

    landmarks = []

    for (i, rect) in enumerate(rects):

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        landmarks.append(shape.tolist())

    return landmarks

