import tkinter as tk
from tkinter import messagebox, colorchooser, simpledialog
import customtkinter as ctk
import json
import os
from datetime import datetime, timedelta
from calendar import monthrange, month_name

# Create main window
root = tk.Tk()
root.title("Task Manager & Calendar")
root.geometry("1400x800")

class Task:
    def __init__(self, content, due_date=None, priority="medium"):
        self.content = content
        self.due_date = due_date
        self.priority = priority
        self.id = id(self)
    
    def to_dict(self):
        return {
            "content": self.content,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "id": self.id
        }
    
    @classmethod
    def from_dict(cls, data):
        due_date = datetime.fromisoformat(data["due_date"]).date() if data["due_date"] else None
        task = cls(data["content"], due_date, data["priority"])
        task.id = data["id"]
        return task

class CalendarView:
    def __init__(self, parent, kanban_board):
        self.parent = parent
        self.kanban_board = kanban_board
        self.main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
    
    def show(self):
        # Show the calendar by packing the main frame
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.update_calendar()
    
    def hide(self):
        # Hide the calendar
        self.main_frame.pack_forget()
    
    def update_calendar(self):
        # Update the calendar display with current tasks
        # Clear the calendar frame first
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add toggle button for calendar view to switch back to Kanban
        toggle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        toggle_frame.pack(fill=tk.X, pady=10, padx=10)
        
        toggle_button = ctk.CTkButton(
            toggle_frame,
            text="📋 Switch to Kanban View",
            command=self.kanban_board.toggle_view,
            fg_color="#5D8DA0",
            hover_color="#586D75",
            font=self.kanban_board.get_font("bold"),
            corner_radius=8,
            width=200
        )
        toggle_button.pack(pady=5)
        
        # Create calendar header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill=tk.X, pady=10)
        
        # Previous month button
        prev_btn = ctk.CTkButton(
            header_frame,
            text="◀ Previous",
            font=self.kanban_board.get_font("bold"),
            command=lambda: self.change_calendar_month(-1),
            fg_color="#4cc9f0",
            hover_color="#3a97b8"
        )
        prev_btn.pack(side=tk.LEFT, padx=10)
        
        # Month and year label
        month_label = ctk.CTkLabel(
            header_frame,
            text=f"{month_name[self.current_month]} {self.current_year}",
            font=self.kanban_board.get_font("bold", 20),
            text_color="black"  # Changed to black for better visibility
        )
        month_label.pack(side=tk.LEFT, expand=True)
        
        # Next month button
        next_btn = ctk.CTkButton(
            header_frame,
            text="Next ▶",
            font=self.kanban_board.get_font("bold"),
            command=lambda: self.change_calendar_month(1),
            fg_color="#4cc9f0",
            hover_color="#3a97b8"
        )
        next_btn.pack(side=tk.RIGHT, padx=10)
        
        # Create days of week header
        days_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        days_frame.pack(fill=tk.X, pady=5)
        
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for day in days:
            day_label = ctk.CTkLabel(
                days_frame,
                text=day,
                font=self.kanban_board.get_font("bold"),
                text_color="black",  # Changed to black for better visibility
                width=140,
                height=30
            )
            day_label.pack(side=tk.LEFT, padx=2, expand=True)
        
        # Create calendar grid
        calendar_grid = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        calendar_grid.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Get number of days in month and first weekday
        num_days = monthrange(self.current_year, self.current_month)[1]
        first_weekday = monthrange(self.current_year, self.current_month)[0]
        
        # Get all tasks with due dates
        all_tasks = []
        for status in ["todo", "doing", "done"]:
            all_tasks.extend(self.kanban_board.tasks[status])
        
        # Group tasks by due date
        tasks_by_date = {}
        for task in all_tasks:
            if task.due_date:
                if (task.due_date.year == self.current_year and 
                    task.due_date.month == self.current_month):
                    date_str = task.due_date.strftime("%Y-%m-%d")
                    if date_str not in tasks_by_date:
                        tasks_by_date[date_str] = []
                    tasks_by_date[date_str].append(task)
        
        # Create empty cells for days before the first day of the month
        row = 0
        col = 0
        for i in range(first_weekday):
            empty_cell = ctk.CTkFrame(calendar_grid, width=140, height=120, fg_color="transparent")
            empty_cell.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
        
        today = datetime.now().date()
        
        # Create cells for each day of the month
        for day in range(1, num_days + 1):
            if col > 6:
                col = 0
                row += 1
            
            # Create day cell
            cell_bg = "#edf2f4"
            cell_date = datetime(self.current_year, self.current_month, day).date()
            
            # Highlight today
            if (cell_date == today and 
                self.current_month == today.month and 
                self.current_year == today.year):
                cell_bg = "#ffe66d"  # Yellow highlight for today
            
            cell = ctk.CTkFrame(calendar_grid, width=140, height=120, 
                               corner_radius=10, border_width=2,
                               border_color="#8d99ae", fg_color=cell_bg)
            cell.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # Day number
            day_label = ctk.CTkLabel(
                cell,
                text=str(day),
                font=self.kanban_board.get_font("bold", 14),
                text_color="black"  # Changed to black for better visibility
            )
            day_label.place(x=5, y=5)
            
            # Check if this day has tasks
            date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
            if date_str in tasks_by_date:
                tasks = tasks_by_date[date_str]
                
                # Show task count
                count_label = ctk.CTkLabel(
                    cell,
                    text=f"{len(tasks)} task(s)",
                    font=self.kanban_board.get_font(size=10),
                    text_color="black"  # Changed to black for better visibility
                )
                count_label.place(x=5, y=30)
                
                # Show task preview (first task only)
                if tasks:
                    task_preview = tasks[0].content
                    if len(task_preview) > 15:
                        task_preview = task_preview[:12] + "..."
                    
                    preview_label = ctk.CTkLabel(
                        cell,
                        text=task_preview,
                        font=self.kanban_board.get_font(size=10),
                        text_color="black",  # Changed to black for better visibility
                        wraplength=130
                    )
                    preview_label.place(x=5, y=50)
            
            col += 1
        
        # Configure grid weights for proper resizing
        for i in range(7):
            calendar_grid.columnconfigure(i, weight=1)
        for i in range(6):  # Maximum 6 rows in a month
            calendar_grid.rowconfigure(i, weight=1)
    
    def change_calendar_month(self, delta):
        # Change the calendar month by delta (-1 for previous, 1 for next)
        self.current_month += delta
        
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        
        self.update_calendar()

