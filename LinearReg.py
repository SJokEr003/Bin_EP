import Functions
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split

# Read data
data = pd.read_csv("energydata_complete.csv", header=0)
time_list = []
nsm_list = []
# Process date column
for date in data['date']:
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    nsm = int(date.hour) * 3600 + int(date.minute) * 60 + int(date.second) * 1
    date = date.hour
    time_list.append(date)
    nsm_list.append(nsm)

data['hour'] = time_list
data['NSM'] = nsm_list
# Delete useless data
del data['date']
del data['rv1']
del data['rv2']

# Get training set and testing set
x_train, x_test, y_train, y_test = train_test_split(data.iloc[:, 1:], data['Appliances'], random_state=1)

# Run linear regression with all attributes
lr = LinearRegression()
lr.fit(x_train, y_train)

# Evaluate performance
y_train_predict = lr.predict(x_train)
t_mae = Functions.mae(y_train, y_train_predict)
t_rmse = Functions.rmse(y_train, y_train_predict)

y_predict = lr.predict(x_test)
mae = Functions.mae(y_test, y_predict)
rmse = Functions.rmse(y_test, y_predict)
print("Linear Regression")
print('Train:')
print('MAE of all: ', t_mae)
print('RMSE of all: ', t_rmse)
print('Test:')
print('Mae of all: ', mae)
print('RMSE of all: ', rmse)

# Plot graph of test output and predict output
plt.figure(figsize=(20, 8))
ax1 = plt.subplot(111)
plt.plot(range(len(y_predict)), y_predict, 'b', label='predict', linewidth=0.8)
plt.plot(range(len(y_predict)), y_test, 'r', label='test', linewidth=0.5)
plt.legend(loc='upper right')
ax1.set_title('ROC(all variables)')
plt.ylabel('Appliances')
plt.show()
