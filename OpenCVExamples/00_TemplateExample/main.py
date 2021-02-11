import cv2

def main():
    filepath = 'path/to/gray/level/imagefile.png'
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)
    print("Image size: {}".format(img.shape))
    return

if __name__ == '__main__':
    main()