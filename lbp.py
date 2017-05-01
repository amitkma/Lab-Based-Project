import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from nolearn.dbn import DBN
import timeit
import cv2

train = pd.read_csv("train.csv")
features = train.columns[1:]
X = train[features]
y = train['label']
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X/255.,y,test_size=0.1,random_state=0)

clf_rf = RandomForestClassifier()
clf_rf.fit(X_train, y_train)
img = cv2.imread('imagea.png',0)
img = img[len('data:image/png;base64,'):].decode('base64')
img = cv2.imdecode(np.fromstring(img, np.uint8), -1)
img = cv2.resize(img[:,:,3], (28,28))
img = img.astype(np.float32).reshape((1,1,28,28))/255.0
acc_rf = accuracy_score(y_test, y_pred_rf)
print "random forest accur`acy: ",acc_rf
