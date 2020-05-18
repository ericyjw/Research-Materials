import numpy as np
import gym
import random
import time

env = gym.make("FrozenLake-v0")

action_space_size = env.action_space.n
state_space_size = env.observation_space.n

q_table = np.zeros((state_space_size, action_space_size))

print(q_table)

num_episodes = 10000
max_steps_per_episode = 100

# alpha
learning_rate = 0.1
# gamma
discount_rate = 0.99
# ebsilon -> initailly full exploration
exploration_rate = 1

max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.01

rewards_all_episodes = []

# Q-learning algorithm
for episode in range(num_episodes):
    # initialize new episode params
    state = env.reset()
    done = False
    rewards_current_episode = 0
    
    for step in range(max_steps_per_episode):
        # Exploration-exploitation trade-off
        # Find whether to explore or exploit at this step
        exploration_rate_threshold = random.uniform(0,1)
        if exploration_rate_threshold > exploration_rate:
        	action = np.argmax(q_table[state, :])
        else:
        	action = env.action_space.sample()

        # Take new action based on the policy chosen (explore/exploit)
        new_state, reward, done, info = env.step(action)

        # Update Q-table for Q(s,a)
        # New Q-value = Weighted sum of the Old Value and the Learned Value
        # Learned value = Reward from taking an action from a state + Discounted estimate of the optimal future Q-value for the next state-action pair (s',a') at time t+1
        # Discounted estimate of the optimal future Q-value = discount_rate * max(NEXT state action pair)
        q_table[state, action] = (1 - learning_rate) * q_table[state, action] + \
                                  learning_rate * \
                                      (reward + discount_rate *
                                       np.max(q_table[new_state, :]))

        # Set new state
        # Add new reward
        state = new_state
        rewards_current_episode += reward

        if done == True:
        	break

    # Exploration rate decay
    # Done at the end of each episode, so the new episode will have a new exploration rate, ebsilon
    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)

    # Add current episode reward to total rewards list
    rewards_all_episodes.append(rewards_current_episode)
    
rewards_per_thosand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/1000)
count = 1000

print("********Average reward per thousand episodes********\n")
for r in rewards_per_thosand_episodes:
	print(count, ": ", str(sum(r/1000)))
	count += 1000

# Print updated Q-table
print("\n\n********Updated Q-table********\n")
print(q_table)

print("\n\n********Play the game with the Trained Model********\n")
for episode in range(3):
    # initialize new episode params
    state = env.reset()
    done = False
    print("*****EPISODE ", episode+1, "*****\n\n\n\n")
    time.sleep(1)

    for step in range(max_steps_per_episode):        
        # Show current state of environment on screen
        env.render()
        time.sleep(0.3)
        # Choose action with highest Q-value for current state
        action = np.argmax(q_table[state,:])        
        new_state, reward, done, info = env.step(action)      
        # Take new action
        if done:
            if reward == 1:
                # Agent reached the goal and won episode
                print("****You reached the goal!****")
                time.sleep(3)
            else:
                # Agent stepped in a hole and lost episode
                print("****You fell through a hole!****")
                time.sleep(3)          
            break
        # Set new state
        state = new_state
        
env.close()