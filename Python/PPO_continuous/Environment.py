import serial
import numpy as np
import time

class Env:
    def __init__(self):
        PORT = 'COM7'
        BaudRate = 115200
        self.ARD = serial.Serial(PORT, BaudRate)
        self.clip_distance = 200.  # unit: cm
        self.dead_distance = 6.
        self.safety_distance = 20.

        self.min_action = 135.
        self.max_action = 255.

    def Decode(self, A):
        A = str(A.decode())
        if A[0] == 'S' and A[10] == 'E':  # 첫문자, 마지막 문자 검사
            dstF = int(A[1:4])
            dstL = int(A[4:7])
            dstR = int(A[7:10])
            result = [dstF, dstL, dstR]
            for i in [0,1,2]:
                if result[i] < 2.0:
                    result[i] = self.dead_distance + 1
            return result
        else:
            print("Error_Wrong Signal")

    def Ardread(self):
        if self.ARD.readable():
            LINE = self.ARD.readline()
            data = self.Decode(LINE)
            # data range: (0. ~ 999.)  >> clip(0. ~ 200.)
            data = np.clip(data, 0., self.clip_distance)
            return data
        else:
            print("읽기 실패 from _Ardread_")

    def step(self, action, repeat = 3):
        done = False
        total_reward = 0

        action_left, action_right = self.map_action(action)
        Trans = "S" + action_left + action_right  # S+000+000
        Trans = Trans.encode('utf-8')
        self.ARD.write(Trans)
        data = self.Ardread()
        if data[0] < (self.dead_distance * 3):
            done = True
            reward = -10
            return data, reward, done
        if data[1] < self.dead_distance or data[2] < self.dead_distance:
            done = True
            reward = -5
            return data, reward, done

        elif (self.dead_distance) <= min(data) < (self.safety_distance):
            reward = .1

        elif min(data) >= (self.safety_distance):
            reward = .2

        total_reward += reward
        return data, reward, done

    def restart(self):
        Trans = "RRRRR"
        Trans = Trans.encode('utf-8')
        self.ARD.write(Trans)
        time.sleep(2)

    def end(self):
        Trans = "EEEEE"
        Trans = Trans.encode('utf-8')
        self.ARD.write(Trans)

    def map_action(self, action):
        
        action = np.reshape(action, (2,))
        action = np.clip(action, -10., 10.)
        action = (action + 10.) / 20.
        action = action * (self.max_action - self.min_action) + self.min_action

        action_left = "{:+03.0f}".format(action[0])
        action_right = "{:+03.0f}".format(action[1])

        return action_left, action_right
