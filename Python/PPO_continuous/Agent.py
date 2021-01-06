import torch
from torch.optim import Adam
from Network import Network
import torch.nn.functional as F
import numpy as np
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler


class Agent:
    def __init__(self, state_dim, action_dim, lr, gamma, lmbda, epsilon, buffer_size, batch_size, k_epochs):
        self.state_dim = state_dim
        self.action_dim = action_dim

        self.net = Network(state_dim, action_dim)
        
        self.optimizer = Adam(self.net.parameters(), lr = lr)
        self.path = './model/' + 'RL_Car.pt'
        self.gamma = gamma
        self.lmbda = lmbda
        self.epsilon = epsilon
        self.buffer_size = buffer_size
        self.batch_size = batch_size

        self.S = np.zeros((buffer_size, state_dim), dtype = 'float')
        self.A = np.zeros((buffer_size, action_dim), dtype = 'float')
        self.P = np.zeros((buffer_size, action_dim), dtype = 'float')
        self.R = np.zeros((buffer_size, state_dim), dtype = 'float')
        self.S_ = np.zeros((buffer_size, state_dim), dtype = 'float')
        self.D = np.zeros((buffer_size, state_dim), dtype = 'bool')
        self.mntr = 0

    def get_action(self, state):
        state = torch.Tensor(state).cuda().view(-1, self.state_dim)
        (mu,std) = self.net(state)[0]
        dist = torch.distributions.Normal(mu,std)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return action[0].detach().cpu().numpy(), log_prob[0].detach().cpu().numpy()

    def learn(self):
        if self.mntr != self.buffer_size:
            return
        S  = torch.from_numpy(self.S).cuda()
        A  = torch.from_numpy(self.A).cuda()
        log_prob_old  = torch.from_numpy(self.A).cuda()
        R  = torch.from_numpy(self.R).cuda()
        S_ = torch.from_numpy(self.S_).cuda()
        D  = torch.from_numpy(self.D).cuda().bool()

        advantage, td_target = self.get_advantage()
        
        for _ in range(self.k_epochs):
            for index in BatchSampler(SubsetRandomSampler(range(self.buffer_size)), self.batch_size, False):
                (mu,std), value = self.net(S)
                dist = torch.distributions.Normal(mu, std)
                log_prob_new = dist.log_prob(A)
                ratio = torch.exp(log_prob_new - log_prob_old)
                surrogate1 = ratio * advantage
                surrogate2 = torch.clip(ratio, 1-self.epsilon, 1+self.epsilon) * advantage
                a_loss = -torch.min(surrogate1, surrogate2).mean()
                v_loss = F.smooth_l1_loss(value, td_target)
                self.optimizer.zero_grad()
                (a_loss + v_loss).backward()
                self.optimizer.step()
        self.mntr = 0

        
    def store(self, s, a, log_prob, r, s_, d):
        idx = self.mntr
        self.S[idx] = s
        self.A[idx] = a
        self.P[idx] = log_prob
        self.R[idx] = r
        self.S_[idx] = s_
        self.D[idx] = d
        self.mntr +=1

    def get_advantage(self, S, R, S_, D):
        with torch.no_grad():
            value = self.net(S)[1]
            value_ = self.net(S_)[1]
        td_target = R + value_ * self.gamma * ~D
        delta = td_target - value

        advantage = torch.zeros_like(delta)
        running_add = 0
        for i in reversed(range(len(delta))):
            advantage[i] = delta[i] + running_add * self.gamma * self.lmbda
            running_add = advantage[i]
        return advantage, td_target

    def save(self):
        torch.save(self.net.state_dict(), self.path)

    def load(self):
        self.net.load_state_dict(torch.load(self.path))