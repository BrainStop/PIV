# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2 
from matplotlib import pyplot as plt
import numpy as np
#leitura da imagem
path = "../imagensTeste/"
imagem = np.array([cv2.imread(path + "P1000697s.jpg"), 
        cv2.imread(path + "P1000698s.jpg"),
        cv2.imread(path + "P1000699s.jpg"),
        cv2.imread(path + "P1000703s.jpg"),
        cv2.imread(path + "P1000705s.jpg"),
        cv2.imread(path + "P1000706s.jpg"),
        cv2.imread(path + "P1000709s.jpg"),
        cv2.imread(path + "P1000710s.jpg"),
        cv2.imread(path + "P1000713s.jpg")])

imagem_redplane = imagem[:,:,:,2]

for img in imagem_redplane:
    
#    color = ('b','g','r')
#    for j,col in enumerate(color):
#        histr = cv2.calcHist([imagem[i]],[j],None,[256],[0,256])
#        plt.plot(histr,color = col)
#        plt.xlim([0,256])
#    plt.show()

    #filtro blur
    kernel_blur = np.ones((6, 6), np.float32) / 25
    dst = cv2.filter2D(img, -1, kernel_blur)
    #binarização
    ret, thresh = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #melhoramento da imagem
#    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
#    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    kernel_erosion = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25, 25))
    erosion = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel_erosion)
    kernel_openign = cv2.getStructuringElement(cv2.MORPH_OPEN,(30,30))
    opening = cv2.morphologyEx(erosion, cv2.MORPH_ELLIPSE, kernel_openign)
#    kernel5 = cv2.getStructuringElement(cv2.MORPH_OPEN,(60,60))
#    opening2 = cv2.morphologyEx(erosion, cv2.MORPH_ELLIPSE, kernel5)
#    
#
    #extracao de componentes conexos
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
#    
#    #extracao de propriedades 
#    circularidade = np.arange(0, len(contours))
#    
#    #limites das areas das diferentes moedas
#    areaLimits = np.array([0, 1200., 2800., 3250., 4250., 5400., 6200., 7400.])
#    #valores das moedas
#    coinValues = np.array([0.01, 0.02, 0.1, 0.05, 0.2, 1, 0.5])
#    quantiaTotal = 0
#    
#    for cnt in contours:
#        #hasChild = (hierarchy[0][2] != -1)
#        #hasFather = (hierarchy[0][3] != -1)
#        #array com os contornos de todos os objetos
#        #momento da imagem é a média das intensidades dos pixeis
#        #dicionário com os momentos de todos os contornos dos objetos que irá ajudar a calcular os centroides
#        M = cv2.moments(cnt)
#        #area de cada objeto
#        area = cv2.contourArea(cnt)
##        print area
#    
#        #perimetro de cada objeto
#        perimetro = cv2.arcLength(cnt, True)
#        #circularidade de cada objeto
#        circularidade_aux = (np.abs(perimetro)**2) / area
#        #se circularidade menor que 15 e mais que 13.5, porque a circularidade das moedas vai sempre dar 14 +/-, à priori
#        #faz-se esta verificação para ver se é circular ou não, se não for, não é passado para o array "circularidade"
#        if(circularidade_aux >= 13.5 and circularidade_aux <= 15):
#            #centroides de cada objeto circular
#            cx = int(M['m10']/M['m00'])
#            cy = int(M['m01']/M['m00'])
#            centroides = (cx, cy)
#            #quantiaTotal para ver quanto dinheiro está na imagem
#            #adiciona a circularidade todos os objetos circulares
#            circularidade[a] = circularidade_aux
#            
#            #ciclo que percorrerá todas as áreas para ver em que valor da coinValues a moeda pertence
#            for a in range(len(areaLimits)-1):
#                if area >= areaLimits[a] and area <= areaLimits[a+1]:
#                    #adiciona à quantiaTotal o valor da moeda desta iteração
#                    quantiaTotal += coinValues[a]
#                    #poe texto na imagem, em cada centroide, o valor correspondente do valor da moeda
#                    cv2.putText(img, str(coinValues[a]), (centroides), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)
#                    
#    #print quantiaTotal
#    cv2.imshow('imagem', img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()