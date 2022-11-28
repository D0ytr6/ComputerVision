import sys
import numpy as np
import cv2

fn = 'images/image_holes.png'
img = cv2.imread(fn)

def getTriangleCircleLine(vertical:list, horizontal: list, approx_polygons, shapes_count: int):
    if len(vertical) != 0:
        vertical = []
    if len(horizontal) != 0:
        horizontal = []

    topdot_y = bottomdot_y = topdot_x = left_x = right_x  = 0
    i = 0
    for j in approx_polygons:
        if (i % 2 == 0):
            x = approx_polygons[i]
            y = approx_polygons[i + 1]
            string = str(x) + " " + str(y)
            cv2.putText(img, string, (x, y), font, 0.5, (0, 255, 0))
            if y > bottomdot_y:
                bottomdot_y = y

            if topdot_y == 0:
                topdot_y = y
                topdot_x = x
            if y < topdot_y:
                topdot_y = y
                topdot_x = x

            if left_x == 0:
                left_x = x

            if left_x > x:
                left_x = x

            if right_x == 0:
                right_x = x

            if right_x < x:
                right_x = x

        i = i + 1

    if shapes_count == 32 or shapes_count == 10:
        middle_left_x = left_x
        middle_right_x = right_x

    elif shapes_count == 8:
        middle_left_x = int(right_x / 2) # just middle x
        middle_right_x = int(bottomdot_y / 2) # just middle y

    else:
        middle_left_x = int((topdot_x + left_x) / 2)
        middle_right_x = int((topdot_x + right_x) / 2)

    middle_y = int((topdot_y + bottomdot_y) / 2)

    # Add vertical coordinate of lines
    if shapes_count != 8:
        vertical_line.append((topdot_x, topdot_y))
        vertical_line.append((topdot_x, bottomdot_y))
        horizontal_line.append((middle_left_x, middle_y))
        horizontal_line.append((middle_right_x, middle_y))

    else:
        vertical_line.append((middle_left_x, topdot_y))
        vertical_line.append((middle_left_x, bottomdot_y))
        horizontal_line.append((left_x, middle_right_x))
        horizontal_line.append((right_x, middle_right_x))

    return vertical_line, horizontal_line

if __name__ == '__main__':
    # Конвертуємо в РГБ
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Конвертуємо в Сірий
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Create a black mask, shape like original img
    mask = np.zeros(img.shape[:2], dtype=img.dtype)
    # cv2.imshow('mask', mask)
    # cv2.waitKey(0)

    font = cv2.FONT_HERSHEY_COMPLEX

    list_contoures = []
    obj_kids_count = {}
    draw_cont = []
    list_hierarchy = []
    # Отримуємо массив з контурів та ієрархію елементів
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for i, cnt in enumerate(contours):
        if i != 0 and hierarchy[0][i][2] != -1:
            list_contoures.append(cnt)

        if i != 0 and hierarchy[0][i][2] == -1 and hierarchy[0][i][3] != -1 and hierarchy[0][i][3] != 0:
            if obj_kids_count.get(hierarchy[0][i][3]):
                obj_kids_count[hierarchy[0][i][3]] += 1
            else:
                obj_kids_count[hierarchy[0][i][3]] = 1

    for i, cnt in enumerate(contours):
        for parent in obj_kids_count.keys():
            if obj_kids_count[parent] == 1:
                if i == parent:
                    list_hierarchy.append(hierarchy[0][i])
                    draw_cont.append(cnt)
                #
                # elif hierarchy[0][i][3] == parent:
                #     draw_cont.append(cnt)

    msg = f"Total objects with holes: {len(list_contoures)}    Total objects with 1 hole: {len(draw_cont)}"
    cv2.putText(img, msg, (10, 15), cv2.FONT_HERSHEY_PLAIN, 1.3, (0, 0, 255), 1, cv2.LINE_AA)

    # Going through every contours found in the image.


    for cnt in list_contoures:

        # get cnt, contour lenght, true if contour closed
        # return shape polygons
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)

        # draws boundary of contours.
        cv2.drawContours(img, [approx], 0, (0, 0, 255), 5)

        # Used to flatted the array containing
        # return the co-ordinates of the vertices.
        approx_polygons = approx.ravel()

        vertical_line = []
        horizontal_line = []

        # triangle
        if len(approx_polygons) == 6:
            vertical_line, horizontal_line = getTriangleCircleLine(vertical_line, horizontal_line, approx_polygons, len(approx_polygons))
            img = cv2.line(img, vertical_line[0], vertical_line[1], color=(0, 255, 0), thickness=9)
            img = cv2.line(img, horizontal_line[0], horizontal_line[1], color=(0, 255, 0), thickness=9)

        if len(approx_polygons) == 32:
            vertical_line, horizontal_line = getTriangleCircleLine(vertical_line, horizontal_line, approx_polygons, len(approx_polygons))
            img = cv2.line(img, vertical_line[0], vertical_line[1], color=(0, 255, 0), thickness=9)
            img = cv2.line(img, horizontal_line[0], horizontal_line[1], color=(0, 255, 0), thickness=9)

        if len(approx_polygons) == 10:
            vertical_line, horizontal_line = getTriangleCircleLine(vertical_line, horizontal_line, approx_polygons, len(approx_polygons))
            img = cv2.line(img, vertical_line[0], vertical_line[1], color=(0, 255, 0), thickness=9)
            img = cv2.line(img, horizontal_line[0], horizontal_line[1], color=(0, 255, 0), thickness=9)

        # if len(approx_polygons) == 8:
        #     vertical_line, horizontal_line = getTriangleCircleLine(vertical_line, horizontal_line, approx_polygons, len(approx_polygons))
        #     img = cv2.line(img, vertical_line[0], vertical_line[1], color=(0, 255, 0), thickness=9)
        #     img = cv2.line(img, horizontal_line[0], horizontal_line[1], color=(0, 255, 0), thickness=9)


    # # Showing the final image.
    cv2.imshow('image2', img)
    cv2.waitKey(0)
