# Research-Materials

## Genetic Algorithm
---
Genetic algorithm reflects the process of Natural Selection. Natural Selection is a process where the fittest individuals from a population is elected to produce an offspring, which inherits the characteristics of the parents. The offspring is then added into the next generation. The fittest survives and the process continues until all the individuals in a generation is the fittest.

### Six Phases of Genetic Algorithm
#### Initial Population
- A set of individuals is selected as a **Population**.
- Each individual is a solution to the problem on hand.
- Each individual is characterised by a set of variables (**Genes**).
- Genes are combined together to form a **Chromosome** (solution).

#### Fitness Function
- Determines the individual's ability to compete with another individual.
- Gives a fitness score to each individual.

#### Selection
- The fittest individuals are selected and their genes are passed to the next generation.
- The higher the fitness score, the more likely the individual is getting selected.

#### Crossover
- Most important part of the genetic algorithm
- For each pair of parents to be mated, a crossover point is chosen at random from within the genes.
- Offspring are created by exchanging the genes of parents among themselves until the crossover point is reached.
- New offsprings are added to the population.
- The population has a fixed size. As new generations are formed, individuals with least fitness die, providing space for new offspring.
- The sequence of phases is repeated to produce individuals in each new generation which are better than the previous generation.

#### Mutation
- In some new offspring formed, some of their genes can be subjected to a mutation with a **low random probability**.
- Mutation maintain diversity within the population and **prevent premature convergence**.

#### Termination
- Terminates if the population has converged, there the population does not produce offspring which are significantly different from the previous generation.
- Individuals in that generation is the solutions to the problem on hand.





## Supervised Learning
---
Supervised Learning is the process of learning with training labels. It is most widely used kind of learning for AI. Supervised Learning has a **supervisor**, who will points out the mistakes to the AI. After training the AI with a large data set, the AI should be able to correctly process a new unique task.

### Unsupervised Learning
* Clustering or grouping
* E.g. Find patterns in the Frames of the video and compress those frames so that the videos can be streamed to us more quickly


### Supervised Learning Process
- Initially, random weight is given to the variable inputs and the bias for the AI to make a decision.
- As the AI is fed with more data, the bias will be updated accordingly.
- For each data, the input variable will multiplied by their weight and bias, and the summation will be passed to a mathematical function. These are possible Activation Functions:
	- Unit Step (Heavy Side): 0 or 1
	- Sign (SIGNUM): -1 or 1
	- Linear
	- Piece-Wise Linear
	- Logistic (Sigmoid)
	- Hyperbolic Tangent
- The output from the Activation Function will correspond to an answer for the problem.
- The weight and bias are used to calculate the **decision boundary** on the graph, where initially it is randomly created.
- **Learning from failure and not success**
	- Upon mistake, the old weight is added with a number and then calculated by the **Update Rule** 
	- If the AI is correct, the weight remains the same.	

### Analysing AI's Decision
#### Confusion Matrix
- Accuracy = Total Correct / Total Decisions
- Precision
	- Indicates how much you should trust the AI's decision
	- If you give the AI Object A, the AI has _x_% chance of getting it right
	- Precision = True Positive / (True Positive + False Positive)
- Recall
	- Indicates how much the AI can find the thing you are looking for
	- Of the total number of Object A, the AI only identify _x_% correctly
	- Recall = True for A / (True for A + False for A)
	- Depends on the criteria the AI is using to make a decision

### Challenges
- To figure out the correct criteria to train the AI with
- More data input means more accuracy but also more processing power and time to make decision

**Need to prioritise goals (High Precision vs High Recall)**





## Neural Network Training
---
Neural Network Training learns to solve problems by making mistakes. If a neural network makes mistakes, it means that the weight on each neurons are not adjusted correctly and needs to update them so that better prediction can be made in the future.

### Optimisation
The task of finding the best weight for a neural network architecture
#### Linear Regression
- Start by drawing a random straight line on the graph.
- Find the distance between the data points and the line to calculate the error, how big a mistake is made.
- Adjust the error to the minimal to find the best-fit line.

___* Some parts of the graph will defy logic.___
___* Not optimal for large number of variables___
#### Neural Network
- Each variable is a node and set random weight on each node.
- Train the model by giving the data of past events (inputs and outputs).
- Each node will multiple their weight with the inputs and adding them together.
- The results is the passed to the hidden layers until the output nodes.
- The difference between the output value and the actual output is the error, and is represented in the loss function.

#### Back-Propagation
- Look at the loss function and the assign blame to the nodes back in the previous layers of the network.
- Some nodes are adjusted more than the others as their calculation may have been more to blame for the error than the others'.

