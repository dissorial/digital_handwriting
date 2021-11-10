import cv2
from draw_rect import select_rois, rect_endpoint_tmp, rect_bbox, refPt, drawing
import os
from PIL import Image
from skimage.color.colorconv import rgb2gray, rgba2rgb
from skimage.io import imread as skimread
from skimage.morphology import convex_hull_image
import numpy as np

     
def transform(image, height=None):
    dim = None
    (h, w) = image.shape[:2]
    r = height / float(h)
    dim = (int(w * r), height)

    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def manual_crop(destination_path, src_image, variations, chars):
    def clear(rect_endpoint_tmp_, rect_bbox_, refPt_, drawing_):
        rect_endpoint_tmp_.clear()
        rect_bbox_.clear()
        refPt_.clear()
        drawing_ = False

    idx = 0
    while idx < (len(chars)):
        try:
            for i in range(0, variations):
                clone = src_image.copy()
                print(f'Crop the letter {chars[idx]}: varation: {i+1}')
                roi_res = select_rois(clone)
                clear(rect_endpoint_tmp, rect_bbox, refPt, drawing)
                roi_image = clone[roi_res[1]:roi_res[3], roi_res[0]:roi_res[2]]
                cv2.imshow('crop_roi', roi_image)
                save_or_redo = cv2.waitKey(0)
                if save_or_redo == ord('s'):
                    cv2.destroyAllWindows()
                    cv2.imwrite(
                        f'{destination_path}/{i}_{ord(chars[idx])}.png',
                        roi_image)
                elif save_or_redo == ord('q'):
                    cv2.destroyAllWindows()
            clear(rect_endpoint_tmp, rect_bbox, refPt, drawing)
            idx += 1
        except Exception as e:
            print('Done')
            break


def autocrop(src_dir, dst_dir):
    for letterimage in os.listdir(f'{src_dir}'):
        im = skimread(f'{src_dir}/{letterimage}')
        im1 = 1 - rgb2gray(im)
        #im1 = 1 - rgb2gray(rgba2rgb(im))
        threshold = 0.5
        im1[im1 <= threshold] = 0
        im1[im1 > threshold] = 1
        chull = convex_hull_image(im1)
        imageBox = Image.fromarray((chull * 255).astype(np.uint8)).getbbox()
        cropped = Image.fromarray(im).crop(imageBox)
        cropped.save(f'{dst_dir}/{letterimage}')