class KanbanBoard:
    def __init__(self, parent):
        self.root = parent
        
        # Create main container for Kanban board
        self.main_frame = tk.Frame(parent)
        
        # Default settings for colors, fonts, etc.
        self.settings = {
            "colors": {
                "todo": "#97CAC9",
                "doing": "#8EA09F",
                "done": "#547574",
                "background": "#42484B",
                "text": "#edf2f4",
                "high_priority": "#ff6b6b",
                "medium_priority": "#ffe66d",
                "low_priority": "#4ecdc4"
            },
            "dyslexia_mode": False,
            "font_size": 12
        }
        
        # Load saved settings if available
        self.load_settings()
        self.apply_settings()
        
        # Create UI components
        self.create_menu()
        self.create_view_toggle()
        
        # Create Kanban columns
        self.todo_frame = self.create_frame("To-Do", 0, self.settings["colors"]["todo"])
        self.doing_frame = self.create_frame("Doing", 1, self.settings["colors"]["doing"])
        self.done_frame = self.create_frame("Done", 2, self.settings["colors"]["done"])
        
        # Create task input area
        self.create_input_area()
        
        # Create calendar instance
        self.calendar_view = CalendarView(parent, self)
        
        # Initialize task storage
        self.tasks = {
            "todo": [],
            "doing": [],
            "done": []
        }
        
        # Load saved tasks
        self.load_tasks()
        self.show()
        
    def show(self):
        # Show the kanban board
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_view_toggle(self):
        # Create a button to toggle between Kanban and Calendar views
        toggle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        toggle_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
        
        self.view_toggle_button = ctk.CTkButton(
            toggle_frame,
            text="📅 Switch to Calendar View",
            command=self.toggle_view,
            fg_color="#5D8DA0",
            hover_color="#586D75",
            font=self.get_font("bold"),
            corner_radius=8,
            width=200
        )
        self.view_toggle_button.pack(pady=5)
        
    def toggle_view(self):
        # Toggle between Kanban and Calendar views
        if hasattr(self.calendar_view, 'main_frame') and self.calendar_view.main_frame.winfo_ismapped():
            # Switch to Kanban view
            self.calendar_view.hide()
            self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.view_toggle_button.configure(text="📅 Switch to Calendar View")
        else:
            # Switch to Calendar view
            self.main_frame.pack_forget()
            self.calendar_view.show()
            self.view_toggle_button.configure(text="📋 Switch to Kanban View")
    
    def create_menu(self):
        # Create application menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Customize Colors", command=self.show_color_customization_dialog)
        settings_menu.add_command(label="Toggle Dyslexia Mode", command=self.toggle_dyslexia_mode)
        settings_menu.add_command(label="Change Font Size", command=self.change_font_size)
        settings_menu.add_separator()
        settings_menu.add_command(label="Reset to Defaults", command=self.reset_settings)
        
    def create_frame(self, title, col, bg_color):
        # Create a Kanban column frame
        frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=bg_color,
            corner_radius=15,
            border_width=2,
            border_color="#8d99ae"
        )
        frame.grid(row=1, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights for proper resizing
        self.main_frame.grid_columnconfigure(col, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Column title
        label = ctk.CTkLabel(
            frame, 
            text=title,
            font=self.get_font("bold"),
            text_color="white",
            fg_color="transparent",
            corner_radius=0,
            width=120,
            anchor="center"
        )
        label.pack(side=tk.TOP, pady=(12, 5))
        
        # Scrollable frame for tasks
        scroll_frame = ctk.CTkScrollableFrame(
            frame,
            fg_color="transparent",
            scrollbar_button_color="#8d99ae",
            scrollbar_button_hover_color="#6c7a9e"
        )
        scroll_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        frame.scroll_frame = scroll_frame
        
        # Add action buttons based on column type
        if col == 0:
            move_button = ctk.CTkButton(
                frame, 
                text="Move All to Doing",
                fg_color="#06d6a0",
                hover_color="#05a181",
                corner_radius=8,
                font=self.get_font(),
                command=lambda: self.move_all_tasks("todo", "doing")
            )
        elif col == 1:
            move_button = ctk.CTkButton(
                frame, 
                text="Move All to Done",
                fg_color="#06d6a0",
                hover_color="#05a181",
                corner_radius=8,
                font=self.get_font(),
                command=lambda: self.move_all_tasks("doing", "done")
            )
        else: 
            move_button = ctk.CTkButton(
                frame, 
                text="Clear All Tasks",
                fg_color="#ef233c",
                hover_color="#d90429",
                corner_radius=8,
                font=self.get_font(),
                command=lambda: self.clear_all_tasks("done")
            )
        move_button.pack(side=tk.BOTTOM, pady=10)
        
        return frame
    
    def create_input_area(self):
        # Create task input area at the bottom
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
        
        # Task description input
        self.entry = ctk.CTkEntry(
            self.input_frame, 
            width=300,
            font=self.get_font(),
            fg_color="#8d99ae",
            text_color="#edf2f4",
            corner_radius=10,
            placeholder_text="Enter task description"
        )
        self.entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        self.entry.bind("<Return>", lambda e: self.add_task())
        
        # Due date selection
        self.due_date_var = tk.StringVar()
        due_date_options = ["No due date", "Today", "Tomorrow", "In 2 days", "In 3 days", "In 5 days", "In 7 days"]
        self.due_date_menu = ctk.CTkOptionMenu(
            self.input_frame,
            variable=self.due_date_var,
            values=due_date_options,
            font=self.get_font(),
            fg_color="#8d99ae",
            button_color="#6c7a9e",
            button_hover_color="#5a6788",
            dropdown_font=self.get_font()
        )
        self.due_date_menu.set("No due date")
        self.due_date_menu.pack(side=tk.LEFT, padx=10)
        
        # Priority selection
        self.priority_var = tk.StringVar(value="medium")
        priority_menu = ctk.CTkOptionMenu(
            self.input_frame,
            variable=self.priority_var,
            values=["low", "medium", "high"],
            font=self.get_font(),
            fg_color="#8d99ae",
            button_color="#6c7a9e",
            button_hover_color="#5a6788",
            dropdown_font=self.get_font()
        )
        priority_menu.pack(side=tk.LEFT, padx=10)
        
        # Add task button
        self.add_button = ctk.CTkButton(
            self.input_frame,
            text="Add Task",
            command=self.add_task,
            fg_color="#33a86f",
            hover_color="#00589e",
            font=self.get_font("bold"),
            corner_radius=8
        )
        self.add_button.pack(side=tk.RIGHT, padx=10)
    
    def get_font(self, weight="normal", size=None):
        # Get appropriate font based on settings
        if size is None:
            size = self.settings["font_size"]
            
        if self.settings["dyslexia_mode"]:
            # Use dyslexia-friendly font if available
            try:
                available_fonts = list(tk.font.families())
                if "OpenDyslexic" in available_fonts:
                    return ("OpenDyslexic", size, weight)
                else:
                    return ("Arial", size, weight)
            except:
                return ("Arial", size, weight)
        else:
            if weight == "bold":
                return ("Calibri", size, "bold")
            return ("Calibri", size)
    
    def apply_settings(self):
        # Apply current settings to the UI
        self.main_frame.config(bg=self.settings["colors"]["background"])
        ctk.set_appearance_mode("dark" if self.is_dark_color(self.settings["colors"]["background"]) else "light")
        
    def is_dark_color(self, hex_color):
        # Check if a color is dark for theme purposes
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance < 0.5
    
    def add_task(self):
        # Add a new task to the To-Do column
        task_content = self.entry.get().strip()
        if not task_content:
            messagebox.showerror("Error", "Task cannot be empty")
            return
            
        # Parse due date from selection
        due_date_option = self.due_date_var.get()
        due_date = None
        if due_date_option != "No due date":
            today = datetime.now().date()
            if due_date_option == "Today":
                due_date = today
            elif due_date_option == "Tomorrow":
                due_date = today + timedelta(days=1)
            elif due_date_option == "In 2 days":
                due_date = today + timedelta(days=2)
            elif due_date_option == "In 3 days":
                due_date = today + timedelta(days=3)
            elif due_date_option == "In 5 days":
                due_date = today + timedelta(days=5)
            elif due_date_option == "In 7 days":
                due_date = today + timedelta(days=7)
        
        # Get priority
        priority = self.priority_var.get()
        
        # Create and add task
        task = Task(task_content, due_date, priority)
        self.tasks["todo"].append(task)
        
        # Create task widget
        self.create_task_widget(task, "todo")
        
        # Clear input fields
        self.entry.delete(0, tk.END)
        self.due_date_menu.set("No due date")
        self.priority_var.set("medium")
        
        # Save tasks to file
        self.save_tasks()
    
    def create_task_widget(self, task, column):
        # Create a widget for a task in the specified column
        if column == "todo":
            parent = self.todo_frame.scroll_frame
        elif column == "doing":
            parent = self.doing_frame.scroll_frame
        else:
            parent = self.done_frame.scroll_frame
        
        # Determine priority color
        if task.priority == "high":
            bg_color = self.settings["colors"]["high_priority"]
        elif task.priority == "low":
            bg_color = self.settings["colors"]["low_priority"]
        else:
            bg_color = self.settings["colors"]["medium_priority"]
        
        # Create task frame
        task_frame = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=10,
            border_width=1,
            border_color="#8d99ae"
        )
        task_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Task content
        content_label = ctk.CTkLabel(
            task_frame,
            text=task.content,
            font=self.get_font(),
            text_color="#2b2d42",
            wraplength=250,
            justify="left"
        )
        content_label.pack(pady=5, padx=10, anchor="w")
        
        # Due date display
        if task.due_date:
            due_date_str = task.due_date.strftime("%Y-%m-%d")
            due_label = ctk.CTkLabel(
                task_frame,
                text=f"Due: {due_date_str}",
                font=self.get_font(),
                text_color="#2b2d42"
            )
            due_label.pack(pady=2, padx=10, anchor="w")
            
            # Color code for overdue/upcoming tasks
            today = datetime.now().date()
            days_until_due = (task.due_date - today).days
            if days_until_due < 0:
                due_label.configure(text_color="#d90429", text=f"OVERDUE: {due_date_str}")
            elif days_until_due == 0:
                due_label.configure(text_color="#ff9e00", text=f"Due: Today")
            elif days_until_due <= 2:
                due_label.configure(text_color="#ff9e00", text=f"Due: {days_until_due} days")
        
        # Button frame for task actions
        button_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        button_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Buttons vary by column
        if column == "todo":
            edit_btn = ctk.CTkButton(
                button_frame,
                text="Edit",
                width=60,
                font=self.get_font(size=10),
                fg_color="#4cc9f0",
                hover_color="#3a97b8",
                command=lambda t=task: self.edit_task(t)
            )
            edit_btn.pack(side=tk.LEFT, padx=5)
            
            move_btn = ctk.CTkButton(
                button_frame,
                text="Start",
                width=60,
                font=self.get_font(size=10),
                fg_color="#06d6a0",
                hover_color="#05a181",
                command=lambda t=task: self.move_task(t, column, "doing")
            )
            move_btn.pack(side=tk.LEFT, padx=5)
            
            delete_btn = ctk.CTkButton(
                button_frame,
                text="Delete",
                width=60,
                font=self.get_font(size=10),
                fg_color="#ef233c",
                hover_color="#d90429",
                command=lambda t=task: self.delete_task(t, column)
            )
            delete_btn.pack(side=tk.LEFT, padx=5)
            
        elif column == "doing":
            edit_btn = ctk.CTkButton(
                button_frame,
                text="Edit",
                width=60,
                font=self.get_font(size=10),
                fg_color="#4cc9f0",
                hover_color="#3a97b8",
                command=lambda t=task: self.edit_task(t)
            )
            edit_btn.pack(side=tk.LEFT, padx=5)
            
            back_btn = ctk.CTkButton(
                button_frame,
                text="Back",
                width=60,
                font=self.get_font(size=10),
                fg_color="#9d4edd",
                hover_color="#7a3bad",
                command=lambda t=task: self.move_task(t, column, "todo")
            )
            back_btn.pack(side=tk.LEFT, padx=5)
            
            move_btn = ctk.CTkButton(
                button_frame,
                text="Complete",
                width=60,
                font=self.get_font(size=10),
                fg_color="#06d6a0",
                hover_color="#05a181",
                command=lambda t=task: self.move_task(t, column, "done")
            )
            move_btn.pack(side=tk.LEFT, padx=5)
            
            delete_btn = ctk.CTkButton(
                button_frame,
                text="Delete",
                width=60,
                font=self.get_font(size=10),
                fg_color="#ef233c",
                hover_color="#d90429",
                command=lambda t=task: self.delete_task(t, column)
            )
            delete_btn.pack(side=tk.LEFT, padx=5)
            
        else:  # done column
            back_btn = ctk.CTkButton(
                button_frame,
                text="Reopen",
                width=80,
                font=self.get_font(size=10),
                fg_color="#9d4edd",
                hover_color="#7a3bad",
                command=lambda t=task: self.move_task(t, column, "doing")
            )
            back_btn.pack(side=tk.LEFT, padx=5)
            
            delete_btn = ctk.CTkButton(
                button_frame,
                text="Delete",
                width=80,
                font=self.get_font(size=10),
                fg_color="#ef233c",
                hover_color="#d90429",
                command=lambda t=task: self.delete_task(t, column)
            )
            delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Store reference to task frame
        task.widget = task_frame
    
    def edit_task(self, task):
        # Open dialog to edit task details
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Task content
        content_label = ctk.CTkLabel(dialog, text="Task Description:", font=self.get_font())
        content_label.pack(pady=10)
        
        content_entry = ctk.CTkEntry(
            dialog, 
            width=350,
            font=self.get_font(),
            fg_color="#8d99ae",
            text_color="#edf2f4"
        )
        content_entry.insert(0, task.content)
        content_entry.pack(pady=5, padx=20)
        
        # Due date
        due_label = ctk.CTkLabel(dialog, text="Due Date:", font=self.get_font())
        due_label.pack(pady=10)
        
        current_due_date = task.due_date.strftime("%Y-%m-%d") if task.due_date else ""
        
        due_entry = ctk.CTkEntry(
            dialog, 
            width=350,
            font=self.get_font(),
            fg_color="#8d99ae",
            text_color="#edf2f4",
            placeholder_text="YYYY-MM-DD (leave empty for no due date)"
        )
        if current_due_date:
            due_entry.insert(0, current_due_date)
        due_entry.pack(pady=5, padx=20)
        
        # Priority
        priority_label = ctk.CTkLabel(dialog, text="Priority:", font=self.get_font())
        priority_label.pack(pady=10)
        
        priority_var = tk.StringVar(value=task.priority)
        priority_menu = ctk.CTkOptionMenu(
            dialog,
            variable=priority_var,
            values=["low", "medium", "high"],
            font=self.get_font(),
            fg_color="#8d99ae",
            button_color="#6c7a9e"
        )
        priority_menu.pack(pady=5)
        
        def save_changes():
            # Save changes from edit dialog
            new_content = content_entry.get().strip()
            if not new_content:
                messagebox.showerror("Error", "Task cannot be empty", parent=dialog)
                return
                
            new_due_date_str = due_entry.get().strip()
            new_due_date = None
            if new_due_date_str:
                try:
                    new_due_date = datetime.strptime(new_due_date_str, "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD", parent=dialog)
                    return
            
            # Update task properties
            task.content = new_content
            task.due_date = new_due_date
            task.priority = priority_var.get()
            
            # Recreate widget with updated values
            for col in ["todo", "doing", "done"]:
                if task in self.tasks[col]:
                    task.widget.destroy()
                    self.create_task_widget(task, col)
                    break
            
            # Update calendar if visible
            if hasattr(self.calendar_view, 'main_frame') and self.calendar_view.main_frame.winfo_ismapped():
                self.calendar_view.update_calendar()
            
            # Save changes
            self.save_tasks()
            dialog.destroy()
        
        # Save button
        save_btn = ctk.CTkButton(
            dialog,
            text="Save Changes",
            font=self.get_font("bold"),
            fg_color="#33a86f",
            hover_color="#00589e",
            command=save_changes
        )
        save_btn.pack(pady=20)
    
    def move_task(self, task, from_column, to_column):
        # Move task between columns
        self.tasks[from_column].remove(task)
        task.widget.destroy()
        
        self.tasks[to_column].append(task)
        self.create_task_widget(task, to_column)
        
        # Update calendar if visible
        if hasattr(self.calendar_view, 'main_frame') and self.calendar_view.main_frame.winfo_ismapped():
            self.calendar_view.update_calendar()
        
        # Save changes
        self.save_tasks()
    
    def delete_task(self, task, column):
        # Delete task from column
        self.tasks[column].remove(task)
        task.widget.destroy()
        
        # Update calendar if visible
        if hasattr(self.calendar_view, 'main_frame') and self.calendar_view.main_frame.winfo_ismapped():
            self.calendar_view.update_calendar()
        
        # Save changes
        self.save_tasks()
    
    def move_all_tasks(self, from_column, to_column):
        # Move all tasks from one column to another
        if not self.tasks[from_column]:
            messagebox.showinfo("Info", f"No tasks to move from {from_column}")
            return
            
        for task in self.tasks[from_column][:]:
            self.move_task(task, from_column, to_column)
    
    def clear_all_tasks(self, column):
        # Clear all tasks from a column
        if not self.tasks[column]:
            messagebox.showinfo("Info", f"No tasks to clear from {column}")
            return
            
        if messagebox.askyesno("Confirm", f"Are you sure you want to clear all tasks from {column}?"):
            for task in self.tasks[column][:]:
                self.delete_task(task, column)
    
    def show_color_customization_dialog(self):
        # Open color customization dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Customize Colors")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        options_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        options_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        title_label = ctk.CTkLabel(
            options_frame, 
            text="Customize Colors", 
            font=self.get_font("bold", 16),
            text_color=self.settings["colors"]["text"]
        )
        title_label.pack(pady=10)
        
        # Color options
        color_options = [
            ("To-Do Column", "todo"),
            ("Doing Column", "doing"),
            ("Done Column", "done"),
            ("Background", "background"),
            ("Text Color", "text"),
            ("High Priority", "high_priority"),
            ("Medium Priority", "medium_priority"),
            ("Low Priority", "low_priority")
        ]
        
        for display_name, color_key in color_options:
            option_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
            option_frame.pack(fill=tk.X, pady=5)
            
            label = ctk.CTkLabel(
                option_frame, 
                text=display_name + ":", 
                font=self.get_font(),
                text_color=self.settings["colors"]["text"],
                width=150,
                anchor="w"
            )
            label.pack(side=tk.LEFT, padx=5)
            
            # Color display
            color_display = ctk.CTkFrame(
                option_frame, 
                width=50, 
                height=30,
                fg_color=self.settings["colors"][color_key],
                corner_radius=5,
                border_width=1,
                border_color="#8d99ae"
            )
            color_display.pack(side=tk.LEFT, padx=5)
            
            # Color selection callback
            def make_color_callback(key, display):
                def callback():
                    color = colorchooser.askcolor(initialcolor=self.settings["colors"][key])[1]
                    if color:
                        self.settings["colors"][key] = color
                        display.configure(fg_color=color)
                        self.apply_settings()
                        self.update_frame_colors()
                        # Update task widgets if priority colors changed
                        if key in ["high_priority", "medium_priority", "low_priority"]:
                            for column in ["todo", "doing", "done"]:
                                for task in self.tasks[column]:
                                    if task.priority == key.split('_')[0]:
                                        task.widget.configure(fg_color=color)
                        self.save_settings()
                return callback
            
            color_btn = ctk.CTkButton(
                option_frame,
                text="Choose Color",
                width=100,
                font=self.get_font(),
                command=make_color_callback(color_key, color_display)
            )
            color_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            font=self.get_font("bold"),
            fg_color="#ef233c",
            hover_color="#d90429",
            command=dialog.destroy
        )
        close_btn.pack(pady=20)
    
    def update_frame_colors(self):
        # Update Kanban column colors
        self.todo_frame.configure(fg_color=self.settings["colors"]["todo"])
        self.doing_frame.configure(fg_color=self.settings["colors"]["doing"])
        self.done_frame.configure(fg_color=self.settings["colors"]["done"])
    
    def toggle_dyslexia_mode(self):
        # Toggle dyslexia-friendly font mode
        self.settings["dyslexia_mode"] = not self.settings["dyslexia_mode"]
        
        try:
            available_fonts = list(tk.font.families())
            if self.settings["dyslexia_mode"] and "OpenDyslexic" not in available_fonts:
                messagebox.showwarning("Font Not Available", 
                                      "OpenDyslexic font is not installed on your system. "
                                      "Using Arial as fallback.")
        except:
            pass
            
        self.update_fonts()
        self.save_settings()
        status = "enabled" if self.settings["dyslexia_mode"] else "disabled"
        messagebox.showinfo("Dyslexia Mode", f"Dyslexia mode {status}")
    
    def change_font_size(self):
        # Change application font size
        new_size = simpledialog.askinteger(
            "Font Size", 
            "Enter new font size (8-24):",
            initialvalue=self.settings["font_size"],
            minvalue=8,
            maxvalue=24
        )
        if new_size:
            self.settings["font_size"] = new_size
            self.update_fonts()
            self.save_settings()
    
    def update_fonts(self):
        # Update all fonts in the application
        font = self.get_font()
        bold_font = self.get_font("bold")
        
        # Update frame labels
        for frame in [self.todo_frame, self.doing_frame, self.done_frame]:
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(font=bold_font)
        
        # Update input area
        self.entry.configure(font=font)
        self.due_date_menu.configure(font=font, dropdown_font=font)
        self.add_button.configure(font=bold_font)
        
        # Recreate all task widgets with new fonts
        for column in ["todo", "doing", "done"]:
            for task in self.tasks[column]:
                task.widget.destroy()
                self.create_task_widget(task, column)
    
    def reset_settings(self):
        # Reset all settings to defaults
        self.settings = {
            "colors": {
                "todo": "#707699",
                "doing": "#669ee8",
                "done": "#82f5ff",
                "background": "#2b2d42",
                "text": "#edf2f4",
                "high_priority": "#ff6b6b",
                "medium_priority": "#ffe66d",
                "low_priority": "#4ecdc4"
            },
            "dyslexia_mode": False,
            "font_size": 12
        }
        self.apply_settings()
        self.update_frame_colors()
        # Recreate all task widgets with default colors
        for column in ["todo", "doing", "done"]:
            for task in self.tasks[column]:
                task.widget.destroy()
                self.create_task_widget(task, column)          
        self.update_fonts()
        self.save_settings()
        messagebox.showinfo("Settings Reset", "All settings have been reset to defaults")
    
    def load_settings(self):
        # Load settings from JSON file
        try:
            if os.path.exists("kanban_settings.json"):
                with open("kanban_settings.json", "r") as f:
                    loaded_settings = json.load(f)
                    # Merge with default settings
                    for key in self.settings:
                        if key in loaded_settings:
                            if isinstance(self.settings[key], dict):
                                self.settings[key].update(loaded_settings[key])
                            else:
                                self.settings[key] = loaded_settings[key]
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        # Save settings to JSON file
        try:
            with open("kanban_settings.json", "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def load_tasks(self):
        # Load tasks from JSON file
        try:
            if os.path.exists("kanban_tasks.json"):
                with open("kanban_tasks.json", "r") as f:
                    tasks_data = json.load(f)
                    
                    # Clear existing tasks
                    self.tasks = {"todo": [], "doing": [], "done": []}
                    
                    # Load tasks for each column
                    for column in ["todo", "doing", "done"]:
                        if column in tasks_data:
                            for task_dict in tasks_data[column]:
                                try:
                                    task = Task.from_dict(task_dict)
                                    self.tasks[column].append(task)
                                    self.create_task_widget(task, column)
                                except Exception as e:
                                    print(f"Error loading task: {e}")
                                    continue
                    
                print(f"Loaded {len(self.tasks['todo'])} todo, {len(self.tasks['doing'])} doing, {len(self.tasks['done'])} done tasks")
            else:
                print("No saved tasks found")
        except Exception as e:
            print(f"Error loading tasks: {e}")
    
    def save_tasks(self):
        # Save tasks to JSON file
        try:
            tasks_data = {
                "todo": [task.to_dict() for task in self.tasks["todo"]],
                "doing": [task.to_dict() for task in self.tasks["doing"]],
                "done": [task.to_dict() for task in self.tasks["done"]]
            }
            with open("kanban_tasks.json", "w") as f:
                json.dump(tasks_data, f, indent=4, default=str)
            
            print(f"Saved {len(self.tasks['todo'])} todo, {len(self.tasks['doing'])} doing, {len(self.tasks['done'])} done tasks")
        except Exception as e:
            print(f"Error saving tasks: {e}")

# Create and start the application
try:
    kanban_board = KanbanBoard(root)
    print("Application started successfully")
except Exception as e:
    print(f"Error starting application: {e}")
    messagebox.showerror("Error", f"Failed to start application: {e}")

# Start the application
root.mainloop()