___* Goal is to find the best combination of weights to get the lowest error___
##### Global Optimal Solution vs Local Optimal Solution
__Global Optimal Solution__: a solution that is optimal where the error is minimal
__Local Optimal Solution__: a solution where the weights make the error relatively small but not minimal
The way to overcome Local Optimal Solution is to re-run the model at different starting points or run the model with multiple starting points. This increases the chance of finding the global optimal solution, by cross-checking all the output results. 

##### Learning Rate
The weight the neurons adjusted every time back propagation happens


### Fitting to Training Data
Large number of input variables will increase the accuracy of the model. But random irrelevant input variables may find unrelated relationships between the inputs and outputs, and affect the accuracy and reliability of the outputs (__Overfitting__). It is important to keep the neural network simple and avoid irrelevant inputs.





## Reinforcement Learning 
---
Reinforcement Learning is the process of learning in an environment through feedback from an AI's behaviour. Reinforcement Learning can train AI to perform complicated tasks, but only providing the answer to the solution at the end of the task and then asking the AI how it did it. It involves trial-and-error over many iterations. Unlike Supervised Learning, we do not know what is the right decision until the task is done.

### Reinforcement Learning Process
- AI will interact with the environment until it achieve the end goal.
- Every time the agent success at its task, we look back on the actions taken to achieve the end goal.
- We then figure out which states are helpful and which are not.
- During this reflection, we then assign values to each of these states, and on a **Policy** for which actions work best.
	- Value: Higher values is given for states that help to achieve the end goal. 
		- Helps with the trial-and-error reinforcement learning
		- Gives the AI more information about better actions to take when the task is repeated
	- Policy: Exploration vs Exploitation
		- Need a balance between both
		- More complicated with different rewards in placed
		- More complicated with non-deterministic environment
	- Value Function is used to determine the values assigned to each state
		

### Challenges
- Credit Assignment
	- Difficult to know which actions helps to get the reward and thus the credit
	- Difficult to know which actions slowed down the AI, without pausing at each action to think
- Exploitation vs Exploration
	- Exploitation: keep using existing knowledge to do the same tasks
		- Able to get the job done all the time
		- May not be the more efficient way
	- Exploration: trying different strategies to achieve the same end goal
		- Have more information and thus able to make better decisions in the future for the same task
		- Take more time in the short run, but more efficient in the long run
- Require lots of time and data

### Markov Decision Processes (MDPs)
#### Components:
- Agent: the decision maker
- Environment
- State: the representation of the environment
- Action: the action that the agent take at a given state
- Reward: the reward given to the agent as a consequence of the previous action

The process of selecting an action from a given state, transitioning to a new state, and receiving a reward happens sequentially repeatedly, creating a **trajectory** that shows the sequence of states, actions and rewards.

Throughout this process, the agent's goal is to **maximise the total amount of rewards that it receives from taking actions in a given state**. The goal is to maximise not just the immediate reward, but also the **cumulative rewards** it receives in the long run.

#### MDP Notation
S -> a set of states
A -> a set of actions
R -> a set of rewards
**Assume that each of these sets have a finite number of elements**

At each time step t = 0,1,2,...,T, the agent will be in $S_{t} \in S$. At each state, the agent will select an action $A_{t} \in A$. This results in a state-action pair ($S_{t}, A_{t}$).

Time step is then incremented to the next time step, t+1, and the environment is transitioned to a new state $S_{t+1} \in S$. At this time, the agent receives a reward $R_{t+1} \in R$ for action $A_{t}$ taken in state $S_{t}$. 

Resulting function: $f(S_{t},A_{t}) = R_{t+1}$

Since the sets S and R are finite, the random variable $R_{t}$ and $S_{t}$ have well defined probability distributions, and all possible values can be assigned to $R_{t}$ and $S_{t}$ have some associated probability. These distributions depends on the **preceding** state $s \in S$ and action $a \in A(s)$.

For all $s' \in S$, $s \in S$, $r \in R$ and $a \in A(s)$, the probability of the transition state to s' with reward r from taking action a in state s is:
p(s',r|s,a) = Pr{$S_{t} = s', R_{t} = r| S{t-1} = s, A_{t-1} = a$}

#### Expected Return
$G_{t} = R_{t+1} + R_{t+2}+ \cdots + R_{T}$, where T is the final time step.
The agent's goal is to maximise the expected return of rewards.
This concept of expected rewards is the factor that drives the agent to make the decisions it make.
However, this concept of expected returns requires the tasks to be **episodic**.

- Episodic: a task that has a finite time step / will eventually end. The task is then restart to a  beginning state independent of the previous state in the previous episode.

#### Discounted Return
Instead of the agent's goal being to maximise the expected return of rewards, the agent's goal is to **maximise the expected DISCOUNTED return of rewards**.

