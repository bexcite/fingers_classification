"""
Augmenting a directory with images
Params:
  input_dir - Input directory with images
  outpur_dir - Directory where augmented images will be placed
  resize - resize images to a provided size if present
"""

import cv2
import numpy as np
import argparse
import glob
from pprint import pprint
import os
import shutil
from scipy import misc

def prepare_file_path(input_dir, file_path, suffix = None, output_dir = None):
  """
  Prepares the path for the output file given params and suffix.
  """
  ap = file_path[len(input_dir) + 1:]
  if suffix:
    # Add suffix
    fname, fext = os.path.splitext(ap)
    ap = fname + suffix + fext
  if output_dir:
    ap = os.path.join(output_dir, ap)
    # Check and make directory
    fpath, fname = os.path.split(ap)
    if not os.path.exists(fpath):
      print('directory created: ' + fpath)
      os.makedirs(fpath)
  return ap

def augment_images(
    input_dir,
    output_dir,
    resize = None):
  """
  Augment all images in the input folder by flipping it and resizing (if not None)
  """

  # Get files
  files = glob.glob(input_dir + '/**/*.png')
  # pprint("files = {}".format(files))

  cnt = 0

  for f in files:
    img = misc.imread(f)

    if resize:
      img = misc.imresize(img, (resize, resize))

    # Save original
    output_file = prepare_file_path(input_dir, f, output_dir = output_dir)
    misc.imsave(output_file, img)

    img_flip = np.fliplr(img)

    # Save flipped
    output_file = prepare_file_path(input_dir, f, '_flip', output_dir = output_dir)
    misc.imsave(output_file, img_flip)

    print("[{}] = {}".format(cnt, output_file))

    cnt += 1

    # if cnt > 10:
    #   break

if __name__ == '__main__':
  # Parse arguments
  parser = argparse.ArgumentParser(description='Augmenting images in a given directory')
  parser.add_argument('--input_dir', type=str, help="Original data")
  parser.add_argument('--output_dir', type=str, help="Output augmented dataplace")
  parser.add_argument('--resize', type=int, help="Resize image to a given size.")
  parser.add_argument('--clean_output', default=False, action='store_true', help="Clean output_dir if exists")

  args = parser.parse_args()

  input_dir = args.input_dir
  assert input_dir, "input_dir can't be empty"

  output_dir = args.output_dir
  assert output_dir, "output_dir can't be empty"

  resize = args.resize

  print("input_dir = {}".format(input_dir))
  print("output_dir = {}".format(output_dir))

  if os.path.exists(output_dir):
    print('Clean output dir: ' + output_dir)
    shutil.rmtree(output_dir)

  augment_images(input_dir, output_dir, resize)
