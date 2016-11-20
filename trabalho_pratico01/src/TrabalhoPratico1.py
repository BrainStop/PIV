# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2 
import numpy as np
import matplotlib.pyplot as plt
import os

#leitura das imagens
path = "../imagens/"
files = []
for f in os.listdir(path):
    if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
        files.append(cv2.imread(path + f))
imagens = np.array(files)

#histograma das diferentes cores RGB
imagens_stacked = np.vstack(imagens[:])
color = ('b','g','r')
for j,col in enumerate(color):
    histr = cv2.calcHist([imagens_stacked],[j],None,[256],[0,256]) 
    plt.plot(histr, color = col)
    plt.xlim([0,256])
plt.show()

#Extraccao do canal vermelho
imagens_red_channel = imagens[:,:,:,2]

for i in range(len(imagens)):

    #filtro blur
    kernel_blur = np.ones((6, 6), np.float32) / 25
    dst = cv2.filter2D(imagens_red_channel[i], -1, kernel_blur)
    
    #binarização
    _, thresh = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #melhoramento da imagem
    kernel_erosion = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25, 25))
    erosion = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel_erosion)
    kernel_openign = cv2.getStructuringElement(cv2.MORPH_OPEN,(30,30))
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel_openign)

    #extracao de componentes conexos
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imagens[i], contours, -1, (0, 0, 255), 3)

    #extracao de propriedades 
    circularidade = np.arange(0, len(contours))
    
    #limites das areas das diferentes moedas
    areaLimits = np.array([5077, 8095., 10181., 11555., 13453., 14990., 16150., 19000])
    
    #valores das moedas
    coinValues = np.array([0.01, 0.02, 0.1, 0.05, 0.2, 1, 0.5])
    quantiaTotal = 0

    for a in range(len(contours)):
        #array com os contornos de todos os objetos
        cnt = contours[a]
        #momento da imagem é a média das intensidades dos pixeis
        #dicionário com os momentos de todos os contornos dos objetos que irá ajudar a calcular os centroides
        M = cv2.moments(cnt)
        #area de cada objeto
        area = cv2.contourArea(cnt)
        #perimetro de cada objeto
        perimetro = cv2.arcLength(cnt, True)
        #circularidade de cada objeto
        circularidade_aux = (np.abs(perimetro)**2) / area
        #se circularidade menor que 15 e mais que 13.5, porque a circularidade das moedas vai sempre dar 14 +/-, à priori
        #faz-se esta verificação para ver se é circular ou não, se não for, não é passado para o array "circularidade"
        if(circularidade_aux >= 13.5 and circularidade_aux <= 15):
            #centroides de cada objeto circular
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            centroides = (cx, cy)
            
            #quantiaTotal para ver quanto dinheiro está na imagem
            #adiciona a circularidade todos os objetos circulares
            circularidade[a] = circularidade_aux
            
            #ciclo que percorrerá todas as áreas para ver em que valor da coinValues a moeda pertence
            for b in range(len(areaLimits)-1):
                if area >= areaLimits[b] and area <= areaLimits[b+1] :  
                    if area >= 16200 and area <= 17000:
                        break
                    else: 
                        #adiciona à quantiaTotal o valor da moeda desta iteração
                        quantiaTotal += coinValues[b]
                    #poe texto na imagem, em cada centroide, o valor correspondente do valor da moeda
                    cv2.putText(imagens[i], str(coinValues[b]) + "euro", (centroides), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2)
    #coloca a quantia total das moedas apresentadas na imagem
    cv2.putText(imagens[i], "ValorTotal=" + str(quantiaTotal), (30, 30), cv2.FONT_HERSHEY_PLAIN , 2, (255,255,255),2)

    #visualizacao das imagens com a informacao
    cv2.imshow('imagem', imagens[i])
    cv2.waitKey(0)
    cv2.destroyAllWindows()