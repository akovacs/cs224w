#finding P(Q,T)

from features import *

import sys
import math
import sanetime

import numpy as np
import pylab
import matplotlib.pyplot as plt
import matplotlib

question_dict = dict()

print 'building question_dict'

for i in questions.index:
	time_in_sec = sanetime.time(questions.ix[i][3]).seconds
	question_dict[questions.ix[i][0]] = time_in_sec
	#add (answerID, time) pair to dictionary for O(1) lookup. 

print 'buildling time_delta'

#populate the deltas (question answered time - question asked time in seconds.)
time_delta = []

for i in answers.index:
	question_t = question_dict[answers.ix[i][1]] #time question was asked.
	answered_t = sanetime.time(answers.ix[i][3]).seconds #time answered.
	delta = answered_t - question_t
	time_delta.append(delta)

def bucketList(time_delta, num_buckets, normalize):
	time_min = 0
	time_max = max(time_delta)

	spread = time_max + 1
	#lower bound is time_min-1 and upper is time_max+1

	bucket_s = spread / num_buckets

	if spread % num_buckets != 0: #last bucket is left out because of int division.
		bucket_s += 1

	num_months = bucket_s / (3600 * 24.0 * 30)

	norm_const = len(time_delta) + num_buckets

	if normalize:
		prob_vec = [1.0 / norm_const for i in range(num_buckets)] #smoothing adding 1/norm_const to each bucket.
		time = [i * num_months for i in range(num_buckets)]

		for delta in time_delta:
			bucket_index = delta / bucket_s
			prob_vec[bucket_index] += 1.0 / norm_const #add fraction of occurences.
		return (prob_vec, time, bucket_s)
	else:
		prob_vec = [1 for i in range(num_buckets)] #smoothing adding 1/norm_const to each bucket.
		time = [i * num_months for i in range(num_buckets)]

		for delta in time_delta:
			bucket_index = delta / bucket_s
			prob_vec[bucket_index] += 1 #add fraction of occurences.
		return (prob_vec, time, bucket_s)

print 'running bucketList'

#we need these to compute P(Q,T) for other questions

(counts, time, bucket_s) = bucketList(time_delta, 1000, False)

log_counts = [math.log(count) for count in counts]

plt.xlabel('Time Since Question Was Asked in Months')
plt.ylabel('Log Count of Answers')

plt.title('Log Count of Answers Recorded After Questions Were Asked')
plt.plot(time, prob_vec, 'r-')

plt.savefig('prob_dist.png')


print prob_vec[0:5]


