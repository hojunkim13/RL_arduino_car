import gym

class Rule:
    def __init__(self):
        self.n_episode = 20
        self.save_cycle = 1
        self.load = False
        
        self.env_name = 'RL_Car'

        #Hyperparameters for Training
        self.alpha = 1e-4 #2.5e-5
        self.beta = 1e-3 #2.5e-4
        self.gamma = 0.99
        self.tau = 5e-3

        #Hyperparameters for Environment
        
        self.state_dim = 3
        self.action_dim = 2

        #Hyperparameters for ReplayBuffer
        self.maxlen = 1000000
        self.batch_size = 64
        
        #Nfor Network
        self.fc1_dim = 400
        self.fc2_dim = 300