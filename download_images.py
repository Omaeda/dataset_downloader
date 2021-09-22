# import the necessary packages
import argparse
import imghdr
import os
import pathlib
import socket
import sys
from urllib.request import urlretrieve

socket.setdefaulttimeout(60)  # 60 seconds


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--urls", required=True,
                    help="path to file containing image URLs")
    ap.add_argument("-o", "--output", required=True,
                    help="path to output directory of images")
    args = vars(ap.parse_args())
    # grab the list of URLs from the input file, then initialize the
    # total number of images downloaded thus far
    rows = open(args["urls"]).read().strip().split("\n")
    total = 0

    # loop the URLs
    for url in rows:
        try:
            # get new file path
            p = os.path.sep.join([args["output"], "{}.jpg".format(
                str(total).zfill(8))])
            # try to download the image
            urlretrieve(url, p)
            # update the counter
            print("[INFO] downloaded: {}".format(p))
            total += 1
        # handle if any exceptions are thrown during the download process
        except:
            print("[INFO] error downloading {}...skipping".format(p))

    # loop over the image paths we just downloaded
    for imagePath in pathlib.Path(args["output"]).glob('*'):
        # initialize if the image should be deleted or not
        delete = False
        # try to load the image
        try:
            image = imghdr.what(imagePath)
            # if the image is `None` then we could not properly load it
            # from disk, so delete it
            if image is None:
                delete = True
        # if OpenCV cannot load the image then the image is likely
        # corrupt so we should delete it
        except:
            print("Except")
            delete = True
        # check to see if the image should be delete
        if delete:
            print("[INFO] deleting {}".format(imagePath))
            os.remove(imagePath)

    # USO : python download_images.py --urls urls.txt --output images/santa

    # PD: el directorio de salida debe estar creado


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
