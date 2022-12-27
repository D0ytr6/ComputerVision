import cv2
import cvzone
import os
import mediapipe as mp
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation

segmentor = SelfiSegmentation()

# initialize mediapipe
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

FRAME_COUNT = 500
save_path = 'D:/LabVideo/Result/'
bg_int = 0

for i in range(FRAME_COUNT + 1):
    final_str = "0000"
    bg_str = str(bg_int)
    # print(bg_str)

    if(len(bg_str) == 1):
        final_str = final_str[:3]

    if (len(bg_str) == 2):
        final_str = final_str[:2]

    if(len(bg_str) == 3):
        final_str = final_str[:1]

    final_str = final_str + bg_str + ".png"
    print(final_str)
    bg_int += 1

    imgBg = "images/background/" + final_str
    img_face = "images/face/" + final_str

    imgBg = cv2.imread(imgBg)
    img_face = cv2.imread(img_face)

    height, width, channel = img_face.shape

    # Конвертуємо в РГБ
    RGB = cv2.cvtColor(img_face, cv2.COLOR_BGR2RGB)

    # get selfie class
    results = selfie_segmentation.process(RGB)

    # extract segmented mask
    mask = results.segmentation_mask

    # show outputs
    # cv2.imshow("mask", mask)
    # cv2.imshow("Frame", img_face)

    # Повертаємо матрицю зображення розміром як маска, true, якщо значення пікселя більше 0,5
    condition = np.stack((results.segmentation_mask, ) * 3, axis=-1) > 0.5

    # resize the background image to the same size of the original frame
    imgBg = cv2.resize(imgBg, (width, height))

    # combine frame and background image using the condition
    output_image = np.where(condition, img_face, imgBg)

    cv2.imshow("Output", output_image)

    isWritten = cv2.imwrite("D:/LabVideo/Result/" + final_str, output_image)

    if isWritten:
        print('Image is successfully saved as file.')

    key = cv2.waitKey(0)
