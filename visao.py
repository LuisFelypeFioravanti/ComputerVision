import cv2
import numpy as np
import math
import time
cap = cv2.VideoCapture(0)
print("Inicializando Video...")
#Variavel da Maquina de estados
maquina=0
mao=""
while(1):
    try:  #Programa encerra se nao acha nada, por isso esse try.
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)
        kernel = np.ones((3,3),np.uint8)    
    #Área de Interesse
        adi=frame[100:300, 100:300]
        cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)    
        hsv = cv2.cvtColor(adi, cv2.COLOR_BGR2HSV)
    #Gama de cores no HSV
        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)
    #Extrair cor de pele
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
    #Dilatar a imagem da mão pra cobrir pontos escuros
        mask = cv2.dilate(mask,kernel,iterations = 2)
    #Blur Gaussiano
        mask = cv2.GaussianBlur(mask,(5,5),100) 
    #Acha controno
        contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #Acha contorno da maior área
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
    #Aproxima um pouco o contorno
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
    #Casco convexo em torno da mão
        hull = cv2.convexHull(cnt)
     #Área da mão e área do casco
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
    #Porcentagem da área da mão que não cobre a area do casco
        porcentagemArea=((areahull-areacnt)/areacnt)*100
     #Acha os defeitos de convexidades
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
    # l = numero de defeitos
        l=0
    #lista de distancias
        distancias=[]
    #numero de convexidades nos dedos(muita matemática);
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            comeco = tuple(approx[s][0])
            fim = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt= (100,180)
            a = math.sqrt((fim[0] - comeco[0])**2 + (fim[1] - comeco[1])**2)
            b = math.sqrt((far[0] - comeco[0])**2 + (far[1] - comeco[1])**2)
            c = math.sqrt((fim[0] - far[0])**2 + (fim[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            d=(2*ar)/a
        #Lei do cosseno
            angulo = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        #Ignora angulos maiores que 90 e pontos muito proximos do casco(geralmente são por barulho de imagem)
            if angulo <= 120 and d>25:
                l += 1
                cv2.circle(adi, far, 3, [255,0,0], -1)
                distancias.append(far)
        #Desenha em torno da mão
            cv2.line(adi,comeco, fim, [0,255,0], 2)
        l+=1
        #variavel que guarda a convexidade mais baixa da matriz
        maisBaixa=0
        indice=0
        iB=0
        iL=0
        
        for tupla in distancias:
            if(tupla[1]>maisBaixa):
                maisBaixa=tupla[1]
                iB=indice
            indice+=1
        maisLonge=0
        indice=0
        
        for tupla in distancias:
            if(tupla[0]>maisLonge):
                maisLonge=tupla[0]
                iL=indice
            indice+=1
        

        
    # #Printa os gestos
        font = cv2.FONT_HERSHEY_SIMPLEX
        if l==1:
            if areacnt<2000:
                cv2.putText(frame,'Sem mao',(0,50), font, 1, (0,0,255), 3, cv2.LINE_AA)
            else:
                if porcentagemArea<10:
                    cv2.putText(frame,'Nenhum dedo',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    if (maquina==5):
                        if(mao=="Direita"):
                            print("Gesto 0--Mao Direita")
                        else:
                            print("Gesto 0--Mao Esquerda")
                #elif porcentagemArea<17.5:
                #   cv2.putText(frame,'Tinino',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                else:
                    cv2.putText(frame,'1 Dedo',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    if (maquina==5):
                        if(mao=="Direita"):
                            print("Gesto 1--Mao Direita")
                        else:
                            print("Gesto 1--Mao Esquerda")
        elif l==2:
            cv2.putText(frame,'2 Dedos',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            if (maquina==5):
                if(mao=="Direita"):
                    print("Gesto 2-Mao Direita")
                else:
                    print("Gesto 2--Mao Esquerda")
        elif l==3:
              #if porcentagemArea<27:
                    cv2.putText(frame,'3 Dedos',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    if (maquina==5):
                        if(mao=="Direita"):
                            print("Gesto 3--Mao Direita")
                        else:
                            print("Gesto 3--Mao Esquerda")
              #else:
            #     cv2.putText(frame,'OK',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)        
        elif l==4:
            cv2.putText(frame,'4 Dedos',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            if (maquina==5):
                if(mao=="Direita"):
                    print("Gesto 4--Mao Direita")
                else:
                    print("Gesto 4--Mao Esquerda")
        elif l==5:
            cv2.putText(frame,'Base',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
        else :
            cv2.putText(frame,'Reposicione',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
        
        maquina=l
        if(len(distancias) != 0):
            if(distancias[iB]==distancias[iL]):
                mao="Esquerda"
            else:
                mao="Direita"

    # #Mostra os vídeos
        cv2.imshow('mask',mask)
        cv2.imshow('frame',frame)
        time.sleep(0.8)
    except: # Excessão do erro
        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        print("passou")
        time.sleep(0.2)
        pass
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()
cap.release()    