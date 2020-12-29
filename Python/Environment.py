import serial
import numpy as np

class Env:
    def __init__(self):
        PORT = 'COM7'
        BaudRate = 115200
        self.ARD = serial.Serial(PORT,BaudRate)

    def Decode(self, A):
        A = str(A.decode())
        if A[0]=='S':                       #첫문자 검사
            if (len(A)==13):                #문자열 갯수 검사
                dstF=int(A[1:4])
                dstL=int(A[4:7])
                dstR=int(A[7:10])
                result= [dstF, dstL, dstR]
                return result
            else: 
                print ("Error_lack of number _ %d" %len(A))
        else :
            print ("Error_Wrong Signal")
            
        
    def Ardread(self):
            while self.ARD.readable():
                LINE = self.ARD.readline()
                data = self.Decode(LINE)
                return data
            else: 
                print("읽기 실패 from _Ardread_")


    def step(self, action):
        reward = 0
        done = False
        action_left, action_right = self.map_action(action)
        Trans="S" + action_left + action_right # S+000+000
        Trans= Trans.encode('utf-8')
        self.ARD.write(Trans)
        
        data = self.Ardread()

        if data[0] < 10:
            done = True
            reward = -10
            return data, reward, done
        
        elif 10 <= min(data) < 20:
            reward += -1

        elif min(data) >= 20:
            reward += 1
        return data, reward, done

    def restart(self):
        Trans="RRRRR"
        Trans= Trans.encode('utf-8')
        self.ARD.write(Trans)

    def end(self):
        Trans="EEEEE"
        Trans= Trans.encode('utf-8')
        self.ARD.write(Trans)

    def map_action(self, action, minimum = 100):
        # action (0.0 ~ +1.0)  --> (130 ~ 250)
        # action (-1.0 ~ 0.0)  --> (-130 ~ -250)
        action = np.reshape(action, (2,))
        maximum = 250 - minimum
        action = np.clip(action*maximum, -maximum, +maximum)
        for i in range(2):
            if action[i] < 0:
                action[i] -= minimum
            elif action[i] > 0:
                action[i] += minimum
        action_left = "{:+03.0f}".format(action[0])
        action_right = "{:+03.0f}".format(action[1])
        return action_left, action_right