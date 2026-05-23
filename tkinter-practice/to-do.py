"""
TaskFlow - Simple Todo App for Desktop
A beginner-friendly project to learn Python

This app teaches you:
- Tkinter (GUI - Graphical User Interface)
- SQLite3 (Database)
- Matplotlib (Charts)
- Pandas (Data Analysis)
- OOP (Classes and Objects)
- Event Handling (Button clicks)

Author: Created for Learning
Date: 2024
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# ============================================
# PART 1: DATABASE SETUP
# ============================================

class Database:
    """
    Manages all database operations.
    
    Why a class?
    - Keeps all database code organized
    - Easier to modify later
    - Can create multiple databases if needed
    """
    
    def __init__(self, db_name='tasks.db'):
        """Initialize database"""
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """Create tasks table if it doesn't exist"""
        # Connect to database (creates file if doesn't exist)
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Create table - like an Excel spreadsheet
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT DEFAULT 'Medium',
            completed INTEGER DEFAULT 0,
            created_at TEXT,
            completed_at TEXT
        )''')
        
        conn.commit()
        conn.close()
    
    def add_task(self, name, description='', due_date='', priority='Medium'):
        """Add a new task to database"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        created_at = datetime.now().isoformat()
        
        c.execute('''INSERT INTO tasks 
                    (name, description, due_date, priority, created_at)
                    VALUES (?, ?, ?, ?, ?)''',
                 (name, description, due_date, priority, created_at))
        
        conn.commit()
        conn.close()
    
    def get_all_tasks(self):
        """Get all tasks from database"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''SELECT id, name, description, due_date, priority, completed 
                    FROM tasks 
                    ORDER BY completed ASC, created_at DESC''')
        
        tasks = c.fetchall()
        conn.close()
        
        return tasks
    
    def mark_complete(self, task_id):
        """Mark a task as complete"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        completed_at = datetime.now().isoformat()
        
        c.execute('''UPDATE tasks 
                    SET completed = 1, completed_at = ?
                    WHERE id = ?''',
                 (completed_at, task_id))
        
        conn.commit()
        conn.close()
    
    def mark_incomplete(self, task_id):
        """Mark a task as incomplete"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''UPDATE tasks 
                    SET completed = 0, completed_at = NULL
                    WHERE id = ?''',
                 (task_id,))
        
        conn.commit()
        conn.close()
    
    def delete_task(self, task_id):
        """Delete a task"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        
        conn.commit()
        conn.close()
    
    def get_analytics_data(self):
        """Get data for analytics - returns a pandas DataFrame"""
        conn = sqlite3.connect(self.db_name)
        
        # Read all tasks into a pandas DataFrame
        df = pd.read_sql_query(
            'SELECT * FROM tasks',
            conn,
            parse_dates=['created_at', 'completed_at', 'due_date']
        )
        
        conn.close()
        
        return df

# ============================================
# PART 2: ANALYTICS CLASS
# ============================================

class Analytics:
    """
    Analyzes task data and creates charts.
    
    This is where you learn:
    - Pandas data manipulation
    - Creating matplotlib charts
    - Data analysis
    """
    
    def __init__(self, df):
        """Initialize with pandas DataFrame"""
        self.df = df
    
    def get_summary_stats(self):
        """Get summary statistics"""
        if len(self.df) == 0:
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'completion_rate': 0
            }
        
        total = len(self.df)
        completed = len(self.df[self.df['completed'] == 1])
        pending = total - completed
        rate = (completed / total * 100) if total > 0 else 0
        
        return {
            'total_tasks': total,
            'completed_tasks': completed,
            'pending_tasks': pending,
            'completion_rate': round(rate, 1)
        }
    
    def get_by_priority(self):
        """Get task count by priority"""
        if len(self.df) == 0:
            return {}
        
        # Count tasks by priority
        counts = self.df['priority'].value_counts().to_dict()
        return counts
    
    def create_summary_chart(self, parent):
        """Create a pie chart of completed vs pending tasks"""
        if len(self.df) == 0:
            return None
        
        # Count completed and pending
        completed = len(self.df[self.df['completed'] == 1])
        pending = len(self.df[self.df['completed'] == 0])
        
        # Create figure (chart)
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Create pie chart
        labels = ['Completed', 'Pending']
        sizes = [completed, pending]
        colors = ['#51cf66', '#ffd93d']
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Task Completion Status', fontsize=14, fontweight='bold')
        
        return fig
    
    def create_priority_chart(self, parent):
        """Create a bar chart of tasks by priority"""
        if len(self.df) == 0:
            return None
        
        priority_counts = self.df['priority'].value_counts()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        priority_counts.plot(kind='bar', ax=ax, color=['#667eea', '#764ba2', '#f39c12'])
        ax.set_title('Tasks by Priority', fontsize=14, fontweight='bold')
        ax.set_xlabel('Priority')
        ax.set_ylabel('Count')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        
        return fig

# ============================================
# PART 3: MAIN APPLICATION CLASS
# ============================================

class TaskFlowApp:
    """
    Main application class.
    
    This controls:
    - The window (Tkinter)
    - All buttons and widgets
    - Updating the display
    - Handling user actions
    """
    
    def __init__(self, root):
        """Initialize the app"""
        self.root = root
        self.root.title("TaskFlow - Todo App")
        self.root.geometry("700x600")
        
        # Initialize database
        self.db = Database()
        
        # Create the UI
        self.create_ui()
        
        # Load initial data
        self.refresh_tasks()
    
    def create_ui(self):
        """Create all UI elements (buttons, text boxes, etc.)"""
        
        # ===== HEADER =====
        header_frame = tk.Frame(self.root, bg='#667eea', height=60)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame,
            text="📋 TaskFlow - Todo App",
            font=("Arial", 18, "bold"),
            bg='#667eea',
            fg='white'
        )
        header_label.pack(pady=10)
        
        # ===== TAB BUTTONS =====
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.tasks_tab_btn = tk.Button(
            button_frame,
            text="📋 My Tasks",
            command=self.show_tasks_tab,
            font=("Arial", 11),
            padx=20,
            bg='#667eea',
            fg='white'
        )
        self.tasks_tab_btn.pack(side=tk.LEFT, padx=5)
        
        analytics_tab_btn = tk.Button(
            button_frame,
            text="📊 Analytics",
            command=self.show_analytics_tab,
            font=("Arial", 11),
            padx=20
        )
        analytics_tab_btn.pack(side=tk.LEFT, padx=5)
        
        # ===== MAIN CONTENT AREA =====
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_tasks_tab()
        self.create_analytics_tab()
        
        # Show tasks tab by default
        self.show_tasks_tab()
    
    def create_tasks_tab(self):
        """Create the tasks management tab"""
        self.tasks_frame = tk.Frame(self.content_frame)
        
        # ===== ADD TASK SECTION =====
        add_task_label = tk.Label(
            self.tasks_frame,
            text="Add New Task",
            font=("Arial", 12, "bold")
        )
        add_task_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.tasks_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="Task Name:").pack(side=tk.LEFT, padx=5)
        self.task_name_input = tk.Entry(input_frame, width=40)
        self.task_name_input.pack(side=tk.LEFT, padx=5)
        
        # Description frame
        desc_frame = tk.Frame(self.tasks_frame)
        desc_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(desc_frame, text="Description:").pack(side=tk.LEFT, padx=5)
        self.task_desc_input = tk.Entry(desc_frame, width=40)
        self.task_desc_input.pack(side=tk.LEFT, padx=5)
        
        # Priority frame
        priority_frame = tk.Frame(self.tasks_frame)
        priority_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(priority_frame, text="Priority:").pack(side=tk.LEFT, padx=5)
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(
            priority_frame,
            textvariable=self.priority_var,
            values=["Low", "Medium", "High"],
            width=10,
            state="readonly"
        )
        priority_combo.pack(side=tk.LEFT, padx=5)
        
        # Add button
        add_btn = tk.Button(
            self.tasks_frame,
            text="+ Add Task",
            command=self.add_task,
            bg='#51cf66',
            fg='white',
            font=("Arial", 10, "bold")
        )
        add_btn.pack(pady=10)
        
        # ===== TASK LIST SECTION =====
        tasks_label = tk.Label(
            self.tasks_frame,
            text="Your Tasks",
            font=("Arial", 12, "bold")
        )
        tasks_label.pack(pady=10)
        
        # Scrollable task list
        scroll_frame = tk.Frame(self.tasks_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_list = tk.Listbox(
            scroll_frame,
            yscrollcommand=scrollbar.set,
            height=15,
            font=("Arial", 10)
        )
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_list.yview)
        
        # ===== BUTTONS FOR TASK ACTIONS =====
        action_frame = tk.Frame(self.tasks_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        complete_btn = tk.Button(
            action_frame,
            text="✓ Mark Complete",
            command=self.mark_task_complete,
            bg='#667eea',
            fg='white'
        )
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(
            action_frame,
            text="🗑 Delete",
            command=self.delete_task,
            bg='#ff6b6b',
            fg='white'
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
    
    def create_analytics_tab(self):
        """Create the analytics tab"""
        self.analytics_frame = tk.Frame(self.content_frame)
        
        # ===== SUMMARY STATS =====
        stats_label = tk.Label(
            self.analytics_frame,
            text="Summary Statistics",
            font=("Arial", 12, "bold")
        )
        stats_label.pack(pady=10)
        
        self.stats_text = tk.Label(
            self.analytics_frame,
            text="",
            font=("Arial", 10),
            justify=tk.LEFT
        )
        self.stats_text.pack(pady=10)
        
        # ===== CHARTS =====
        self.chart_frame = tk.Frame(self.analytics_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            self.analytics_frame,
            text="🔄 Refresh Analytics",
            command=self.load_analytics,
            bg='#667eea',
            fg='white'
        )
        refresh_btn.pack(pady=10)
    
    def add_task(self):
        """Add a new task"""
        name = self.task_name_input.get().strip()
        description = self.task_desc_input.get().strip()
        priority = self.priority_var.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter a task name!")
            return
        
        # Add to database
        self.db.add_task(name, description, '', priority)
        
        # Clear inputs
        self.task_name_input.delete(0, tk.END)
        self.task_desc_input.delete(0, tk.END)
        
        # Refresh display
        self.refresh_tasks()
        
        messagebox.showinfo("Success", "Task added!")
    
    def refresh_tasks(self):
        """Refresh the task list display"""
        self.task_list.delete(0, tk.END)
        
        tasks = self.db.get_all_tasks()
        
        if not tasks:
            self.task_list.insert(tk.END, "No tasks yet. Add one to get started!")
            return
        
        for task_id, name, description, due_date, priority, completed in tasks:
            # Add checkmark if completed
            status = "✓" if completed else " "
            
            # Format the display
            display_text = f"[{status}] {name} ({priority})"
            if description:
                display_text += f" - {description}"
            
            self.task_list.insert(tk.END, display_text)
            
            # Store task_id in a hidden variable (for reference)
            # We'll use the index to track which task to modify
    
    def mark_task_complete(self):
        """Mark selected task as complete"""
        selection = self.task_list.curselection()
        
        if not selection:
            messagebox.showerror("Error", "Please select a task!")
            return
        
        tasks = self.db.get_all_tasks()
        task_id = tasks[selection[0]][0]  # Get task_id
        
        self.db.mark_complete(task_id)
        self.refresh_tasks()
        messagebox.showinfo("Success", "Task marked complete!")
    
    def delete_task(self):
        """Delete selected task"""
        selection = self.task_list.curselection()
        
        if not selection:
            messagebox.showerror("Error", "Please select a task!")
            return
        
        if not messagebox.askyesno("Confirm", "Delete this task?"):
            return
        
        tasks = self.db.get_all_tasks()
        task_id = tasks[selection[0]][0]  # Get task_id
        
        self.db.delete_task(task_id)
        self.refresh_tasks()
        messagebox.showinfo("Success", "Task deleted!")
    
    def show_tasks_tab(self):
        """Show the tasks tab"""
        self.analytics_frame.pack_forget()
        self.tasks_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_analytics_tab(self):
        """Show the analytics tab"""
        self.tasks_frame.pack_forget()
        self.analytics_frame.pack(fill=tk.BOTH, expand=True)
        
        # Load and display analytics
        self.load_analytics()
    
    def load_analytics(self):
        """Load and display analytics"""
        # Get data from database
        df = self.db.get_analytics_data()
        
        # Create analytics object
        analytics = Analytics(df)
        
        # Get summary stats
        stats = analytics.get_summary_stats()
        
        # Display stats
        stats_text = f"""
        Total Tasks: {stats['total_tasks']}
        Completed: {stats['completed_tasks']}
        Pending: {stats['pending_tasks']}
        Completion Rate: {stats['completion_rate']}%
        """
        
        self.stats_text.config(text=stats_text)
        
        # Clear previous charts
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create and display charts if there's data
        if len(df) > 0:
            # Summary chart
            fig1 = analytics.create_summary_chart(self.chart_frame)
            canvas1 = FigureCanvasTkAgg(fig1, master=self.chart_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5)
            
            # Priority chart
            fig2 = analytics.create_priority_chart(self.chart_frame)
            canvas2 = FigureCanvasTkAgg(fig2, master=self.chart_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5)

# ============================================
# PART 4: RUN THE APP
# ============================================

if __name__ == "__main__":
    """
    This is where the program starts.
    
    if __name__ == "__main__" means:
    "Only run this code if this file is being run directly,
    not if it's imported into another file"
    """
    
    # Create the main window
    root = tk.Tk()
    
    # Create the app
    app = TaskFlowApp(root)
    
    # Run the app (this keeps the window open)
    root.mainloop()