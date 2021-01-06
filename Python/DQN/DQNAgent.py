import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import gym
from collections import deque
import random

class DQN_Network(nn.Module):
    def __init__(self,obs_n,action_n,lr):
        super(DQN_Network, self).__init__()
        self.obs_n = obs_n
        self.action_n = action_n
        self.fc1 = nn.Linear(self.obs_n, 48)
        self.fc2 = nn.Linear(48, 48)
        self.fc3 = nn.Linear(48, self.action_n)
        self.optimizer = torch.optim.Adam(self.parameters(),lr=lr)
        self.loss_fn = nn.MSELoss()
        self.cuda()
        
    
    def forward(self,obs): 
        x = self.fc1(obs)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        return x

class Agent:
    def __init__(self,obs_n,action_n, load = False):
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        self.gamma = 0.99
        self.batch_size = 32
        self.lr = 1e-3
        self.mem_max = 5000
        self.start_learn = 100
        self.action_n = action_n
        self.action_space = [i for i in range(action_n)]
        self.obs_n = obs_n
        self.action_n = action_n
        self.DQN = DQN_Network(self.obs_n,self.action_n, lr = self.lr)
        if load:
            self.load()
        self.DQN_ = DQN_Network(self.obs_n,self.action_n, lr = self.lr)
        self.DQN_.eval()
        self.sync()
        self.memory = deque(maxlen=self.mem_max)
        
    
    def store(self,s,a,r,s_,d):
        self.memory.append((s,a,r,s_,d))
    
    def get_action(self,obs):
        if np.random.rand() > self.epsilon:
            obs = torch.Tensor(obs).view(-1,self.obs_n).cuda()
            action = self.DQN(obs)[0].argmax().item()        
        else:
            action = np.random.choice(self.action_space)
        return action
    
    def learn(self):
        if len(self.memory) < self.start_learn:
            return
        samples = random.sample(self.memory, k=self.batch_size)
        
        S = torch.from_numpy(np.vstack(sample[0] for sample in samples)).cuda().float()
        A = [sample[1] for sample in samples]
        R = torch.from_numpy(np.vstack(sample[2] for sample in samples)).cuda().float()
        S_ = torch.from_numpy(np.vstack(sample[3] for sample in samples)).cuda().float()
        D = torch.from_numpy(np.vstack(sample[4] for sample in samples)).cuda().bool()
              
        
        Q = self.DQN(S)[range(self.batch_size), A]
        Q_ = self.DQN_(S_).detach()
        
        update = R + torch.max(Q_, dim = 1)[0] * self.gamma  * ~D
        
        self.DQN.optimizer.zero_grad()
        loss = self.DQN.loss_fn(Q,update)
        loss.backward()
        self.DQN.optimizer.step()
        
        self.epsilon *= self.epsilon_decay
        if self.epsilon < self.epsilon_min:
            self.epsilon = self.epsilon_min
    
    def sync(self):
        self.DQN_.load_state_dict(self.DQN.state_dict())

    def save(self):
        torch.save(self.DQN.state_dict(), './model/RL_car.pth')

    def load(self):
        self.DQN.load_state_dict(self.DQN.state_dict(), './model/RL_car.pth')

if __name__ == '__main__':
    env = gym.make('CartPole-v1')
    agent = Agent(4,2)
    NUM_EPISODE = 300
    score_list = []
    for e in range(NUM_EPISODE):
        score = 0
        done = False
        obs = env.reset()
        while not done:
            #env.render()
            action = agent.get_action(obs)
            obs_,reward,done,_ = env.step(action)
            score += reward
            agent.store(obs,action,reward,obs_,done)
            agent.learn()
            obs = obs_
        agent.sync()
        score_list.append(score)
        print(f'{e+1}/{NUM_EPISODE} # Score: {score:.1f}, Average Score: {np.mean(score_list[-50:]):.1f}  ',end = '')
        print(f'Epsilon: {agent.epsilon:.2f}')