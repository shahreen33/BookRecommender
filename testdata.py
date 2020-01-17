from keras.models import load_model
import numpy as np

model = load_model("withGRlinksMoredata.h5")
tempdata = [[1,5]]
data = np.asarray(tempdata)
prediction = model.predict(data)
print(prediction)
