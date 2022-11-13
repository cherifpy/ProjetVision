import cv2 as cv
import numpy as np
from PIL import Image
from scipy import ndimage

def InsertText(Text : str, imgBShape):

    font = cv.FONT_HERSHEY_SIMPLEX
    org = (0, 50)
    fontScale = 2
    color = (0, 0, 0)
    thickness = 3
    txt_binaire = ""
    taille_bin = ""

    image = np.ones(imgBShape, dtype = np.uint8)
    image[:] = [255,255,255]
    image = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

    image = cv.putText(image, Text, org, font, fontScale, color, thickness, cv.LINE_AA)

    d1,d2 = image.shape

    for x in range(d1):
        for y in range(d2):

            bin_rep = bin(image[x,y]) 
            bin_rep = bin_rep [2:] 

            while len(bin_rep) < 8 : 
                bin_rep = "0" + bin_rep   
            
            txt_binaire = bin_rep + txt_binaire
    
    shape_x,shape_y = bin(image.shape[0])[2:],bin(image.shape[1])[2:]

    taille_bin = bin(len(txt_binaire))[2:]

    while len(shape_x) < 12:
        shape_x = "0" + shape_x

    while len(shape_y) < 12:
        shape_y = "0" + shape_y

    return txt_binaire + shape_x + shape_y 


def Encode(text, ImagePath): 

    image = cv.imread(ImagePath, cv.IMREAD_COLOR)

    img_ycrcb = cv.cvtColor(image, cv.COLOR_BGR2YCR_CB)

    codage = InsertText(text, (150,300,3))

    d1,d2,d3 = img_ycrcb.shape 

    index = 1


    lc = len(codage)
    for y in range(d1) : 
        for x in range(d2):
            for z in range(d3-1):

                bin_ = list(bin(img_ycrcb[y,x,z+1])[2:])
                
                l = len(bin_)

                bin_[l-1], bin_[l-2], bin_[l-3], bin_[l-4] = "1","1","1","0"

                bin_[l-5] = codage[lc-index]

                index += 1

                img_ycrcb[y,x,z+1] = int("".join(bin_),2)

                if len(codage) == index :
                    break
            if len(codage) == index :
                break
        if len(codage) == index :
            break
    FinalImage = cv.cvtColor(img_ycrcb, cv.COLOR_YCR_CB2BGR)
    cv.imwrite("imageAapresEncode.png",FinalImage)
    return FinalImage

def DecodeText(ImagePath):

    cpt,taille = 0, 0
    t_bin, codage,shape_x,shape_y = "", "","", ""

    imageA = cv.imread(ImagePath, cv.IMREAD_COLOR)
    img_ycbcr = cv.cvtColor(imageA, cv.COLOR_BGR2YCR_CB)

    calc_taille, fin =True, False

    d1,d2,d3 = img_ycbcr.shape

    for y in range(d1):
        for x in range(d2):
            for z in range(d3-1):

                if calc_taille == True:
                    if cpt != 24:
                        rep_bin = list(bin(img_ycbcr[y,x,z+1])[2:]) 
                        l = len(rep_bin)
                        t_bin=   f"{rep_bin[l-5]}" + t_bin
                        cpt+=1
                    else:
                        #taille = int(t_bin,2)
                        shape_x = int(t_bin[:12],2)
                        shape_y = int(t_bin[12:],2)
                        taille = shape_x * shape_y * 8
                        calc_taille = False
                        cpt = 0
                else:
                    if cpt != taille:
                        rep_bin = list(bin(img_ycbcr[y,x,z+1])[2:]) 
                        l = len(rep_bin)
                        codage = f"{rep_bin[l-5]}" +codage
                        cpt+=1
                    else:
                        break
            if fin:
                break
        if fin:
            break

    return codage, shape_x,shape_y


def ConstructionImage(codage,shape_x,shape_y):
    
    data = np.ones((shape_x,shape_y), dtype=np.uint8)
    data[:,:] = 255
    cpt1,cpt2,px_dic,i = 0,0,0,0
    px_bin= ""
    stop = False

    while i < (len(codage)) and not stop:

        px_bin = codage[len(codage) - (i+1)] + px_bin

        if (i+1) % 8 == 0:
            px_dic = int(px_bin,2)
            px_bin = ""
            
            data[cpt1,cpt2] = px_dic

            cpt2+=1

            if cpt2 == (shape_y - 1):
                cpt1 += 1
                cpt2 = 0
                if cpt1 == (shape_x-1 ):
                    stop = True
        i+=1
    
    image = Image.fromarray(data, 'L')    
    image.save("ImgBavantdilatation.png")
    img = cv.imread("ImgBavantdilatation.png",cv.IMREAD_COLOR)
    img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    img = img < 200

    #application de la dilatation
    open_x = ndimage.binary_opening(img)
    
    finalImage = np.zeros(open_x.shape, np.uint8)

    for x in range(open_x.shape[0]):
        for y in range(open_x.shape[1]):
            if open_x[x,y] == False:
                finalImage[x,y] = 255
            else:
                finalImage[x,y] = 0
    
    Fimage = Image.fromarray(finalImage,'L')

    Fimage.save("FinalImage.png")

    return cv.imread("FinalImage.png")

