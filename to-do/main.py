import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


"""
    TaskFlow: A To-do app for desktop
    A beginner friendly project to learn tkinter framework, database management and analysis of data

    Skills:
    1. tkinter: framework for GUIs
    2. sqlite3: database management
    3. matplotlib: data charts
    4. pandas: data analysis
    5. OOP
    6. Event handling

    Date: 28-04-26
    Created for learning
"""

class Database:
    """
    Database class to manage all database operations
    """

    def __init__(self,db_name='taskd.db'):
        self.dbName = db_name
        self.createTable()
    
    def createTable(self):
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXIST tasks (
                    id INTEGER PRIMARY KEY AUTO INCREMENT,
                    name TEXT NOT NULL,
                    decription TEXT,
                    due_date DATETIME,
                    priority TEXT DEAFULT 'Medium',
                    completed INTEGER DEFAULT 0,
                    created_at TEXT,
                    completed_at TEXT)
                    ''')
        
        conn.commit()
        conn.close()

    def addTasks(self,name,decription='',due_date='',priority='Medium'):
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()

        created_at = datetime.now().isoformat()
        cur.execute('''INSERT INTO tasks
                    (name,descriptiob,due_date,priority,created_at)
                    values (?,?,?,?,?)
                    ''',
                    (name,decription,due_date,priority,created_at))
            
        conn.commit()
        conn.close()

    def getTasks(self):
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()

        cur.execute('''SELECT id,name,description,dur_date,priority,completed
                    FROM tasks
                    ORDER BY completed ASC,created_at DESC
                    ''')
            
        tasks = cur.fetchall()

        conn.commit()
        conn.close()

        return tasks
    
    def deleteTasks(self,id):
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()

        cur.execute('''DELETE FROM tasks WHERE id=?
                    ''',(id,))
            
        conn.commit()
        conn.close()
    
    def markComplete(self,id):
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()

        completed_at = datetime.now().isoformat()
        cur.execute('''UPDATE tasks
                    SET completed=1,completed_at=?
                    WHERE id=?
                    ''',(id,completed_at)
                    )
            
        conn.commit()
        conn.close()

    def markIncomplete(self,id):
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()

        cur.execute('''UPDATE tasks
                    SET completed=0,completed_at=NULL
                    WHERE id=?
                    ''',(id,)
                    )
            
        conn.commit()
        conn.close()

    def getDataForAnalytics(self):
        conn = sqlite3.connect(self.dbName)

        df = pd.read_sql_query('SELECT * FROM tasks',
                               conn,
                               parse_dates=['created_at','completed_at','due_date']
                               )
        
        conn.close()

        return df

