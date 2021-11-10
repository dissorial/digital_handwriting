import click
from click.termui import prompt
from helperfuncs import getchars, average_height, get_position, get_words, start_new_line
from PIL import Image
from numpy import random
import cv2


@click.group()
def main():
    pass


@main.command()
@click.option('--src',
              prompt='Path to source directory of images',
              type=str,
              default='autocropped')
@click.option('--fname',
              prompt='Path to text file to convert',
              type=str,
              default='hand2text.txt')
@click.option('--bck',
              prompt='Path to handwriting background image',
              type=str,
              default='base/background.png')
@click.option('--lm', prompt='Left document margin', type=int, default=60)
@click.option('--rm', prompt='Right document margin', type=int, default=80)
@click.option('--tm', prompt='Top document margin', type=int, default=60)
@click.option('--letterspace',
              prompt='Spaces between letters',
              type=int,
              default=3)
@click.option('--linespace',
              prompt='Space between the lines',
              type=int,
              default=120)
@click.option('--variations',
              prompt='Number of variations per each character',
              type=int,
              default=1)
def handwriting(src, fname, bck, lm, rm, tm, linespace, variations,
                letterspace):
    mid = getchars('lowercase_mid.txt')
    mid_high = getchars('lowercase_high.txt')
    mid_low = getchars('lowercase_low.txt')
    upper = getchars('uppercase.txt')
    p_high = getchars('punctuation_high.txt')
    p_mid = getchars('punctuation_mid.txt')
    p_low = getchars('punctuation_low.txt')

    spacechar = cv2.imread('base/32.png')
    for x in range(variations):
        cv2.imwrite(f'autocropped/{x}_32.png', spacechar)

    avg_mid, avg_midlow, avg_midhigh, avg_pmid, avg_plow, avg_phigh, avg_upper = average_height(
        src, mid, mid_low, mid_high, p_mid, p_low, p_high, upper)
    # click.echo(f'Average of middle: {avg_mid}')
    # click.echo(f'Average of middle-low: {avg_midlow}')
    # click.echo(f'Average of middle-high: {avg_midhigh}')
    # click.echo(f'Average of pmid: {avg_pmid}')
    # click.echo(f'Average of plow: {avg_plow}')
    # click.echo(f'Average of phigh: {avg_phigh}')
    # click.echo(f'Average of upper: {avg_upper}')
    filename = fname

    try:
        txt = open(filename, "r")
    except (IndexError, FileNotFoundError) as e:
        print("Text file not found...")

    words = get_words(filename)

    BACKGROUND = Image.open(bck)
    sheet_width = BACKGROUND.width
    gap, space_between_lines = lm, tm
    index = 0
    word_index = 0
    for i in txt.read().replace("\n", ""):
        char_variation = random.randint(variations)
        index += 1
        letter = Image.open('{}/{}_{}.png'.format(src, char_variation,
                                                  str(ord(i))))
        c = f'{src}/{char_variation}_{i}.png'
        c_main = c.split('/')[1][2:-4]
        letter_width = letter.width
        letter_height = letter.height
        if i == ' ':
            word_index += 1
            try:
                if start_new_line(words[word_index], src, gap, sheet_width,
                                  char_variation, rm):
                    gap = int((lm / 3) +
                              ((lm / 3) * random.uniform(-0.5, 0.5)))
                    space_between_lines += linespace
                else:
                    pass
            except IndexError:
                ''
        pos = int(
            get_position(c_main, letter_height, avg_mid, avg_midlow,
                         avg_midhigh, avg_pmid, avg_plow, avg_phigh,
                         avg_upper))
        BACKGROUND.paste(letter, (gap, space_between_lines + pos))
        gap += letter_width + letterspace

    BACKGROUND.show()


if __name__ == "__main__":
    main()