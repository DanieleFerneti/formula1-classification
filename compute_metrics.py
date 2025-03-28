import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, required=True)
parser.add_argument('--name', type=str, required=True)
args = parser.parse_args()

def true_positive(df, label = 0):
	return df[label][label]


def false_positive(df,label = 0):
	fp = 0
	for i in range(15):
		if(i != label):
			fp = fp + (df[label][i])
	return fp

def false_negative(df,label = 0):
	fn = 0
	for i in range(15):
		if(i != label):
			fn = fn + (df[i][label])
	return fn


def compute_precision(df, label = 0):
	precision = 0
	try:
		tp = true_positive(df,label)
		fp = false_positive(df,label)

		return tp/(tp+fp)
	except:
		precision = 0	
	return precision


def compute_recall(df, label = 0):
	recall = 0
	try:
		tp = true_positive(df,label)
		fn = false_negative(df,label)

		return tp/(tp+fn)
	except:
		recall = 0	
	return recall


def compute_f1(precision, recall):
	f1 = 0
	try:
		return 2*((precision*recall)/(precision+recall))
	except:
		f1 = 0	
	return f1


row_data = pd.read_csv(args.data, header=None).values[0]

# Reshape the row data into a 15x15 matrix
# Confusion matrix in input is a one row shape 
# reshape to nxn, where n is number of my classes
confusion_matrix = row_data.reshape(15, 15)

# Convert to a DataFrame for better readability
confusion_df = pd.DataFrame(confusion_matrix)

# Show the reshaped confusion matrix
print('input confusion matrix ========================\n')
print(confusion_df)
print(f'total: {confusion_df.sum().sum()}')
print('\n==============================================\n')

sectors = ['ascari-due', 'ascari-uno', 'biassono', 'lesmo-due', 'lesmo-uno', 'neutro-cinque', 'neutro-due', 'neutro-quattro', 'neutro-sei', 'neutro-tre', 'neutro-uno', 'neutro-zero', 'parabolica', 'prima-variante', 'seconda-variante']
precision = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
recall = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
f1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# Compute precision, recall and f1 for all classes
i = 0
for i in range(15):
	precision[i] = compute_precision(confusion_df, i)
	recall[i] = compute_recall(confusion_df, i)
	f1[i] = compute_f1(precision[i], recall[i])


# Compute macro precision, recall and f1
macro_precision = 0
macro_recall = 0
i = 0
for i in range(15):
	macro_precision += precision[i]
	macro_recall += recall[i]

macro_precision = macro_precision/15	
macro_recall = macro_recall/15
macro_f1 = compute_f1(macro_precision, macro_recall)

print(f'precision: {precision}')
print(f'recall: {recall}')
print(f'f1: {f1}')
print('+++++++++++++++++++++++++++++++++++++')
print(f'macro-precision: {macro_precision}')
print(f'macro-recall: {macro_recall}')
print(f'macro-f1: {macro_f1}')

with open(f"metrics-{args.name}.txt", 'a') as file:
	file.write(f'Metrics for {args.name}\n\n')
	for i in range(15):
		file.write(f'[{sectors[i]}] -- precision: {precision[i]} , recall: {recall[i]}, f1: {f1[i]}\n')
	file.write(f'macro-precision: {macro_precision}\n')
	file.write(f'macro-recall: {macro_recall}\n')
	file.write(f'macro-f1: {macro_f1}\n')



