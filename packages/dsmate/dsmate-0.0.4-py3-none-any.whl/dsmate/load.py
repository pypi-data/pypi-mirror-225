import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy import stats
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from matplotlib.figure import Figure
from pandas.plotting import scatter_matrix


class dfload:
    def __init__(self):
        self.root =tk.Tk()
        self.root.title("Load")
        self.root.iconbitmap("logo.ico")
        self.root.configure(bg='#121212')
        self.root.geometry('250x250')
        self.root.resizable(False, False)
        self.dataframes = []
        self.file_paths = []
        label1 = tk.Label(self.root, text="UPLOAD OUR CSV AND EXCEL FILES",bg='#121212',fg='#FFFFFF',font=("Arial", 10, "bold"))
        label1.pack(pady=10)
        self.browse_button = tk.Button(self.root, text="BROWSER", command=self.browse_files,bg='#3498db',fg='#000000',font=("Arial", 9, "bold"))
        self.browse_button.pack(pady=30)

        self.convert_button = tk.Button(self.root, text="CONVERT", command=self.convert_files,bg='#3498db',fg='#000000',font=("Arial", 9, "bold"))
        self.convert_button.pack()
        self.root.mainloop()
    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xls;*.xlsx")])
        self.file_paths.extend(file_paths)

    def convert_files(self):
        for file_path in self.file_paths:
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                self.dataframes.append(df)
            except Exception as e:
                print(f"Error converting {file_path}: {e}")
        self.root.destroy()
        return self.dataframes