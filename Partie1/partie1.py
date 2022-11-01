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



def Encode(text, ImagePath):

    image = cv.read(ImagePath)

    d1,d2,d3 = image.shape 

    for y in range(d2) : 
        for x in range(d1):
            for z in range(d3):

                print("hey")


    return 0


def DecodeText(Txt_Binaire : str ) -> str :
    return None


print(EncodeText("Hello"))