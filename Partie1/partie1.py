import cv2 as cv
import numpy as np



def EncodeText(Text: str) -> str:

    txt_binaire = ""
    for let in Text:
        ascii_rep = ord(let) #recupere la representation ascii 
        bin_rep = bin(ascii_rep) #transformer en binaire
        bin_rep = bin_rep [2:] #enlever '0b' au debur

        while len(bin_rep) < 8 : #pour avoir a la fin chaque lettre sur 1 octet
            bin_rep = "0" + bin_rep   

        txt_binaire += bin_rep

    #calculer la taille qui va etre representée sur 2 octets (16 bits)
    taille_bin = bin(len(txt_binaire))
    taille_bin = taille_bin[2:]
    while len(taille_bin) < 16 :
        taille_bin = "0" + taille_bin
    return txt_binaire + taille_bin 

def InsertText(Text : str, imgBShape):
    
    font = cv.FONT_HERSHEY_SIMPLEX
    org = (50, 150)
    fontScale = 2
    color = (0, 0, 0)
    thickness = 3
    txt_binaire = ""
    taille_bin = ""

    image = np.ones(imgBShape, dtype=np.uint8)
    
    # Using cv2.putText() method
    image = cv.putText(image, 'OpenCV', org, font, 
                    fontScale, color, thickness, cv.LINE_AA)

    imgB = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            bin_rep = bin(imgB[x,y]) #transformer en binaire
            bin_rep = bin_rep [2:] #enlever '0b' au debur

        while len(bin_rep) < 8 : #pour avoir a la fin chaque lettre sur 1 octet
            bin_rep = "0" + bin_rep   

        txt_binaire += bin_rep
    
    #calculer la taille qui va etre representée sur 2 octets (16 bits)
    taille_bin = bin(len(txt_binaire))
    taille_bin = taille_bin[2:]
    while len(taille_bin) < 16 :
        taille_bin = "0" + taille_bin
    return txt_binaire + taille_bin 





def Encode(text, ImagePath):

    image = cv.imread(ImagePath, cv.IMREAD_COLOR)

    img_ycbcr = cv.cvtColor(image, cv.COLOR_BGR2YCR_CB)

    codage = InsertText(text, ImagePath)

    d1,d2,d3 = img_ycbcr.shape 
    index = 0 
    for y in range(d1) : 
        for x in range(d2):
            for z in range(d3-1):

                px = img_ycbcr[x,y,z+1]
                bin_ = list(bin(px))[2:]

                bin_[4] = codage[index]
                
                index += 1
                bin_[5] = codage[index]

                index += 1
                img_ycbcr[x,y,z+1] = int("".join(bin_),2)

                if len(codage) <= index :
                    break
            if len(codage) <= index :
                    break
        if len(codage) <= index :
                    break

    return cv.cvtColor(img_ycbcr, cv.COLOR_YCR_CB2BGR)


def DecodeText(Txt_Binaire : str ) -> str :
    return None


print(EncodeText("Hello"))


image = cv.imread("img.jpg",cv.IMREAD_COLOR)

img2 = cv.cvtColor(image, cv.COLOR_BGR2YCR_CB)

print(img2.shape)

print(img2[:,:,0].min())

"""
cv.imshow("GRAY2",img2)
cv.waitKey(0)
cv.destroyAllWindows()
"""

#Encode("Hello","img.jpg")
