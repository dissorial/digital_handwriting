import os
import cv2
import PIL
from PIL import Image
from numpy import mean
import itertools
import numpy as np


def getchars(path_to_file):
    with open(f'txtsplit/{path_to_file}', 'r') as f:
        lines = f.readlines()
    return [c for c in lines[0]]


def average_height(src, mid, midlow, midhigh, pmid, plow, phigh, upper):
    h_mid = []
    h_midlow = []
    h_midhigh = []
    p_mid = []
    p_low = []
    p_high = []
    uppercase = []

    for letterimage in os.listdir(f'{src}'):
        temp_height = []
        img = cv2.imread(f'{src}/{letterimage}')
        img_height, img_width, _ = img.shape
        temp_height.append(img_height)
        character = chr(int(letterimage[2:-4]))

        if character in mid:
            h_mid.append(temp_height)

        elif character in midlow:
            h_midlow.append(temp_height)

        elif character in midhigh:
            h_midhigh.append(temp_height)

        elif character in pmid:
            p_mid.append(temp_height)

        elif character in plow:
            p_low.append(temp_height)

        elif character in phigh:
            p_high.append(temp_height)

        elif character in upper:
            uppercase.append(temp_height)

    h_mid = np.round(mean(list(itertools.chain.from_iterable(h_mid))), 0)
    h_midlow = np.round(mean(list(itertools.chain.from_iterable(h_midlow))), 0)
    h_midhigh = np.round(mean(list(itertools.chain.from_iterable(h_midhigh))),
                         0)
    p_mid = np.round(mean(list(itertools.chain.from_iterable(p_mid))), 0)
    p_low = np.round(mean(list(itertools.chain.from_iterable(p_low))), 0)
    p_high = np.round(mean(list(itertools.chain.from_iterable(p_high))), 0)
    uppercase = np.round(mean(list(itertools.chain.from_iterable(uppercase))),
                         0)

    return h_mid, h_midlow, h_midhigh, p_mid, p_low, p_high, uppercase


def get_position(character, img_height, avg_mid, avg_midlow, avg_midhigh,
                 avg_pmid, avg_plow, avg_phigh, avg_upper):

    mid = getchars('lowercase_mid.txt')
    mid_high = getchars('lowercase_high.txt')
    mid_low = getchars('lowercase_low.txt')
    upper = getchars('uppercase.txt')
    p_high = getchars('punctuation_high.txt')
    p_mid = getchars('punctuation_mid.txt')
    p_low = getchars('punctuation_low.txt')
    p_small = getchars('punctuation_small.txt')
    pepe = avg_midhigh > avg_upper

    # if character == 'i' or character == 'j':
    #     return ((avg_midhigh + avg_upper) / 2) / 3

    if character in mid or character in mid_low:
        return avg_midhigh - avg_mid

    elif character in upper:
        if pepe:
            return (avg_midhigh - avg_upper)
        else:
            return 0

    elif character in mid_high:
        if pepe:
            return 0
        else:
            return (avg_midhigh - avg_upper)

    elif character in p_low:
        #return ((avg_midhigh + avg_upper) / 2)
        return max(avg_upper, avg_midhigh) + (img_height / 2)

    elif character in mid:
        return avg_upper - avg_mid

    elif character in p_mid or character in p_high:
        return abs(avg_upper - avg_midhigh)

    elif character in p_small:
        return min(avg_upper, avg_midhigh) / 2

    else:
        return 0


def get_words(textfile_path):
    text = open(f'{textfile_path}', 'r')
    words = []
    for word in text.read().split():
        words.append(word)
    return words


def start_new_line(word, src_dir, line_width, canvas_width, var, rm):
    word_chars = [c for c in word]
    word_width = 0
    for char in word_chars:
        img = cv2.imread(f'{src_dir}/{var}_{ord(char)}.png')
        word_width += img.shape[1]
    if line_width + word_width <= canvas_width - rm:
        return False
    else:
        return True


def resize_images_height(source_directory, destination_directory, height):
    for pngfile in os.listdir(source_directory):
        img = Image.open(f'{source_directory}/{pngfile}')
        hpercent = (height / float(img.size[0]))
        wsize = int((float(img.size[1]) * float(hpercent)))
        img = img.resize((wsize, height), PIL.Image.ANTIALIAS)
        img.save(f'{destination_directory}/{pngfile}'.format(
            destination_directory, pngfile))


def resize_images_width(source_directory, destination_directory, width):
    for pngfile in os.listdir(source_directory):
        img = Image.open(f'{source_directory}/{pngfile}')
        wpercent = (width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width, hsize), PIL.Image.ANTIALIAS)
        img.save(f'{destination_directory}/{pngfile}'.format(
            destination_directory, pngfile))
