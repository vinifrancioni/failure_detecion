'''

TRABALHO DE PDI
Alunos: Vinicius Francioni
        Kaue Silva Marcondes

'''

import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from tkinter import *

########################################## C O N F I G U R A Ç Õ E S ###################################################

kernel = np.ones((9,9),np.uint8)                                      # Kernel que define o espaço da morfologia
path = "imagens"
onlyfiles = [ f for f in listdir(path) if isfile(join(path, f)) ]
fotos = len(onlyfiles)                                                  # Número de fotos a serem analisadas ou pode ser substituido por um numero inteiro

lower_blue = np.array([110, 130, 50])                                   # Define o limitante superior para a máscara
upper_blue = np.array([150, 230, 230])                                  # Define o limitante inferior para a máscara

lower_red = np.array([150, 70, 70])
upper_red = np.array([200, 210, 210])

lower_green = np.array([20, 80, 80])
upper_green = np.array([90, 210, 180])

############################################# I M P O R T A R ##########################################################

image_import = np.empty(len(onlyfiles), dtype=object)
imagem_hist = np.empty(len(onlyfiles), dtype=object)
imagem_hsv = np.empty(len(onlyfiles), dtype=object)
res_blue = np.empty(len(onlyfiles), dtype=object)
res_red = np.empty(len(onlyfiles), dtype=object)
res_green = np.empty(len(onlyfiles), dtype=object)
res_mask = np.empty(len(onlyfiles), dtype=object)
hist_blue = np.empty(len(onlyfiles), dtype=object)
hist_red = np.empty(len(onlyfiles), dtype=object)
hist_green = np.empty(len(onlyfiles), dtype=object)
imagem_blur = np.empty(len(onlyfiles), dtype=object)
imagem_ruido = np.empty(len(onlyfiles), dtype=object)
imagem_blur_hsv = np.empty(len(onlyfiles), dtype=object)

############################################### L O O P S ##############################################################

def importar ():

    for n in range(0, len(onlyfiles)):

      image_import[n] = cv2.imread(join(path, onlyfiles[n]))
      image_import[n] = cv2.resize(image_import[n], (480, 360))
      imagem_hsv[n] = cv2.cvtColor(image_import[n], cv2.COLOR_BGR2HSV)                # Muda o esquema de cores de BGR para HSV

    return;


def filtros ():

    n = 0

    while n < fotos:

        mask_blue = cv2.inRange(imagem_hsv[n], lower_blue, upper_blue)
        mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)# Faz uma morphologia para retirar os grãos da máscara
        #hist_blue[n] = cv2.calcHist([mask_blue], [0, 1], None, [180, 256], [5, 180, 5, 256])
        res_blue[n] = cv2.bitwise_and(image_import[n], image_import[n], mask = mask_blue)

        mask_red = cv2.inRange(imagem_hsv[n], lower_red, upper_red)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE,kernel)
        #hist_red[n] = cv2.calcHist([mask_red], [0], None, [256], [1, 256])
        res_red[n] = cv2.bitwise_and(image_import[n], image_import[n], mask = mask_red)

        mask_green = cv2.inRange(imagem_hsv[n], lower_green, upper_green)   # Essa máscara reconhece verde e amarelo ao mesmo tempo
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE,kernel)
        #hist_green[n] = cv2.calcHist([mask_green], [0], None, [256], [1, 256])
        res_green[n] = cv2.bitwise_and(image_import[n], image_import[n], mask = mask_green)

        res_mask[n] = np.hstack((res_red[n], res_blue[n]))
        res_mask[n] = np.hstack((res_mask[n], res_green[n]))            # Faz a junção das imagens, só para exibição

        cv2.imshow('Máscaras', res_mask[n])
        cv2.waitKey()

        n = n + 1

    #plt.plot(hist_blue[1])
    #plt.plot(hist_red[1])
    #plt.plot(hist_green[1])
    plt.show()

    return;

def ruido():                                                            # Faz a aplicação de ruído sal e pimenta

    n = 0

    while n < fotos:

        input = cv2.cvtColor(imagem_hsv[n], cv2.COLOR_HSV2RGB)              # Converção facilita o processo
        output = np.zeros(input.shape, np.uint8)                        # Cria matriz igual a imagem para os dados do ruido
        p = 0.05                                                        # Quantidade de ruído desejado

        for i in range(input.shape[0]):                                 # Loop para adicionar o efeito (ou não) a cada pixel da matriz
            for j in range(input.shape[1]):
                r = random.random()
                if r < p / 2:
                        output[i][j] = 0, 0, 0
                elif r < p:
                        output[i][j] = 255, 255, 255
                else:
                        output[i][j] = input[i][j]

        imagem_ruido[n] = output
        imagem_ruido[n] = cv2.cvtColor(imagem_ruido[n], cv2.COLOR_RGB2BGR)          # Converte e imagem para BGR

        #cv2.imshow("Com ruido", imagem_ruido[n])
        #cv2.waitKey()

        n = n + 1

    return;

def ajustes ():                                                         # Aplicação de redução de Sal e Pimenta

    for n in range(0, len(onlyfiles)):

        imagem_blur[n] = cv2.medianBlur(imagem_ruido[n], 3)
        imagem_hsv[n] = cv2.cvtColor(imagem_blur[n], cv2.COLOR_BGR2HSV)

        #cv2.imshow("Depois", imagem_blur[n])
        #cv2.waitKey()

    return;

