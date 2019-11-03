import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np

with open("data.txt") as f:
    content = f.readlines()

content = [x.strip() for x in content]

newlist1 = []
newlist2 = []

for line in content:
	l = line.split(" ")
	xdata = l[0:2] 
	xdata = [float(i) for i in xdata]
	ydata = l[2]
	ydata = [int(i) for i in ydata]
	temp = [0]*5
	temp[ydata[0]-1] = 1
	newlist1.append(xdata)
	newlist2.append(temp)


x = np.asarray(newlist1)
y = np.asarray(newlist2)
data = np.asarray([[50.222,0.99],[70.22, 0.4]])

print(y)




model = Sequential()
model.add(Dense(20, input_dim=2, activation='sigmoid'))
model.add(Dense(5, activation = 'softmax'))


model.compile(optimizer='sgd', loss='mse', metrics=['mse'])

weights = model.layers[0].get_weights()
w_init = weights[0][0][0]
b_init = weights[1][0]
print('Linear regression model is initialized with weights w: %.2f, b: %.2f' % (w_init, b_init)) 


model.fit(x,y, batch_size=1, epochs=10, shuffle=False)

weights = model.layers[0].get_weights()
w_final = weights[0][0][0]
b_final = weights[1][0]
print('Linear regression model is trained to have weight w: %.2f, b: %.2f' % (w_final, b_final))

print(x.shape)
print(data.shape)
predict = model.predict(data)
print(predict)



