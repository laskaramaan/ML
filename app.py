# -*- coding: utf-8 -*-
"""car price prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SjXc2dhVGQr7yQf44Z8gaz9losXDesGi
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn import metrics
from flask import Flask, render_template,request



app = Flask(__name__)

@app.route("/" , methods=['GET','POST'])
def index():
    
# date,km,fuel,seller,t_type,owner
    if request.method == "POST":

        a_date = request.form['date']
        Km = request.form['km']
        fuel = request.form['fuel']
        seller = request.form['seller']
        t_type = request.form['t_type']
        owner = request.form['owner']


        print(a_date,Km, fuel,seller,t_type,owner)
        car_dataset= pd.read_csv('static/CAR DETAILS FROM CAR DEKHO.csv')
        car_dataset.head(10)

        car_dataset['selling_price'] = car_dataset['selling_price']/100000

        """Getting the details about the data"""

        car_dataset.shape

        car_dataset.info()

        """checking for the number of missing values"""

        car_dataset.isnull().sum()

        #  Check for the differnt cateogories of the data
        print(car_dataset.fuel.value_counts())
        print(car_dataset.transmission.value_counts())
        print(car_dataset.owner.value_counts())
        print(car_dataset.seller_type.value_counts())

        """

        ---
        <br>
        <h4> Encoding of the cateogorical data :</h4> <br>
        This means that the data is now converted into the numeric value for each part i:e transmission or fuel type into numbers"""

        car_dataset.replace({'fuel':{'Petrol':0,'Diesel':1,'CNG':2,'LPG':3,'Electric':4}},inplace=True)
        car_dataset.replace({'transmission':{'Manual':0,'Automatic':1}},inplace=True)
        car_dataset.replace({'owner':{'First Owner':0,'Second Owner':1,'Third Owner':2,'Fourth & Above Owner':3,'Test Drive Car':4}},inplace=True)
        car_dataset.replace({'seller_type':{'Individual':0,'Dealer':1,'Trustmark Dealer':2}},inplace=True)

        car_dataset.head()

        """Spliting the Dataset into training and target"""

        x = car_dataset.drop(['name','selling_price'],axis=1)
        y = car_dataset['selling_price']

        print(y)

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

        """Model Training
        1. Linear Regression Model
        """

        lin_reg_model = LinearRegression()

        lin_reg_model.fit(x_train, y_train)

        """Model Evvaluation"""

        # Prediction of Training Data
        training_data_prediction = lin_reg_model.predict(x_train)

        # R Square Error
        error_score = metrics.r2_score(y_train, training_data_prediction)
        print("R Square Error: ",error_score)

        """Visualising the Actual prices and the predicted prices"""

        # plt.scatter(y_train, training_data_prediction)
        # plt.xlabel("Actual Prices")
        # plt.ylabel("Predicted Prices")
        # plt.title("Actual Prices VS Predicted Prices")
        # plt.show()

        """### Now Calculate for the Test Data"""

        # Prediction of Testing Data
        testing_data_prediction = lin_reg_model.predict(x_test)

        # R Square error
        error_score = metrics.r2_score(y_test, testing_data_prediction)
        print("R Square Error For Test Data: ",error_score)

        # plt.scatter(y_test, testing_data_prediction)
        # plt.xlabel("Actual Prices")
        # plt.ylabel("Predicted Prices")
        # plt.title("Actual Prices VS Predicted Prices")
        # plt.show()

        """# Now By Lasso Regression"""

        lass_reg_model = Lasso()

        lass_reg_model.fit(x_train, y_train)

        """Model Evvaluation"""

        # Prediction of Training Data
        training_data_prediction = lass_reg_model.predict(x_train)

        # R Square Error
        error_score = metrics.r2_score(y_train, training_data_prediction)
        # print("R Square Error: ",error_score)

        # plt.scatter(y_train, training_data_prediction)
        # plt.xlabel("Actual Prices")
        # plt.ylabel("Predicted Prices")
        # plt.title("Actual Prices VS Predicted Prices")
        # plt.show()

        # Prediction of Testing Data
        testing_data_prediction = lass_reg_model.predict(x_test)

        # R Square error
        error_score = metrics.r2_score(y_test, testing_data_prediction)
        print("R Square Error For Test Data: ",error_score)

        # plt.scatter(y_test, testing_data_prediction)
        # plt.xlabel("Actual Prices")
        # plt.ylabel("Predicted Prices")
        # plt.title("Actual Prices VS Predicted Prices")
        # plt.show()

        """Printing the Output"""

        print(lin_reg_model.coef_)
        print(lin_reg_model.intercept_)

        """# Sample Output

        The Output will be in format of Year, KM Driven, Fuel, Seller Type,  Transmission, Owner
        """

        cost = (lin_reg_model.predict([[a_date,Km,fuel,seller,t_type,owner]]))
        cost = cost*100000

        print(cost[0])
        return render_template('index.html', cost = round(cost[0], 2))
    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)