import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# horse_path = 'DATA/horse.jpg'
# rainbow_path = 'DATA/rainbow.jpg'
# bricks_path = 'DATA/bricks.jpg'


def load_img(path, resize=0.0, recolor=False, greyscale=False):

    "recolor must be like cv2.COLOR_BGR2RGB"

    messages=[]

    if not os.path.exists(path):
        raise IOError("File {} does not exist!".format(path))

    if greyscale:
        img1 = cv2.imread(path, 0)
        messages.append("- Applicata la scala di grigi")
    else:
        img1 = cv2.imread(path)

    if resize > 0:
        factor = resize
        img1 = cv2.resize(img1, (0,0), fx=factor, fy=factor) 
        messages.append("- Applicato un resize di {}".format(factor))

    if recolor:
        # cv2.COLOR_BGR2RGB
        img1 = cv2.cvtColor(img1, recolor)
        messages.append("- Applicata la conversione di colori {}".format(str(recolor[4:])))

        
    print("Generata nuova immgine di partenza: {}".format(path))

    for m in messages:
        print(m)

    return img1

# covert a matplotlib image into a opencv one



def convert_matplotlib_to_opencv_img(matplotlib_format_img=None, clear=False, transitory_img_path='tmp345678.jpg'):

    """
    matplotlib_format_img: must be a matplotlib class object, like histograms from function cv2.calcHist
    clear: if set to true, it will clear any existing matplotlib.pyplot object.
    """

    messages=[]

    # plt è un.metodo fa si che plt abbia un elemento che vien append plottato con qulloc he gli do in input.
    # per ripulire la figura uso plt.clf()
    if clear:
        plt.clf()
        messages.append("- L'elemento matplotlib.pyplot è stato cancellato.")

    if any(matplotlib_format_img):
        plt.plot(matplotlib_format_img)
        # altrimenti plotta il plot gà esistente
        messages.append("- L'immagine in input è stata aggiunta al matplotlib.pyplot.")

    try:
        plt.savefig(transitory_img_path)

        cv2_imread_format_img = cv2.imread(transitory_img_path)

        import os
        try: 
            os.remove(transitory_img_path)
        except: 
            raise OSError("could not remove file {}".format(transitory_img_path))

    except: 
        raise OSError("could not save img to {}".format(transitory_img_path))
    

    return cv2_imread_format_img



def cyclical_drawing(images, labels=None):

    """
    images: list of images
    labels: list of the names of the images
    """

    print("--- cyclical drawing --- S")

    # print("images: {}".format(images))

    # labeling
    if not labels:

        labels = []
        for idx, image in enumerate(images):
            labels.append( "my_drawing_" + str(idx+1))
            # only here I make the human friendly index

        # labels = [ "my_drawing_" + str(index()) for image in images ]

    for idx, image in enumerate(images):
        cv2.namedWindow(winname=labels[idx])
        # print( 'my_drawing_'+str(idx) )

    while True:
        for idx, image in enumerate(images):
            cv2.imshow(labels[idx], image)

        if cv2.waitKey(1) & 0xFF == 27: # se premo esc
            break

    cv2.destroyAllWindows()