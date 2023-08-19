import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score

class ml_model:
    def __init__(self,X,y,split=0.25,randomness=0,type=0):
        self.master = tk.Tk()
        self.master.geometry('300x300')
        self.master.configure(bg='#121212')
        self.master.resizable(False, False)
        self.master.iconbitmap("logo.ico")
        self.type=type
        self.model=None
        self.X_train,self.X_test,self.y_train,self.y_test=train_test_split(X, y, test_size=split, random_state=randomness)
        self.master.title("ML MODEL BUILDER")
        if self.type==0:
            text='CHOOSE ALGORITHM FOR CLASSIFICATION'
        else:
            text='CHOOSE ALGORITHM FOR REGRESSION'
        self.label_top = tk.Label(self.master, text=text,font=("Arial", 10, "bold"),bg='#121212',fg='#FFFFFF')
        self.label_top.pack(pady=10)
        if self.type==0:
            options = ['Logistic Regression','k-Nearest Neighbors Classification','Support Vector Classification Linear','Support Vector Classification Non-Linear','Decision Trees Classification','Random Forest Classification','Naive Bayes','Ridge Classifier']#classification
        else:
            options = ['Linear Regression','Ridge Regression','Lasso Regression','Elastic Net','k-Nearest Neighbors Regression','Decision Tree Regressor','Random Forest Regressor','Support Vector Regression Linear','Support Vector Regression Non-Linear']#regression
        self.variable = tk.StringVar()
        self.variable.set("")
        self.menu = ttk.Combobox(self.master,width=40,background='gray' ,textvariable=self.variable, values=options)
        self.menu.pack(pady=30)
        self.button = tk.Button(self.master, text="ACCURACY",bg='#3498db',fg='#000000', font=("Arial", 11, "bold"),width=20,height=1,command=self.accuracy_value)
        self.button.pack(pady=10)
        self.accuracy_label = tk.Label(self.master, text="ACCURACY: ",font=("Arial", 11, "bold"),bg='#121212',fg='#FFFFFF')
        self.accuracy_label.pack(pady=20)
        self.give_model = tk.Button(self.master, text="GIVE MODEL",bg='#3498db',fg='#000000', font=("Arial", 11, "bold"),width=15,height=1, command=self.model_selected)
        self.give_model.pack(pady=10)
        self.master.mainloop()
    def model_class(self,value):
        if value=='Random Forest Classification':
            model = RandomForestClassifier()
        elif value=='Support Vector Classification Linear':
            model=svm.SVC(kernel='linear')
        elif value=='Ridge Classifier':
            model = RidgeClassifier()
        elif value=='Support Vector Classification Non-Linear':
            model=svm.SVC(kernel='poly')
        elif value=='Logistic Regression':
            model = LogisticRegression()
        elif value=='k-Nearest Neighbors Classification':
            model = KNeighborsClassifier(n_neighbors=3)
        elif value=='Decision Trees Classification':
            model = DecisionTreeClassifier()
        elif value=='Naive Bayes':
            model = GaussianNB()#classification
        elif value=='Linear Regression':
            model = LinearRegression()
        elif value=='Ridge Regression':
            model = Ridge(alpha=1.0)
        elif value=='Lasso Regression':
            model = Lasso(alpha=0.1)
        elif value=='Elastic Net':
            model = ElasticNet(alpha=0.1, l1_ratio=0.5)
        elif value=='k-Nearest Neighbors Regression':
            model = KNeighborsRegressor(n_neighbors=3)
        elif value=='Decision Tree Regressor':
            model = DecisionTreeRegressor()
        elif value=='Random Forest Regressor':
            model = RandomForestRegressor(n_estimators=100)
        elif value=='Support Vector Regression Linear':
            model = SVR(kernel='linear')
        elif value=='Support Vector Regression Non-Linear':
            model = SVR(kernel='poly')
        model.fit(self.X_train,self.y_train)
        return model
    def model_selected(self):
        value = self.variable.get()
        model=self.model_class(value)
        self.master.destroy()
        return model
    def accuracy_value(self):
        value = self.variable.get()
        model=self.model_class(value)
        if self.type==0:
            accuracy=accuracy_score(self.y_test,model.predict(self.X_test))
        else:
            accuracy=r2_score(self.y_test,model.predict(self.X_test))
        self.accuracy_label.config(text=f"ACCURACY: {accuracy:.2f}")