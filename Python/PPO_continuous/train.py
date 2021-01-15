import serial
from Agent import Agent
from Environment import Env
import gym
import numpy as np
import matplotlib.pyplot as plt


n_episode = 20
save_cycle = 1
load = False
#Hyperparameters for Training
lr = 1e-4 #2.5e-5
gamma = 0.99
lmbda = 0.95
epsilon = 0.2
#Hyperparameters for Environment
state_dim = 3
action_dim = 2
#Hyperparameters for buffer
buffer_size = 1000
batch_size = 512
k_epochs = 10

if __name__ == '__main__':
    env = Env()
    agent = Agent(state_dim, action_dim, lr, gamma, lmbda, epsilon, buffer_size, batch_size, k_epochs)
    score_list = []
    mas_list = []
    for e in range(n_episode):
        score = 0
        done = False
        obs = env.Ardread()
        while not done:
            action, log_prob = agent.get_action(obs)
            obs_,reward,done = env.step(action)
            print(obs_, action)
            score += reward
            agent.store(obs,action,log_prob,reward,obs_,done)
            obs = obs_
            agent.learn()
        #episode is ended.
        env.restart()
        agent.save()
        score_list.append(score)
        average_score = np.mean(score_list[-100:])
        mas_list.append(average_score)
        print(f'{e+1}/{n_episode} # Score: {score:.1f}, Average Score: {average_score:.1f}')
    env.end()
    plt.plot(mas_list)
    plt.xlabel('Episode')
    plt.ylabel('Moving Average Score')
    plt.title('Aruduino RL Car')
    plt.show()