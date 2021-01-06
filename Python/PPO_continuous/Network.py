import torch
import torch.nn as nn


class Network(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Network, self).__init__()
        self.fcnet = nn.Sequential(nn.Linear(state_dim, 64),
                                   nn.ReLU(),)
        self.critic = nn.Linear(64, 1)
        self.mu_net = nn.Sequential(nn.Linear(64,action_dim),
                                    nn.Tanh())
        self.std_net = nn.Sequential(nn.Linear(64, action_dim),
                                     nn.Softplus())
        self.apply(self._weights_init)
        self.cuda()                                     
    
    def forward(self, state):
        x = self.fcnet(state)
        value = self.critic(x)
        mu = self.mu_net(x)
        std = self.std_net(x)
        return (mu, std), value
    
    @staticmethod
    def _weights_init(m):
        if isinstance(m, nn.Linear):
            nn.init.xavier_uniform_(m.weight, gain=nn.init.calculate_gain('relu'))
            nn.init.constant_(m.bias, 0.1)
