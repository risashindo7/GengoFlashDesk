import argparse
import glob
import os
from image_logic.labelExtractor import extract_labels


def parse_args():
    parser = argparse.ArgumentParser(description="Image retrieval.")
    parser.add_argument('--images', nargs='?', default='data/images',
                        help='Path of the document file.')
    return parser.parse_args()


def load_image_list(path):
    """
    Returns
    -------
    images : list
        each entry is a tuple (image name, image path)
    """
    images = []
    for f in glob.glob(os.path.join(path, '*.jpg')):
        fname = os.path.basename(f)
        images.append((os.path.splitext(fname)[0], f))
    return images

if __name__ == '__main__':
    args = parse_args()
    # load images in datbase
    images = load_image_list(args.images)
    extract_labels(images)
