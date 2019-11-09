import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import optimizers
import numpy as np
import os


fname = str(os.getcwd())+'/'+ "dataset.txt"
with open(fname) as f:
    content = f.readlines()

content = [x.strip() for x in content]

print(content)

train_listx = []
train_listy = []
test_listx = []
test_listy = []
count = 0
for line in content:
	l = line.split(" ")
	xdata = l[0:2] 
	xdata = [float(i) for i in xdata]
	ydata = l[2]
	ydata = [int(i) for i in ydata]
	temp = [0]*5
	temp[ydata[0]-1] = 1
	if(count%3 == 0):
		test_listx.append(xdata)
		test_listy.append(temp)
	else:
		train_listx.append(xdata)
		train_listy.append(temp)
	count +=1


x = np.asarray(train_listx)
y = np.asarray(train_listy)
#x = x[:2700]
#y = y[:2700]
data = np.asarray(test_listx)

#print(y)


model = Sequential()
model.add(Dense(20, input_dim=2, activation='sigmoid'))
model.add(Dense(5, activation = 'softmax'))

sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

model.compile(optimizer= sgd, loss='mse', metrics=['mse'])

weights = model.layers[0].get_weights()
w_init = weights[0][0][0]
b_init = weights[1][0]
print('Linear regression model is initialized with weights w: %.2f, b: %.2f' % (w_init, b_init)) 


model.fit(x,y, batch_size=1, epochs=5, shuffle=False)

weights = model.layers[0].get_weights()
w_final = weights[0][0][0]
b_final = weights[1][0]
print('Linear regression model is trained to have weight w: %.2f, b: %.2f' % (w_final, b_final))

print(x.shape)
print(data.shape)
predict = model.predict(data)
model.save("Initial run")


accurate = 0
closely_accurate = 0
inaccurate = 0

for i in range(len(predict)):
	maxi = 0
	maxidx = -1
	for j in range(5):
		if(predict[i][j] > maxi):
			maxi = predict[i][j]
			maxidx = j
	predicted_rating = maxidx + 1
	maxi = 0
	maxidx = -1
	for j in range(5):
		if(test_listy[i][j] > maxi):
			maxi = y[i][j]
			maxidx = j
	actual_rating = maxidx + 1
	if(predicted_rating == actual_rating):
		accurate +=1
	elif(abs(predicted_rating - actual_rating) == 1):
		closely_accurate += 1
	else:
		inaccurate += 1

total = len(predict)
accuracy = (accurate/total)*100	
print(accurate, (accurate/total)*100)
print(closely_accurate, (closely_accurate/total)*100)
print(inaccurate, (inaccurate/total)*100)

print(((accurate+closely_accurate)/total)*100)

	






