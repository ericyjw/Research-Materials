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