import serial
from DDPGAgent import Agent
from Environment import Env
import gym
import numpy as np
from Rule import Rule

if __name__ == '__main__':
    env = Env()
    rule = Rule()
    agent = Agent(rule)
    score_list = []
    MAS_list = []
    for e in range(rule.n_episode):
        score = 0
        done = False
        obs = env.Ardread()
        while not done:
            action = agent.get_action(obs)
            for _ in range(3):
                obs_,reward,done = env.step(action)
            score += reward
            agent.replaybuffer.store(obs,action,reward,obs_,done)
            agent.learn()
            obs = obs_
        #episode is ended.
        env.restart()
        agent.save()
        score_list.append(score)
        average_score = np.mean(score_list[-50:])
        MAS_list.append(average_score)
        print(f'{e+1}/{rule.n_episode} # Score: {score:.1f}, Average Score: {average_score:.1f}')
    env.end()
    plt.plot(np.arange(rule.n_episode), MAS_list)
    plt.xlabel('Epochs')
    plt.ylabel('Moving Average Score')
    plt.title('Aruduino RL Car')
    plt.show()