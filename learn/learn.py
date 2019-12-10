import numpy as np
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = np.loadtxt('dataset.csv', delimiter=',', dtype=int)

train_data, test_data, train_label, test_label = train_test_split(data[:, 1:], data[:, 0])

clf = SVC(C=1, gamma=0.001)
clf.fit(train_data, train_label)

print("訓練セット：{}".format(clf.score(train_data, train_label)))
print("テストセット：{}".format(clf.score(test_data, test_label)))
