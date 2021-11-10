import cv2

rect_endpoint_tmp = []
rect_bbox = []
refPt = []
drawing = False


def select_rois(img):
    def draw_rect_roi(event, x, y, flags, param):
        global rect_bbox, rect_endpoint_tmp, drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            rect_endpoint_tmp = []
            rect_bbox = [(x, y)]
            drawing = True
        elif event == cv2.EVENT_LBUTTONUP:
            rect_bbox.append((x, y))
            drawing = False
            p_1, p_2 = rect_bbox
            cv2.rectangle(img, p_1, p_2, color=(0, 255, 0), thickness=1)
            cv2.imshow('image', img)
            p_1x, p_1y = p_1
            p_2x, p_2y = p_2
            lower_x = min(p_1x, p_2x)
            lower_y = min(p_1y, p_2y)
            upper_x = max(p_1x, p_2x)
            upper_y = max(p_1y, p_2y)
            if (lower_x, lower_y) != (upper_x, upper_y):
                bbox = [lower_x, lower_y, upper_x, upper_y]
                refPt.append(bbox)
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            rect_endpoint_tmp = [(x, y)]

    img_copy = img.copy()
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rect_roi)
    keep_open = True
    while keep_open and True:
        if not drawing:
            cv2.imshow('image', img)
        elif drawing and rect_endpoint_tmp:
            rect_cpy = img.copy()
            start_point = rect_bbox[0]
            end_point_tmp = rect_endpoint_tmp[0]
            cv2.rectangle(rect_cpy, start_point, end_point_tmp, (0, 255, 0), 1)
            cv2.imshow('image', rect_cpy)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"):
            img = img_copy.copy()
        if key == ord('q'):
            keep_open = False
            cv2.destroyAllWindows()
        if key == ord('c'):
            break
    cv2.destroyAllWindows()
    return refPt[0]
