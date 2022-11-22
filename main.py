##################################################
# Exemplo de programação Arduino reconhecimento de
# cores para atuar como selecionador de objetos em
# um esteira.
# Prof. Wanderlei Silva do Carmo
# Versão: 0.9
##################################################
import time

import cv2
import numpy as np
import pyfirmata
from pyfirmata import Arduino
import inspect

if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

## port = "COM3"

#board = Arduino(port)
#it = pyfirmata.util.Iterator(board)
#it.start()

ledVerde = 2
ledAmarelo = 4
ledVermelho = 6

#servo_verde = board.get_pin('d:9:s')
#sensor = board.get_pin('a:1:i')

# left = board.get_pin('d:11:s')
# right = board.get_pin('d:10:s')

cap = cv2.VideoCapture(0)

corAlterada = ''
corFinal = ''

HOR = [0x01,0x02,0x03,0x04]
AHO = [0x04,0x03,0x01,0x01]

atraso_fase = 2
intervalo = 1

DDRB = 0x0f
PORTB = 0x00

def motor_AHO():
    for i in range(512):
        for j in range(4):
            PORTB = AHO[j]
            time.sleep(atraso_fase)

def motor_HOR():
    for i in range(512):
        for j in range(4):
            PORTB = HOR[j]
            time.sleep(atraso_fase)


while True:
    _, img = cap.read()
    #img2 = imutils.resize(img, width=50, height=50)

    h, w, _ = img.shape
    offset = 220
    campo = img[offset:h-offset, offset:w-offset]

    corMediaLinha = np.average(campo, axis=0)
    corMedia = np.average(corMediaLinha, axis=0)

    r,g,b = int(corMedia[2]), int(corMedia[1]), int(corMedia[0])

    cor = [r,g,b]

    print(cor)

    if r >= 100 and g <=60 and b <= 100:
#        board.digital[ledAmarelo].write(1)
        corFinal = 'Vermelho'
    elif r <= 100 and g >= 100 and b<= 120:
        corFinal = 'Verde'

    elif np.argmax(cor) == 0:
 #       board.digital[ledVermelho].write(1)
        corFinal = 'Amarelo'
    elif  np.argmax(cor) == 1:
  #      servo_verde.write(0)
        corFinal = 'Verde'

    else:
   #     board.digital[ledVermelho].write(0)
   #     board.digital[ledVerde].write(0)
   #     board.digital[ledAmarelo].write(0)
        corFinal = 'Preto'

    if corFinal != corAlterada:
        pass
        #board.digital[ledVermelho].write(0)
        #board.digital[ledVerde].write(0)
        #board.digital[ledAmarelo].write(0)


    corAlterada = corFinal

    cv2.rectangle(img,(offset,offset), (w-offset, h - offset), [b*1.5,g*1.5,r*1.5], 100 )
    cv2.rectangle(img, (offset, offset), (w - offset, h - offset), [b*1.5,g*1.5,r*1.5], 3 )

    cv2.putText(img, corFinal, (110, 440), cv2.FONT_HERSHEY_SIMPLEX, .9, color=(b*2,g*2,r*2), thickness=2)

    print("Vermelho: {0}, Verde: {1}, Azul: {2}".format(r, g, b) )


    if corFinal == 'Verde':
        pass#servo_verde.write(0)
    else:
        pass#servo_verde.write(180)

    #saida = sensor.read()

    #print(saida)

    # motor_AHO()
    # time.sleep(intervalo)

    # motor_HOR()
    # time.sleep(intervalo)
    # cv2.imshow('campo', campo)


    cv2.imshow('Img', img)

    cv2.waitKey(1)

