import sys
import numpy as np
import cv2

def formMaskbyPerimetr(base_perimetr, mask, contours, hierarchy):
    for i, cnt in enumerate(contours):
        # Якщо в об'єкта є дочірні елементи, виводимо білим
        if(hierarchy[0][i][2] != -1):
            perimetr = cv2.arcLength(cnt, True)
            if (perimetr > base_perimetr):
                cv2.drawContours(mask, [cnt], 0, (255), -1)

        # Якщо в об'єкта нема дочірніх елементів і він сам є дочірнім елементом, виводимо чорним
        if (hierarchy[0][i][2] == -1 and hierarchy[0][i][3] != -1):
            perimetr = cv2.arcLength(cnt, True)
            print(perimetr)
            if (perimetr > base_perimetr):
                cv2.drawContours(mask, [cnt], 0, (0), -1)

        # Всі інші, виводимо білим
        else:
            perimetr = cv2.arcLength(cnt, True)
            print(perimetr)
            if (perimetr > base_perimetr):
                cv2.drawContours(mask, [cnt], 0, (255), -1)

    return mask

if __name__ == '__main__':
    fn = 'images/image.png'
    img = cv2.imread(fn)

    # Конвертуємо в РГБ
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Конвертуємо в Сірий
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Отримуємо массив з контурів та ієрархію елементів
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    image = cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    cv2.imshow('Contours', image)
    cv2.waitKey(0)

    # Create a black mask, shape like original img
    mask = np.zeros(img.shape[:2], dtype=img.dtype)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)

    reform_mask = formMaskbyPerimetr(800, mask, contours, hierarchy)

    cv2.imshow('Result', reform_mask)
    cv2.waitKey(0)
