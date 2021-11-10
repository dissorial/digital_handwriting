import click
from click.termui import prompt
import cv2
from helperfuncs import getchars
from crop_utils import autocrop, manual_crop, transform


@click.group()
def main():
    pass


@main.command()
@click.option('--src',
              help='Image path',
              prompt='Image path',
              type=str,
              required=True)
@click.option('--height',
              help='Desired image height in pixels',
              type=int,
              prompt='Desired image height in pixels',
              required=False,
              default=1000)
def transform_image(src, height):
    image = cv2.imread(src)
    resized = transform(image, height)
    cv2.namedWindow('image')
    cv2.imshow('image', resized)

    wait_time = 1000
    prop = cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE)
    while prop >= 1:
        keyCode = cv2.waitKey(wait_time)
        #if (keyCode & 0xFF) == ord("q"):
        if cv2.waitKey(0):
            cv2.destroyAllWindows()
            cont = click.prompt(
                '[c] Continue and save or [r] rescale the image again?',
                type=click.Choice(['c', 'r']))
            if cont == 'r':
                new_height = click.prompt('Height in pixels', type=int)

                resized = transform(image, new_height)
                cv2.namedWindow('resized')
                cv2.imshow('resized', resized)
            else:
                break

    save_img = click.prompt('Save the image?', type=click.Choice(['y', 'n']))

    if save_img == 'y':
        valid_path = False
        dst_dir = click.prompt('Enter the destination directory', type=str)
        while not valid_path:
            try:
                cv2.imwrite(dst_dir, resized)
                valid_path = True
            except cv2.error:
                click.echo('Invalid directory path. Try again...')
                dst_dir = click.prompt('Enter the destination directory',
                                       type=str)

        click.echo(f'Saved to: {dst_dir}')
        click.echo('Done')
    else:
        click.echo('Done')


@main.command()
@click.option('--dst',
              type=str,
              prompt='Path to destination folder',
              default='manual_crop')
@click.option('--img',
              type=str,
              prompt='Path to image to crop the characters from')
@click.option('--vars',
              type=int,
              prompt='Number of variations for each of your characters')
def crop_manual(dst, img, vars):
    image = cv2.imread(img)

    custom_punc = click.prompt(
        "Define the puncutation characters you'll be using", type=str)

    # with open('txtsplit/punctuation_all.txt', 'w') as f:
    #     f.write(custom_punc)

    uppercase = getchars('uppercase.txt')
    lowercase = getchars('alllowercase.txt')
    punctuation = [c for c in custom_punc]

    chars_to_crop = lowercase + uppercase + punctuation
    manual_crop(dst, image, vars, chars_to_crop)


@main.command()
@click.option('--src',
              type=str,
              prompt='Path to source folder of images you cropped manually',
              required=True,
              default='manual_crop')
@click.option('--dst',
              type=str,
              prompt='Path to destination folder',
              required=True,
              default='autocropped')
def crop_auto(src, dst):

    autocrop(src, dst)
    click.echo(f'Done: autocropped images from {src} to {dst}')


if __name__ == "__main__":
    main()
