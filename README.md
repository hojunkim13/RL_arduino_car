# Reinforcement Learning on Arduino Car

Implementation RL algorithms on arduino car.  
Arduino car learn from real environment as an agent.  

  ## Usage
  * Arduino (Agent / Environment)  
    * Arduino Uno  
    * Arduino Sensor Shield  
    * Ultrasonic Sensor * 3  
    * Servo Moter * 4  
    * Arduino Motor Driver  
    * Bluetooth Module (for connecting with PC)  
  
  * Python (Brain)  
    * pytorch  
    * pySerial  
    * etc.  
  
  
## Implementation Algorithm  
#### DQN Algorithm (for discrete action space)  - *removed
  DQN Algorithm works good. but it can work only discrete action space.  
#### DDPG Algorithm (for continuous action space)  
  DDPG is slower then DQN, but it can make agent do soft action!

## To do
* implementation PPO Algorithm (Discrete, continuous)