Discount rate, γ, is a number between 0 and 1. The discounted rate will be the rate for which we discount the **future** rewards, and will determine the present value of future rewards. With this, we define the discounted return as:
$G_{t} = R_{t+1} + γR_{t+2} + γ^{2}R_{t+3} + \cdots $ <br/>  
$G_{t} = R_{t+1} + γG_{t+1}$, where reward > 0 and Constanta and γ < 1

Discounted Return causes the agent to care more about the immediate reward over future rewards, since the future rewards will be more heavily discounted. 

#### Policies
Policies address the question: "How probable is it for an agent to select any action from a given state?"

A policy is a function that **maps a given state to probabilities of selecting each possible action from that state**. The symbol π to denote a policy. 

If an agent follows policy π at time t,
Probability of taking action a in state s = π(a|s),
where each state $s \in S$ and,
π is a probability distribution over $a \in A(s)$

#### Value Functions
Value Functions address the question: "How good is any given action or any given state for an agent?"

Value functions are functions of states, or of state-value pairs, that estimate how good it is for an agent to be in a given state, or how good it is for the agent to perform a given action is a given state.

This notion of how good a state or state-action pair is is given in terms of expected return. Value functions are defined with respect to specific ways of acting. Since the way an agent acts is influenced by the policy it's following, then we can see that value functions are defined with respect to policies.

##### State-Value Function
The state-value function for policy π, denoted as $v_{π}$, tells us **how good any given state is** for an agent following policy π. It gives the value of a state under π.

Formally, the value of state s under policy π is the expected return from starting from state s at time t and following policy π thereafter.
$v_{π}(s) = E_{π}[G_{t} | S_{t} = s]$

##### Action-Value Function
The action-value function for policy π, denoted as $q_{π}$, tells us **how good it is for the agent to take any given action from a given state** while following policy π. It gives the value of an action under π.

Formally, the value of action a in state s under policy π is the expected return from starting from state s at time t, taking action a, and following policy π thereafter. 
$q_{π}(s,a) =  E_{π}[G_{t} | S_{t} = s, A_{t} = a]$

Action-Value Function $q_{π}$ is referred as the Q-function, and the output of the function for any given state-action pari is call a Q-value, where "Q" represents the quality of taking a given action in a given state.

#### Optimality
The goal of reinforcement learning algorithms to find a policy that will yield a lot of rewards for the agent if the agent indeed follows that policy. 

##### Optimal Policy
In terms of return, a policy π is considered to be better than to the same as policy π' if the expected return of π is the greatest than or equal to the expected return of π' for all states. 
$π \ge π'$ iff $v_{π}(s) \ge v+{π'}(s)$, for all $s \in S$

Note: **$v_{π}(s)$ gives the expected return for starting in state s and following π thereafter**.

##### Optimal State-Value Function
The optimal policy has an associated optimal state-value function and the optimal state-value function is denoted as $v_{∗}$ and
$v_{∗} = max_{\pi}v_{\pi}(s)$, for all $s \in S$,
and $v_{∗}$ gives the largest expected returns achievable by any policies $\pi$ for **each state**

##### Optimal Action-Value Function
The optimal policy has an optimal action-value function, or optimal Q-function, which we denote as $q_{\ast}$ and 
$q_{\ast}(s,a) = max_{\pi}q_{\pi}(s,a)$, for all $s \in S$ and $a \in A(s)$,
and $q_{\ast}$ gives the largest expected return achievable by any policy $\pi$ for **each state-action pair**

