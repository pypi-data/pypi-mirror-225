import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import messagebox
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from matplotlib.figure import Figure


class dfclean:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.null_counts = dataframe.isnull().sum()
        self.window = tk.Tk()
        self.window.iconbitmap("logo.ico")
        self.window.configure(bg='#121212')
        self.window.geometry('500x500')
        self.window.resizable(False, False)
        
        self.window.title("CLEAN")

        self.tab_control = ttk.Notebook(self.window)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab4 = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab1, text='Null Values')
        self.tab_control.add(self.tab2, text='Categorical Encoding')
        self.tab_control.add(self.tab3, text='Standard Scaling')
        self.tab_control.add(self.tab4, text='Outlier Removal')
        
        self.tab_control.pack(expand=1, fill='both')
        self.style = ttk.Style()
        self.style.theme_create("custom", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "tabmargins": [2, 5, 2, 0],
                    "background": "lightgray"  # Background color of the tab area
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [10, 5],
                    "background": "gray",     # Unselected tab color
                    "font": ("Arial", 8, "bold"),
                },
                "map": {
                    "background": [("selected", '#3498db'),   # Selected tab color
                                   ("!selected", "gray")]
                }
            }
        })
        
        self.style.theme_use("custom")

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        self.setup_tab4()

    def setup_tab1(self):
        tab1_canvas = tk.Canvas(self.tab1)
        tab1_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        tab1_canvas.configure(bg='#121212')
        tab1_scrollbar = ttk.Scrollbar(self.tab1, orient=tk.VERTICAL,command=tab1_canvas.yview)
        tab1_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tab1_canvas.configure(yscrollcommand=tab1_scrollbar.set)
        tab1_canvas.bind('<Configure>', lambda e: tab1_canvas.configure(scrollregion=tab1_canvas.bbox('all')))
        
        tab1_frame = tk.Frame(tab1_canvas)
        tab1_frame.configure(bg='#121212')
        tab1_canvas.create_window((0, 0), window=tab1_frame, anchor='nw')

        label = tk.Label(tab1_frame, text="Total Null Values: {}".format(self.null_counts.sum()),bg='#121212',fg='#FFFFFF',font=("Arial", 10, "bold"))
        label.pack(pady=10)

        process_all_var = tk.StringVar()
        process_all_dropdown = ttk.Combobox(tab1_frame, textvariable=process_all_var, values=["remove", "column mean"])
        process_all_dropdown.pack()
        process_all_button = tk.Button(tab1_frame, text="Process All Null Values", command=lambda: self.process_all_nulls(process_all_var.get()),bg='#3498db',fg='#000000',font=("Arial", 10, "bold"))
        process_all_button.pack(pady=20)

        null_columns = self.null_counts[self.null_counts > 0]
        for column, count in null_columns.items():
            frame = tk.Frame(tab1_frame)
            frame.pack()
            frame.configure(bg='#121212')
            label = tk.Label(frame, text="Column: {} ({} null values)".format(column, count),bg='#121212',fg='#FFFFFF',font=("Arial", 10, "bold"))
            label.pack(side=tk.LEFT,pady=10)
            action_var = tk.StringVar()
            action_dropdown = ttk.Combobox(frame, textvariable=action_var, values=["remove", "column mean"])
            action_dropdown.pack(side=tk.LEFT,padx=20)
            button = tk.Button(frame,bg='#3498db',fg='#000000', text="APPLY", font=("Arial", 10, "bold"), command=lambda col=column,action=action_var: self.handle_null_action(col, action.get()))
            button.pack(side=tk.LEFT,padx=20)

    def process_all_nulls(self, action):
        if action == "remove":
            self.dataframe = self.dataframe.dropna()
        elif action == "column mean":
            self.dataframe = self.dataframe.fillna(self.dataframe.mean())
        self.update_tab1()

    def handle_null_action(self, column, action):
        if action == "remove":
            self.dataframe = self.dataframe.dropna(subset=[column])
            self.update_tab1()
        elif action == "column mean":
            column_mean = self.dataframe[column].mean()
            self.dataframe[column].fillna(column_mean, inplace=True)
            self.update_tab1()

    def update_tab1(self):
        self.null_counts = self.dataframe.isnull().sum()
        self.tab_control.forget(self.tab1)
        self.tab1.destroy()
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.insert(0, self.tab1)
        self.setup_tab1()

    def setup_tab2(self):
        tab2_canvas = tk.Canvas(self.tab2)
        tab2_canvas.configure(bg='#121212')
        tab2_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        tab2_scrollbar = ttk.Scrollbar(self.tab2, orient=tk.VERTICAL, command=tab2_canvas.yview)
        tab2_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tab2_canvas.configure(yscrollcommand=tab2_scrollbar.set)
        tab2_canvas.bind('<Configure>', lambda e: tab2_canvas.configure(scrollregion=tab2_canvas.bbox('all')))
        
        self.tab2_frame = tk.Frame(tab2_canvas)
        self.tab2_frame.configure(bg='#121212')
        tab2_canvas.create_window((0, 0), window=self.tab2_frame, anchor='nw')

        self.categorical_vars = {}
        categorical_columns = [col for col in self.dataframe.columns if self.dataframe[col].dtype == 'object']
        for column in categorical_columns:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.tab2_frame, text=column, variable=var,background='#121212',font=("Arial", 11, "bold"),highlightthickness=3,foreground='#3498db')
            checkbox.pack(anchor='w',pady=10)
            self.categorical_vars[column] = var

        apply_button = tk.Button(self.tab2, text="APPLY CHANGES",bg='#3498db',font=("Arial", 8, "bold"),fg='#000000', command=self.apply_categorical_encoding)
        apply_button.pack(pady=20)

        apply_all_button = tk.Button(self.tab2, text="APPLY All",bg='#3498db',font=("Arial", 8, "bold"),fg='#000000', command=self.apply_all_categorical)
        apply_all_button.pack()

    def setup_tab3(self):
        tab3_canvas = tk.Canvas(self.tab3)
        tab3_canvas.configure(bg='#121212')
        tab3_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        tab3_scrollbar = ttk.Scrollbar(self.tab3, orient=tk.VERTICAL, command=tab3_canvas.yview)
        tab3_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tab3_canvas.configure(yscrollcommand=tab3_scrollbar.set)
        tab3_canvas.bind('<Configure>', lambda e: tab3_canvas.configure(scrollregion=tab3_canvas.bbox('all')))
        
        self.tab3_frame = tk.Frame(tab3_canvas)
        self.tab3_frame.configure(bg='#121212')
        tab3_canvas.create_window((0, 0), window=self.tab3_frame, anchor='nw')

        self.scaling_vars = {}
        numeric_columns = [col for col in self.dataframe.columns if pd.api.types.is_numeric_dtype(self.dataframe[col])]
        for column in numeric_columns:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.tab3_frame, text=column, variable=var,background='#121212',font=("Arial", 11, "bold"),highlightthickness=3,foreground='#3498db')
            checkbox.pack(anchor='w',pady=10)
            self.scaling_vars[column] = var

        apply_button = tk.Button(self.tab3,text="APPLY CHANGES",bg='#3498db',font=("Arial", 8, "bold"),fg='#000000', command=self.apply_standard_scaling)
        apply_button.pack(pady=20)

        apply_all_button = tk.Button(self.tab3,  text="APPLY All",bg='#3498db',font=("Arial", 8, "bold"),fg='#000000', command=self.apply_all_scaling)
        apply_all_button.pack()

    def setup_tab4(self):
        tab4_canvas = tk.Canvas(self.tab4)
        tab4_canvas.configure(bg='#121212')
        tab4_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        tab4_scrollbar = ttk.Scrollbar(self.tab4, orient=tk.VERTICAL, command=tab4_canvas.yview)
        tab4_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tab4_canvas.configure(yscrollcommand=tab4_scrollbar.set)
        tab4_canvas.bind('<Configure>', lambda e: tab4_canvas.configure(scrollregion=tab4_canvas.bbox('all')))
        
        tab4_frame = tk.Frame(tab4_canvas)
        tab4_frame.configure(bg='#121212')
        tab4_canvas.create_window((0, 0), window=tab4_frame, anchor='nw')

        self.outlier_label = tk.Label(tab4_frame, text="Number of Outliers: ",bg='#121212',font=("Arial", 11, "bold"),fg='#FFFFFF')
        self.outlier_label.pack(padx=180,pady=80)

        remove_outliers_button = tk.Button(tab4_frame, text="Remove Outliers",bg='#3498db',font=("Arial", 10, "bold"),fg='#000000', command=self.remove_outliers_iqr)
        remove_outliers_button.pack(padx=180)
        
    def remove_outliers_iqr(self):
        Q1 = self.dataframe.quantile(0.25)
        Q3 = self.dataframe.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        self.dataframe = self.dataframe[~((self.dataframe < lower_bound) | (self.dataframe > upper_bound)).any(axis=1)]

        self.update_tab4()

    def update_tab4(self):
        self.outlier_label.config(text="Number of Outliers: {}".format(len(self.dataframe)))

    def apply_all_categorical(self):
        for var in self.categorical_vars.values():
            var.set(1)
        self.apply_categorical_encoding()

    def apply_all_scaling(self):
        for var in self.scaling_vars.values():
            var.set(1)
        self.apply_standard_scaling()

    def apply_categorical_encoding(self):
        for column, var in self.categorical_vars.items():
            if var.get() == 1:
                le = LabelEncoder()
                self.dataframe[column]=le.fit_transform(self.dataframe[column])

    def apply_standard_scaling(self):
        scaler = StandardScaler()
        for column, var in self.scaling_vars.items():
            if var.get() == 1:
                self.dataframe[column] = scaler.fit_transform(self.dataframe[[column]])

    def get_resultant_dataframe(self):
        return self.dataframe

    def clean(self):
        close_button = tk.Button(self.window,bg='#3498db',fg='#000000', text="PROCESS", font=("Arial", 10, "bold") ,width=30,command=self.window.destroy)
        close_button.pack(pady=10)
        self.window.mainloop()
        return self.get_resultant_dataframe()