def sem_filtro():

    n = 0

    while n < fotos:

        cv2.imshow('Sem filtro', imagem_ruido[n])
        cv2.waitKey()

        n = n + 1

    return;

def matrizes ():                                                        # Zera todas as matrizes, util na troca de botões

    image_import = np.empty(len(onlyfiles), dtype=object)
    imagem_hist = np.empty(len(onlyfiles), dtype=object)
    imagem_hsv = np.empty(len(onlyfiles), dtype=object)
    res_blue = np.empty(len(onlyfiles), dtype=object)
    res_red = np.empty(len(onlyfiles), dtype=object)
    res_green = np.empty(len(onlyfiles), dtype=object)
    res_mask = np.empty(len(onlyfiles), dtype=object)
    hist_blue = np.empty(len(onlyfiles), dtype=object)
    hist_red = np.empty(len(onlyfiles), dtype=object)
    hist_green = np.empty(len(onlyfiles), dtype=object)
    imagem_blur = np.empty(len(onlyfiles), dtype=object)
    imagem_ruido = np.empty(len(onlyfiles), dtype=object)
    imagem_blue_hsv = np.empty(len(onlyfiles), dtype=object)

    return;

############################################# U S E R   I N T E R F A C E ##############################################


class Janela:

    def __init__(self, toplevel):

        # Cria o layout da UI
        self.frame = Frame(toplevel)
        self.frame.pack()
        self.frame2 = Frame(toplevel)
        self.frame2.pack()
        self.titulo = Label(self.frame, text='\n\n\n\nSTARTUP \n HACKERMAN 2000',font=('Verdana', '13', 'bold'))
        self.titulo.pack()

        self.msg = Label(self.frame, width=100, height=20, text='Selecione a opção desejada')
        self.msg.focus_force()
        self.msg.pack()

        # Define o botão 1
        self.b01 = Button(self.frame2, text='Teste Normal')
        self.b01['padx'], self.b01['pady'] = 10, 5
        self.b01['bg'] = 'blue'
        self.b01.bind("<Return>", self.keypress01)
        self.b01.bind("<Any-Button>", self.button01)
        self.b01.bind("<FocusIn>", self.fin01)
        self.b01.bind("<FocusOut>", self.fout01)
        self.b01['relief'] = RIDGE
        self.b01.pack(side=LEFT)

        # Define o botão 2
        self.b02 = Button(self.frame2, text='Sal e Pimenta')
        self.b02['padx'], self.b02['pady'] = 10, 5
        self.b02['bg'] = 'green'
        self.b02.bind("<Return>", self.keypress02)
        self.b02.bind("<Any-Button>", self.button02)
        self.b02.bind("<FocusIn>", self.fin02)
        self.b02.bind("<FocusOut>", self.fout02)
        self.b02['relief'] = RIDGE
        self.b02.pack(side=LEFT)

        # Define o botão 3
        self.b03 = Button(self.frame2, text='Sal e Pimenta Sem filtro')
        self.b03['padx'], self.b03['pady'] = 10, 5
        self.b03['bg'] = 'gray'
        self.b03.bind("<Return>", self.keypress03)
        self.b03.bind("<Any-Button>", self.button03)
        self.b03.bind("<FocusIn>", self.fin03)
        self.b03.bind("<FocusOut>", self.fout03)
        self.b03['relief'] = RIDGE
        self.b03.pack(side=LEFT)

        # Define o botão 4
        self.b04 = Button(self.frame2, text=' SAIR ')
        self.b04['padx'], self.b04['pady'] = 10, 5
        self.b04['bg'] = 'red'
        self.b04.bind("<Return>", self.keypress04)
        self.b04.bind("<Any-Button>", self.button04)
        self.b04.bind("<FocusIn>", self.fin04)
        self.b04.bind("<FocusOut>", self.fout04)
        self.b04['relief'] = RIDGE
        self.b04.pack(side=LEFT)

    # Define os estados dos botões
    def keypress01(self,event): self.msg
    def keypress02(self,event): self.msg
    def keypress03(self, event): self.msg
    def keypress04(self, event): self.msg

    # Faz as chamadas de função conforme o botão pressionado
    def button01(self,event):
        matrizes()
        importar()
        filtros()

    def button02(self,event):
        matrizes()
        importar()
        ruido()
        ajustes()
        filtros()

    def button03(self, event):
        matrizes()
        importar()
        ruido()
        sem_filtro()

    def button04(self, event):
        exit()

    def fin01(self,event): self.b01['relief']=FLAT
    def fout01(self,event): self.b01['relief']=RIDGE
    def fin02(self,event): self.b02['relief']=FLAT
    def fout02(self,event): self.b02['relief']=RIDGE
    def fin03(self,event): self.b02['relief']=FLAT
    def fout03(self,event): self.b02['relief']=RIDGE
    def fin04(self,event): self.b02['relief']=FLAT
    def fout04(self,event): self.b02['relief']=RIDGE


raiz =Tk()
Janela(raiz)
raiz.mainloop()