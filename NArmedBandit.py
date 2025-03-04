import tensorflow as tf
import numpy as np

#List out our bandits.  Currently bandit 4 (index#3) is set to most often
#provide a positive reward.
bandits = [-5, -3, 0, 3, 5]
num_bandits = len(bandits)
def pullBandit(bandit):
	#Get a random number.
	result = np.random.randn(1)
	if result > bandit:
		#return a positive reward.
		return 1
	else:
		#return a negative reward.
		return -1

	tf.reset_default_graph()

#These two lines established the feed-forward part of the network.  This does
#the actual choosing.
weights = tf.Variable(tf.ones([num_bandits]))
chosen_action = tf.argmax(weights, 0)

#The next six lines establish the training proceedure.  We feed the reward and
#chosen action into the network
#to compute the loss, and use it to update the network.
reward_holder = tf.placeholder(shape = [1], dtype = tf.float32)
action_holder = tf.placeholder(shape = [1], dtype = tf.int32) #index of slot machine to choose
responsible_weight = tf.slice(weights, action_holder, [1]) #scalar weight responsible for reward
loss = -(tf.log(responsible_weight) * reward_holder)
optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.001)
update = optimizer.minimize(loss)

total_episodes = 2000 #Set total number of episodes to train agent on.
total_reward = np.zeros(num_bandits) #Set scoreboard for bandits to 0.
choices = np.zeros(num_bandits) #How many times each bandit was chosen
e = 0.1 #Set the chance of taking a random action (exploration rate)

init = tf.global_variables_initializer()

# Launch the tensorflow graph
with tf.Session() as sess:
	sess.run(init)
	for i in range(total_episodes):
		#Choose either a random action or one from our network.
		if np.random.rand(1) < e:
			action = np.random.randint(num_bandits) #Choose random action
		else:
			action = sess.run(chosen_action) #Choose action with highest weight
		
		reward = pullBandit(bandits[action]) #Get our reward from picking one of the bandits.
		
		#Update the network.
		_, old_responsible_weight, adjusted_weights = sess.run([update, responsible_weight,weights], feed_dict = { reward_holder: [reward], action_holder: [action] })
		#print("resp = ", old_weight, "ww = ", adjusted_weights, "choice = ", action)
		#Update our running tally of scores.
		total_reward[action] += reward
		choices[action] += 1
		if i % 100 == 0:
			print ("Running reward for the " + str(num_bandits) + " bandits: " + str(total_reward) + str(choices))
print ("The agent thinks bandit " + str(np.argmax(adjusted_weights) + 1) + " is the most promising....")
if np.argmax(adjusted_weights) == np.argmax(-np.array(bandits)):
	print ("...and it was right!")
else:
	print ("...and it was wrong!")