class dfsum:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.columns = list(dataframe.columns)
        
        self.root = tk.Tk()
        self.root.title("SUMMARY")
        self.root.geometry("700x700")
        self.root.configure(bg='#121212')
        self.root.resizable(False, False)
        self.root.iconbitmap("logo.ico")
        
        self.column_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE,background='#121212',fg='#FFFFFF',font=("Arial", 11, "bold"))
        self.column_listbox.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        
        for column in self.columns:
            self.column_listbox.insert(tk.END, column)
        
        self.analysis_frame = tk.Frame(self.root)
        self.analysis_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.scrollable_canvas = tk.Canvas(self.analysis_frame)
        self.scrollable_canvas.configure(bg='#121212')
        self.scrollable_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollable_scrollbar = tk.Scrollbar(self.analysis_frame, orient=tk.VERTICAL, command=self.scrollable_canvas.yview)
        self.scrollable_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scrollable_canvas.configure(yscrollcommand=self.scrollable_scrollbar.set)
        self.scrollable_canvas.bind('<Configure>', lambda e: self.scrollable_canvas.configure(scrollregion=self.scrollable_canvas.bbox("all")))
        
        self.scrollable_frame_content = tk.Frame(self.scrollable_canvas)
        self.scrollable_frame_content.configure(bg='#121212')
        self.scrollable_canvas.create_window((0, 0), window=self.scrollable_frame_content, anchor=tk.NW)
        
        self.scrollable_frame_content.bind("<Configure>", self.on_frame_configure)
        
        self.plot_button = tk.Button(self.root, text="ANALYZE",bg='#3498db',fg='#000000',font=("Arial", 11, "bold"),width=20,height=2, command=self.analyze)
        self.plot_button.pack(padx=10, pady=10)
        
        self.root.mainloop()
        
    def on_frame_configure(self, event):
        self.scrollable_canvas.configure(scrollregion=self.scrollable_canvas.bbox("all"))
        
    def analyze(self):
        selected_columns = [self.columns[i] for i in self.column_listbox.curselection()]
        
        for widget in self.scrollable_frame_content.winfo_children():
            widget.destroy()
        
        if not selected_columns:
            return
        
        for column in selected_columns:
            column_frame = tk.Frame(self.scrollable_frame_content, relief=tk.RAISED)
            column_frame.configure(bg='#3498db')
            column_frame.pack(padx=5, pady=5, fill=tk.X)
            
            label = tk.Label(column_frame, text=f"Column: {column}",bg='#3498db',fg='#000000',font=("Arial", 11, "bold"))
            label.pack(anchor=tk.W, padx=5, pady=5)
            
            column_data = self.dataframe[column]
            mean_label = tk.Label(column_frame, text=f"Mean: {column_data.mean():.2f}",bg='#3498db',fg='#000000',font=("Arial", 11, "bold"))
            mean_label.pack(anchor=tk.W, padx=5)
            
            median_label = tk.Label(column_frame, text=f"Median: {column_data.median():.2f}",bg='#3498db',fg='#000000',font=("Arial", 11, "bold"))
            median_label.pack(anchor=tk.W, padx=5)
            
            std_label = tk.Label(column_frame, text=f"Standard Deviation: {column_data.std():.2f}",bg='#3498db',fg='#000000',font=("Arial", 11, "bold"))
            std_label.pack(anchor=tk.W, padx=5)
            unique_label = tk.Label(column_frame, text=f"Unique Values: {column_data.nunique()}",bg='#3498db',fg='#000000',font=("Arial", 11, "bold"))
            unique_label.pack(anchor=tk.W, padx=5)
            
        if len(selected_columns) > 1:
            correlation_frame = tk.Frame(self.scrollable_frame_content, relief=tk.RAISED, borderwidth=1)
            correlation_frame.configure(bg='#121212')
            correlation_frame.pack(padx=5, pady=5, fill=tk.X)
            
            correlation_label = tk.Label(correlation_frame, text="Correlation Matrix", font=("Arial", 13, "bold"),bg='#121212',fg='#FFFFFF')
            correlation_label.pack(anchor=tk.W, padx=5, pady=5)
            
            selected_data = self.dataframe[selected_columns]
            corr_matrix = selected_data.corr()
            self.plot_correlation_matrix(corr_matrix, correlation_frame)
            
    def plot_correlation_matrix(self, corr_matrix, parent_frame):
        figure = plt.Figure(figsize=(6, 4))
        ax = figure.add_subplot(111)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title("Correlation Matrix")
        
        canvas = FigureCanvasTkAgg(figure, parent_frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()

class dfviz:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.columns = list(dataframe.columns)
        
        self.root = tk.Tk()
        self.root.title("DataFrame Visualizer")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#121212')
        self.root.iconbitmap("logo.ico")
        
        self.column_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE,background='#121212',foreground='#3498db',font=("Arial", 11, "bold"))
        self.column_listbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        
        for column in self.columns:
            self.column_listbox.insert(tk.END, column)
        
        self.graph_options = ["Scatter Plot", "Histogram", "Bar Graph", "Correlation Matrix"]
        self.graph_dropdown = ttk.Combobox(self.root, values=self.graph_options)
        self.graph_dropdown.pack(padx=10, pady=5)
        
        self.plot_button = tk.Button(self.root, text="PLOT", command=self.plot,bg='#3498db',fg='#000000',font=("Arial", 10, "bold"),width=20)
        self.plot_button.pack(padx=10, pady=5)
        
        self.clear_button = tk.Button(self.root, text="CLEAR", command=self.clear_plot,bg='#3498db',fg='#000000',font=("Arial", 10, "bold"),width=20)
        self.clear_button.pack(padx=10, pady=5)
        
        self.figure = Figure(figsize=(6, 4))
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.root.mainloop()
        
    def plot(self):
        selected_columns = [self.columns[i] for i in self.column_listbox.curselection()]
        graph_type = self.graph_dropdown.get()
        
        if not selected_columns:
            messagebox.showwarning("No Columns Selected", "Please select at least one column.")
            return
        
        self.figure.clear()
        
        if graph_type == "Scatter Plot":
            ax = self.figure.add_subplot(111)
            self.dataframe.plot.scatter(x=selected_columns[0], y=selected_columns[1], ax=ax)
            ax.set_title("Scatter Plot")
            self.canvas.draw()
            
        elif graph_type == "Histogram":
            self.dataframe[selected_columns].hist(ax=self.figure.gca())
            self.figure.suptitle("Histogram")
            self.canvas.draw()
            
        elif graph_type == "Bar Graph":
            self.dataframe[selected_columns].plot(kind='bar', ax=self.figure.gca())
            self.figure.suptitle("Bar Graph")
            self.canvas.draw()
            
        elif graph_type == "Correlation Matrix":
            self.figure.clear()
            selected_data = self.dataframe[selected_columns]
            corr_matrix = selected_data.corr()
            ax = self.figure.add_subplot(111)
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
            ax.set_title("Correlation Matrix")
            self.canvas.draw()
            
    def clear_plot(self):
        self.figure.clear()
        self.canvas.draw()