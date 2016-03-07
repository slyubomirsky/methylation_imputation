import math
import numpy as np 
from sklearn.externals.six import StringIO
#import pydot
import pandas
import os

print('dataset={')

last_row = -1

def write_to_file(row, col, val, last_row):
	if(row != last_row):
		if(last_row != -1):
			print('},')
		print('\'' + str(row) + '\': {')
		last_row = row
	print('\'' + str(col) + '\': ' + str(val) + ',\n')
	return last_row;


# read_csv() function needs the parameter sep to tell it what your separator is
train_bed = pandas.read_csv('/Users/Valerie/Documents/School/Junior/COS 424/HW2/data/intersected_final_chr1_cutoff_20_train.bed', sep='\t', header=None)
sample_p_bed = pandas.read_csv('/Users/Valerie/Documents/School/Junior/COS 424/HW2/data/intersected_final_chr1_cutoff_20_sample_partial.bed', sep='\t', header=None)
sample_f_bed = pandas.read_csv('/Users/Valerie/Documents/School/Junior/COS 424/HW2/data/intersected_final_chr1_cutoff_20_sample_full.bed', sep='\t', header=None)


# You can refer to each *column* of the datatable by index:
test_indeces = sample_p_bed[5]==1
train_indeces = sample_p_bed[5]==0
#print(sum(test_indeces))
#print(np.where(test_indeces))

# Let's take indices of the sample file that aren't nans for comparison:
# By the way, learning the python list comprehension construction is totally worth it.
# Check out http://www.secnetix.de/olli/Python/list_comprehensions.hawk if the following code confuses you.

not_nans_in_full = ~np.isnan(sample_f_bed[4])
test_indeces_nan_filtered = [test_indeces[x] and not_nans_in_full[x] for x in range(len(test_indeces))]

#print(sum(test_indeces_nan_filtered))

train_indeces_nan_filtered = [train_indeces[x] and not_nans_in_full[x] for x in range(len(train_indeces))]

#print(sum(train_indeces_nan_filtered))

# Python list comprehension keeps coming up...
test_indeces_nan_filtered_numeric = np.where(test_indeces_nan_filtered)[0]

partial_values_test = [sample_f_bed[4][x] for x in test_indeces_nan_filtered_numeric]

# http://stackoverflow.com/questions/17197492/root-mean-square-error-in-python
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

train_indeces_nan_filtered_numeric = np.where(train_indeces_nan_filtered)[0]

full_values_test = [sample_f_bed[4][x] for x in train_indeces_nan_filtered_numeric]

# we have partial_values_test defined from above:

for i in range(4,37):
    test_array = [train_bed[i][x] for x in test_indeces_nan_filtered_numeric]
    test_array_mod = [test_array[x] for x in range(len(test_array)) if ~np.isnan(test_array[x])]
    temp_partial_values_test = [partial_values_test[x] for x in range(len(partial_values_test)) if ~np.isnan(test_array[x])]
    for j in range(0,len(test_array_mod)):
    	last_row = write_to_file(i, j, test_array_mod[j], last_row)
    #for j in range(0,len(temp_partial_values_test)):
        #last_row = write_to_file(i, j, temp_partial_values_test[j], last_row)
    #print("Sample " + str(i) + " has r = ")
    #print(np.corrcoef(test_array_mod, temp_partial_values_test)[0,1])

samp_23_test = [train_bed[23][x] for x in train_indeces_nan_filtered_numeric]
full_values_test = [sample_f_bed[4][x] for x in train_indeces_nan_filtered_numeric]

# Need to take out nans. However, in the real assignment, you must fill in the nans with some value for full imputation:
samp_23_test_mod = [samp_23_test[x] for x in range(len(samp_23_test)) if ~np.isnan(samp_23_test[x])]
full_values_test_mod = [full_values_test[x] for x in range(len(samp_23_test)) if ~np.isnan(samp_23_test[x])]

#print(np.corrcoef(samp_23_test_mod, full_values_test_mod))
#print(rmse(np.array(samp_23_test_mod), np.array(full_values_test_mod)))


print('}\n}')