#### Bellman Optimality Equation For $q_{*}$
$q_{\ast}(s,a) = E[R_{t+1} + γmax_{a'}q_{\ast}(s',a')]$

Bellman Optimality Equation states that,
For any state-action pair (s,a) at time t, the expected return from starting in state s, selecting action a and following the optimal policy thereafter, is going to be the expected reward we get from taking action a in state s, which is $R_{t+1}$, plus the maximum expected discounted return that can be achieved from any possible next state-action pair (s',a').

Since the agent is following an optimal policy, the following state s' will be the state from which the best possible next action a' can be taken at time t+1.

**The aim is to use Bellman equation to $q_{\ast}$, and use $q_{\ast}$ to determine the optimal policy because with $q_{\ast}$ for any state s, an reinforcement learning algorithm can find the action a that maximises $q_{\ast}(s,a)$.**

#### Q-Learning Objective
The objective of Q-learning is to:
- **find a policy that is optimal in the sense that the expected value of the total reward over all successive steps is the maximum achievable**
- **find the optimal policy by learning the optimal Q-values for each state-action pair**

#### Q-Learning With Value Iteration
Q-Function / Action-Value Function: $q_{π}(s,a) =  E_{π}[G_{t} | S_{t} = s, A_{t} = a]$
Bellman Optimality Equation: $q_{\ast}(s,a) = E[R_{t+1} + γmax_{a'}q_{\ast}(s',a')]$

##### Value Iteration
The **Q-learning algorithm** iteratively updates the Q-values for each state-action pair using the Bellman equation until the Q-function converges to the optimal Q-function, $q_{\ast}$. This approach is called **value iteration**.

At the start, the agent has no idea how good any action is from any given state. It is not aware of anything besides the current state of the environment. **Therefore, the Q-values for each state-action pair is all initialised to zero.** Through the course, the Q-values for each state-action pair will be iteratively updated using value iteration.

##### Storing Q-Values in a Q-table
Q-table stores the Q-values for each state-action pair. The horizontal axis of the table represents the actions, and the vertical axis represents the states. So, the dimensions of the table are the number of actions by the number of states.

Initially, all the Q-values in the table are initialised to zero.Overtime, the Q-values produced for the state-action pairs that the agent experiences will be used to update the Q-values stored in the Q-table. As the Q-table becomes updated, **in later moves and later episodes**, the agent can look in the Q-table and base its next action on the highest Q-value for the current state.

##### Episodes
During the episodes, the learning process will take place. In each episode, the agent starts out by choosing the action based on which action has the highest Q-value in the Q-table for the current state. However, at the very first state of the very first episode, all the Q-values are zero and the agent will take a random pick on the action to take.

##### Exploration vs Exploitation
- Exploration: the act of exploring the environment to find out information about it
- Exploitation: the act of exploiting the information that is _already known_ about the environment in order to maximise the return

Exploitation may result in short term benefit and long term loss, while Exploration allows the optimal solution to be discovered. However, if there is only exploration and no exploitation, the agent will miss out on making use of known information that could help to maximise the return.

#### Epsilon Greedy Strategy
Epsilon Greedy Strategy is used to get a balance between exploitation and exploration. The exploration rate ϵ is **initially set to 1**. The exploration rate is the **probability that the agent will explore the environment rather than exploit it**. 

With ϵ = 1, it is 100% certain that the agent will start out by exploring the environment. As the agent learns more about the environment, at the start of each new episode, **ϵ will decay by some rate**. Therefore, the likelihood of exploration becomes less probable as the agent learns more about the environment. The agent will become “greedy” in terms of exploiting the environment once it has had the opportunity to explore and learn more about it.

To determine whether the agent will choose exploration or exploitation at each time step, a random number between 0 and 1 is generated. 

- If the **number is greater than epsilon**, then the agent will choose its next action via **exploitation**, and will choose the action with the highest Q-value for its current state from the Q-table. 
- If the **number is less than or equal to epsilon**, the agent's next action will be chosen via exploration and randomly choosing its action and exploring what happens in the environment.

##### Updating the Q-Value
To update the Q-value for the action taken from the previous state, Bellman equation is used.
Bellman Optimality Equation: $q_{\ast}(s,a) = E[R_{t+1} + γmax_{a'}q_{\ast}(s',a')]$

The objective is to make the Q-value for the given state-action pair as close as to the right hand side of the Bellman equation so that the Q-value will eventually converge to the optimal Q-value $q_{∗}$.This will happen over time by iteratively comparing the loss between the Q-value and the optimal Q-value for the given state-action pair and then updating the Q-value over and over again each time the agent encounter the **same state-action pair** to reduce the loss.
loss = $q_{*}$(s,a) - $q(s,a)$
loss = $E[R_{t+1} + γmax_{a'}q_{\ast}(s',a')]$ - $E_{π}[G_{t} | S_{t} = s, A_{t} = a]$

##### Learning Rate
The learning rate is a number between 0 and 1, which can be thought of as how quickly the agent abandons the previous Q-value in the Q-table for a given state-action pair for the new Q-value.

Instead of just overwriting the old Q-value, learning rate is used as a tool to determine how much information to keep about the previously computed Q-value for the given state-action pair versus the new Q-value calculated for the same state-action pair at a later time step. We’ll denote the learning rate with the symbol α.

The higher the learning rate, the more quickly the agent will adopt the new Q-value.

Formula for calculating the new Q-value for state-action pair (s,a) at time t is:
$q^{new}(s,a) = (1-\alpha) q(s,a) + \alpha(R_{t+1} + γmax_{a'}q(s',a')$,
where $q(s,a)$ is the old value

The new Q-value is equal to a weighted sum of the old value and the learned value. The learned value is the reward the agent receives from taking an action from a state plus the discounted estimate of the optimal future Q-value for the next state-action pair (s',a') at time t+1. The entire learned value is then multiplied by the learning rate. γ is a predefined value.

The new Q-value calculated is then stored in our Q-table for that state-action pair. This process is needed for every single time step and will repeat until termination for each episode. The termination can either be auto terminated by the agent via winning or losing, or by reading the maximum allowed time steps predefined.


Once the Q-function converges to the optimal Q-function, optimal policy is obtained.





## TensorFlow
---
#### What is TensorFlow
- A Python open source library by Google
- Used for numerical computation and large-scale machine learning
- Ease the process of acquiring data, training models, serving predictions, and refining future results
- Can train and run deep neural networks for:
	- Handwritten digit classification
	- Image recognition
	- Word embeddings
	- Recurrent neural networks
	- Sequence-to-sequence models for machine translation
	- Natural language processing
	- PDE (partial differential equation) based simulations
- Transformation libraries are written in C++ binaries, and Python hooks them up through high level abstractions
- Can run on a local machine, a cluster in the cloud, iOS and Android devices, CPUs or GPUs
- If using Google cloud, can run TensorFlow on Google’s custom TensorFlow Processing Unit (TPU) silicon for further acceleration

#### Benefits
- Provides high level abstraction machine learning development
- Convenient in debugging and gain introspection into TensorFlow apps
	- Able to evaluate and modify each graph operation separately and transparently, instead of contracting the entire graph as a single opaque object and evaluating it as a whole
	- Able to inspect and profile they way graph runs using interactive web-based dashboard

#### Drawbacks
- Non-deterministic
	- Hard for deterministic model-training jobs

## Machine Learning & Deep Learning Fundamentals
---
### Machine Learning
- Machine learning is the practice of using algorithms to analyse data, learn from that data, and then make a determination or prediction about new data.
- Rather than manually writing code with a specific set of instructions to accomplish a specific task, the machine is trained using data and algorithms that give it the ability to perform the task without being explicitly being told how to do so.


### Deep Learning
- Deep learning is a **sub-field** of machine learning that uses algorithms **inspired by the structure and function of the brain's neural networks**.
- Are machine learning algorithms that learn from data but now the learning are based loosely on the structure and function of the brain's neural networks - **artificial neural networks (ANNs)**


### Artificial Neural Network (ANN)
- An artificial neural network is a computing system that is comprised of a collection of connected units called neurons that are organised into layers
- Connected neural units form the network
- Each connection between neurons transmits a signal from one neuron to the other. The receiving neuron processes the signal and signals to downstream neurons connected to it within the network.
- Different layers perform different kinds of transformations on their inputs
- Input layer -> Hidden layers -> Output layer [Forward pass through the network]


### Layers in Neural Network
- Type of layers:
	- Dense (or fully connected) layers
	- Convolutional layers
	- Pooling layers
	- Recurrent layers
	- Normalization layers
- Different layers perform different transformations on their inputs, and some layers are better suited for some tasks than others.
	- Convolutional layer for image data.
	- Recurrent layers for time series data
	- Fully connected layers fully connects each input to each output within its layer.
- Layer Weight
	- Each connection between two nodes has an associated weight.
	- Each weight represents the strength of the connection between the two nodes.
- Input in the input layer -> connection to 2nd layer -> input multiply by the weight of connection
- For each node in 2nd layer, a weighted sum is then computed with each of the incoming connections. This sum is then passed to an activation function, which performs some type of transformation on the given sum.
	- **Node output = activation(weighted sum of inputs)**
- As the model learns, the weights at all connections are updated and optimised so that the input data point maps to the correct output prediction class. 


### Activation Functions
- An activation function is a function that maps a node's inputs to its corresponding output
- Node output = activation(weighted sum of inputs)
- The activation function does some type of operation to transform the sum to a number that is often times between some _lower limit_ and some _upper limit_. This transformation is often a _non-linear transformation_.
- Example: Sigmoid Activation Function (Sigmoid)
	- For most negative inputs, sigmoid will transform the input to a number very close to 0.
	- For most positive inputs, sigmoid will transform the input into a number very close to 1.
	- For inputs relatively close to 0, sigmoid will transform the input into some number between 0 and 1.
	- For sigmoid, 0 is the lower limit, and 1 is the upper limit.
- Example: Relu Activation Function (ReLU)
	-  _Rectified linear unit_,transforms the input to the maximum of either 
0 or the input itself -> relu(x) = max(0,x)
- Most activation functions are non-linear and allow the neural networks to compute arbitrarily complex functions

### Training a Neutral Network
- Optimising the weight in the model
- Use optimising algorithm, like _stochastic gradient descent(SGD)_
- Objective is to minimise the loss function, so that the loss function is as close to its minimum value as possible
- Most common loss function: _mean squared error (MSE)_
- Final output is a set of probabilities of the choices
- Loss = difference between what the network predicting prediction versus the true label
- SGD will then try to minimise the error to make the model as accurate as possible in its predictions
- After passing all of the data, the SAME data is passed in over and over again - **training**


### Learning In Artificial Neural Networks
- Epoch -> a single pass of the entire dataset to the network during training.
- Once the output is obtained, the loss can be computed for that specific output by looking at what the model predicted versus the true label. The loss computation depends on the chosen loss function
- After the loss is calculated, the gradient of the loss function is computed with respect to each of the weights within the network.
	- Calculated the loss of a single output
	- Calculate the gradient of that loss with respect to our single chosen weight
- This calculation is done using a technique called **backpropagation
- The gradient of the loss function calculate is then used to update the model’s weight. The gradient tells us which direction will move the loss towards the minimum value.
- The gradient value is multiplied by the **learning rate**
	- small number usually ranging between 0.01 and 0.0001
	- tells us how large of a step we should take in the direction of the minimum
- **New Weight = Old Weight - (Learning Rate * Gradient)**
- **The value for the gradient is going to be different for each weight because the gradient is being calculated with respect to each weight**
- All these weights being iteratively updated with each epoch. The weights are going to be incrementally getting closer and closer to their optimised values while SGD works to minimise the loss function.



### Loss in Neural Network
- Loss function is what optimising algorithm is attempting to minimise by iteratively updating the weights in the network.
- At the end of each epoch during the training process, the loss will be calculated using the network’s output predictions and the true labels for the respective input.
- Error = difference between the model’s prediction and the true label 
	- (1,0) vs (0.25, 0.75)
	- Error = 1 - 0.25
- This process is performed for every output. For each epoch, the error is accumulated across all the individual outputs.
- Mean Squared Error
	- MSE(input) = (output - label)(output - label)
	- If we passed our entire training set to the model at once (batch_size=1), then the process we just went over for calculating the loss will occur at the end of each epoch during training.
	- If we split our training set into batches, and passed batches one at a time to our model, then the loss would be calculated on each batch.
	- With either method, since the loss depends on the weights, we expect to see the value of the loss change each time the weights are updated.
- Given that the objective of SGD is to minimise the loss, we want to see our loss decrease as we run more epochs.


### Learning Rates And Neural Networks
- Learning rate too big -> risk the possibility of overshooting
	- Take a step that’s too large in the direction of the minimised loss function and shoot past this minimum and miss it.
- Learning rate too small -> steps will be really small
	- Take us a lot longer to reach the point of minimised loss.
- Trade off between a higher learning rate and a lower learning rate

### Train, Test, & Validation Sets
- Training Set
	- The set of data used to train the model
	- During each epoch, the model will be trained over and over again on this same data in our training set, and it will continue to learn about the features of this data.
	- Objective: the model is able to accurately predict on new data that it’s never seen before and be making these predictions based on what it’s learned about the training data.
- Validation Set
	- The set of data, separate from the training set 
	- Gives information that may assist in adjusting the hyperparameters.
	- While the model is train in each epoch, it is also simultaneously validated on the data in the validation set.
		- **The weights will not be updated in the model based on the loss calculated from our validation data.**
	- Ensure that the model is not overfitting to the data in the training set.
		- Overfitting -> the model becomes really good at being able to classify data in the training set, but it’s unable to generalise and make accurate classifications on data that it wasn’t trained on.
	- **During training, if we’re also validating the model on the validation set and see that the results it’s giving for the validation data are just as good as the results it’s giving for the training data, then we can be more confident that our model is not overfitting.**
		- But if the results on the training data are really good, but the results on the validation data are lagging behind, then our model is overfitting.
- Test Set
	- The set of data that is used to test the model after the model has already been trained.
	- The test set is separate from both the training set and validation set.
	- Use to predict the output of the unlabeled data in the test set
	- One major difference between the test set and the two other sets:
		- The test set should not be labeled
		- The training set and validation set have to be labeled so that we can see the metrics given during training, like the loss and the accuracy from each epoch.
	- **Provides a final check that the model is generalising well before deploying the model to production.**

**Ultimate goal of machine learning and deep learning is to build models that are able to generalise well**


### Predicting With A Neural Network
- Predictions are based on what the model learned during training.
	- Tell us how well our model performs on data it hasn’t seen before based on how well its predictions match the true labels for the data.
	- Help give us some insight on what our model has or hasn’t learned
- Need to make sure that the training and validation sets are representative of the actual data we want our model to be predicting on

### Overfitting In A Neural Network 
- Overfitting occurs when the model becomes really good at being able to classify or predict on data that was included in the training set, but is not as good at classifying data that it wasn’t trained on. 
- How to spot Overfitting:
	-  Validation set during training, we get metrics for the validation accuracy and loss and the training accuracy and loss.
	- If the validation metrics are considerably worse than the training metrics, then that is indication that our model is overfitting.
	- If during training, the model’s metrics were good, but when we use the model to predict on test data, it doesn't accurately classify the data in the test set.
- Overfitting = the model is unable to generalise well.
	- It has learned the features of the training set extremely well
	- But if given any data that slightly deviates from the exact data used during training, it’s unable to generalize and accurately predict the output.
- Reducing Overfitting
	- Adding more data to training set
		- More data trained on model = More learning from the training set
		- More data = More diversity to the training set
	- Data Augmentation
		- The process of creating additional augmented data by reasonably modifying the data in the training set
		- For image data, these modifications include:
			- Cropping
			- Rotating
			- Flipping
			- Zooming
		-  Allows us to add more data to our training set that is similar to the data that we already have, but is just reasonably modified to some degree so that it’s not the exact same.
	- Reducing complexity of the model
		- Removing some layers from the model
		- Reducing the number of neurons in the layers
		- Help the model to generalise better to data it hasn’t seen before
	- Dropouts
		- If you add dropout to a model, it will randomly ignore some subset of nodes in a given layer during training
		- Prevent these dropped out nodes from participating in producing a prediction on the data.
		- Helps to generalise better to data it hasn’t seen before.


### Underfitting In A Neural Network 
- Underfitting occurs when it’s not even able to classify the data it was trained on.
- How to spot Underfitting:
	- When the metrics given for the training data are poor
	- Training accuracy of the model is low
	- Training loss is high.
- Reducing Underfitting
	- Increase The Complexity Of The Model
		- If the data is more complex, and we have a relatively simple model, then the model may not be sophisticated enough to be able to accurately classify or predict on our complex data.
		- Increasing the number of layers in the model.
		- Increasing the number of neurons in each layer.
		- Changing what type of layers we’re using and where.
	- Add More Features To The Input Samples
		- These additional features in the training set may help our model classify the data better.
	- Reduce Dropout
		- Dropout is a regularisation technique that randomly ignores a subset of nodes in a given layer. It essentially prevents these dropped out nodes from participating in producing a prediction on the data.
		- Decrease dropout rate
		- These nodes are only dropped out for purposes of training and not during validation.
			- If the model is fitting better to the validation data than it is to the training data, then this is a good indicator to reduce the amount of dropout.


## Supervised Learning For Machine Learning
- Labelled Data: Labels are used to supervise or guide the learning process.
- With supervised learning, each piece of data passed to the model during training is a pair that consists of the input object, along with the corresponding label or output value.
- **With supervised learning, the model is learning how to create a mapping from given inputs to particular outputs based on what it’s learning from the labeled training data**
- Labels are numeric
	- Need to be encoded into something numeric -> 0 for X and 1 for Y
- After labelling, we then determine the loss for all of the data in our training set for as many epochs as we specify. 
	- During this training, the objective of the model is to minimise the loss, so when we deploy our model and use it to predict on data it wasn’t trained on, it will be making these predictions based on the labeled data that it did see during training.


## Unsupervised Learning
- Unsupervised learning occurs with unlabelled data.
- Since the model is unaware of the labels for the training data, there is no way to measure accuracy. 
	- **Accuracy is not typically a metric that we use to analyse an unsupervised learning process**
- Model under unsupervised learning is going to attempt to learn some type of structure from the data and will extract the useful information or features from this data.
- Clustering Algorithm
	- The clustering algorithm could analyse this data and start to learn the structure of it even though it’s not labeled. 
	- Through learning the structure, it can start to cluster the data into groups.
	- Nothing explicitly telling us the labels for this data
		- But can see that there are distinct clusters and can infer the classification from the distinct clusters
- Auto-Encoders
	- Auto-encoders is an artificial neural network that takes in input, and then outputs a reconstruction of this input.
	- Auto-encoders will take in an image of a digit, and it will then encode the image.
	- At the end of the network, it will decode the image and output the decoded reconstructed version of the original image.
	- Objective: to reconstructed the image to be as close as possible to the original image.
	- The more similar the reconstructed image is to the original image, the lower the loss.
	- Since auto-encoder is an artificial neural network, variation of SGD during training can be used and the same objective of minimising the loss function can be achieved.
		- During training, the model is incentivised to make the reconstructed images closer and closer to the originals.
- Applications Of Auto- encoders
	- De-noise images
		-  Once the model has been trained, then it can accept other similar images that may have a lot of noise surrounding them, and it will be able to extract the underlying meaningful features and reconstruct the image without the noise.


## Semi-Supervised Learning
- Semi-supervised learning uses a combination of both labeled and unlabelled data.
- Labelling large unlabelled dataset is not practical
	- Go through and manually label some portion of this large data set ourselves and use that portion to train our model.
- Pseudo-Labelling
	- Labeled some portion of the data set
	- Use the labelled data as the training set for our model to train the model
	- After training the model with labelled data set, the model then predicts on the remaining unlabelled data
	- Take these predictions and label each piece of unlabelled data with the individual outputs that were predicted for them.
	- After labelling the unlabelled data through pseudo-labelling process, the model is then trained on the full dataset, which is now comprised of both the data that was actually truly labeled along with the data that was pseudo labeled.
- Pseudo-labelling allows us to train on a vastly larger dataset.
- Train on data that otherwise may have potentially taken many tedious hours of human labor to manually label the data.


## Data Augmentation
- Data augmentation occurs when we create new data based on modifications of our existing data.
- Reasons for Data Augmentation:
	- Reduce Overfitting
		- Producing new data set by augmenting the original data set increase the size of the data set
- Some data augmentation techniques may not be appropriate to use on the given data set.
	- E.g Horizontally flipping the dog images makes sense, not vertically


## One-Hot Encoding
- Most of the time the labels are encoded, and take on the form of an integer or of a vector of integers
- One-hot encodings transform the categorical labels into vectors of 0s and 1s.
- With each one-hot encoded vector, every element will be a zero EXCEPT for the element that corresponds to the actual category of the given input. 


## Convolutional Neural Networks (CNN)
-  CNN as an artificial neural network that has some type of specialisation for **being able to pick out or detect patterns**. This pattern detection is what makes CNNs so **useful for image analysis**.
- CNN is different from the standard multilayer perceptron or MLP
	- CNNs have hidden layers called **convolutional layers**
- Convolutional Layers
	- Just like any other layer, a convolutional layer receives input, transforms the input in some way, and then outputs the transformed input to the next layer. 
	- The inputs to convolutional layers are called input channels, and the outputs are called output channels.
	- With a convolutional layer, the transformation that occurs is called a convolution operation. 
	- Convolution operations performed by convolutional layers are actually called **cross-correlations**.
- Filters And Convolution Operations
	- Each convolutional layer has a number of filters to detect the patterns.
		- edges
		- shapes
		- textures
		- curves
		- objects
		- colors
	- Simple and geometric filters are found at the start of a convolutional neural network.
	- The deeper the network goes, the more sophisticated the filters become. 
		- In deeper layers, the filters may be able to detect specific objects like eyes.
	- In even deeper layers, the filters are able to detect even more sophisticated objects like full dogs.
	- Filters:
		- **The number of filters determine the number of output channels.**
		- A filter is a relatively small matrix (tensor), for which, we decide the number of rows and columns this matrix has, and the values within this matrix are initialised with random numbers.
		- A convolutional filter is slid across the input channel:
			- For each position on the input channel, the n x n filter does a computation that maps the part of the input channel to the corresponding part of the output channel -> **convolving**
		- When the filter lands on its first n x n block of pixels, the **dot product of the filter itself with the n x n block of pixels from the input will be computed and stored**. This will occur for each n x n block of pixels that the filter convolves.
		- After this filter has convolved the entire input, a new representation of the input is stored in the output channel -> **feature map**
		- The feature map then becomes the input of the next layer, and this process repeats till all the layers are completed.
- The pattern detectors are derived automatically by the network
	- The filter values start out with random values
	- The values change as the network learns during training. 
	- The pattern detecting capability of the filters emerges automatically.


## Zero Padding
- Image dimension are reduced during convolution.
- Given N x N input image & F x F filer, the size of the output is (N-F+1) x (N-F+1) 
- Issue with Reducing Dimensions:
	- Will be a problem is the important part of the input is removed -> lose valuable information by completely removing the information around the edges of the input
	- If input passes through the network and gets convolved by more filters, it will decrease in dimensions significantly -> become meaningless
- Zero Padding:
	- Zero padding is a technique that allows us to preserve the original input size.
	- This is something that we specify on a per-convolutional layer basis. 
	- With each convolutional layer, just as we define how many filters to have and the size of the filters, we can also specify whether or not to use padding.
	- **Zero padding occurs when we add a border of pixels all with value zero around the edges of the input images.**
 	- Maintain original dimensions
		- Sometimes may need to add more than a single pixel thick border, depending on the size of the input and the size of the filters.
- Online API
	- Valid -> No Padding -> Dimensions Reduce
	- Same -> Zero Padding -> Dimensions Stay The Same













