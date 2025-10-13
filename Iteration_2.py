import tkinter as tk
from tkinter import messagebox, colorchooser, simpledialog
import customtkinter as ctk
import json
import os
from datetime import datetime, timedelta

class Task:
    def __init__(self, content, due_date=None, priority="medium"):
        self.content = content
        self.due_date = due_date
        self.priority = priority
        self.id = id(self)  # Unique identifier for the task

class KanbanBoard:
    def __init__(self, root):
        self.root = root    
        self.root.title("Kanban Board")
        self.root.geometry("1200x700")
        
        # Default settings
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
        
        # Load saved settings if available
        self.load_settings()
        
        # Apply initial settings
        self.apply_settings()
        
        # Create menu
        self.create_menu()
        
        # Create frames
        self.todo_frame = self.create_frame("To-Do", 0, self.settings["colors"]["todo"])
        self.doing_frame = self.create_frame("Doing", 1, self.settings["colors"]["doing"])
        self.done_frame = self.create_frame("Done", 2, self.settings["colors"]["done"])
        
        # Create input area
        self.create_input_area()
        
        # Store tasks
        self.tasks = {
            "todo": [],
            "doing": [],
            "done": []
        }
        
    def create_menu(self):
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
        frame = ctk.CTkFrame(
            self.root,
            fg_color=bg_color,
            corner_radius=15,  
            border_width=2,
            border_color="#8d99ae"
        )
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weights for proper resizing
        self.root.grid_columnconfigure(col, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
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
        
        # Create a scrollable frame for tasks
        scroll_frame = ctk.CTkScrollableFrame(
            frame,
            fg_color="transparent",
            scrollbar_button_color="#8d99ae",
            scrollbar_button_hover_color="#6c7a9e"
        )
        scroll_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        frame.scroll_frame = scroll_frame
        
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
        input_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        input_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
        
        # Task input
        self.entry = ctk.CTkEntry(
            input_frame, 
            width=300,
            font=self.get_font(),
            fg_color="#8d99ae",
            text_color="#edf2f4",
            corner_radius=10,
            placeholder_text="Enter task description"
        )
        self.entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        self.entry.bind("<Return>", lambda e: self.add_task())
        
        # Due date input
        self.due_date_var = tk.StringVar()
        due_date_options = ["No due date", "Today", "Tomorrow", "In 2 days", "In 3 days", "In 5 days", "In 7 days"]
        self.due_date_menu = ctk.CTkOptionMenu(
            input_frame,
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
            input_frame,
            variable=self.priority_var,
            values=["low", "medium", "high"],
            font=self.get_font(),
            fg_color="#8d99ae",
            button_color="#6c7a9e",
            button_hover_color="#5a6788",
            dropdown_font=self.get_font()
        )
        priority_menu.pack(side=tk.LEFT, padx=10)
        
        self.add_button = ctk.CTkButton(
            input_frame,
            text="Add Task",
            command=self.add_task,
            fg_color="#33a86f",
            hover_color="#00589e",
            font=self.get_font("bold"),
            corner_radius=8
        )
        self.add_button.pack(side=tk.RIGHT, padx=10)
    
    def get_font(self, weight="normal", size=None):
        if size is None:
            size = self.settings["font_size"]
            
        if self.settings["dyslexia_mode"]:
            # Try to use OpenDyslexic if available
            try:
                # Check if OpenDyslexic is available
                available_fonts = list(tk.font.families())
                if "OpenDyslexic" in available_fonts:
                    return ("OpenDyslexic", size, weight)
                else:
                    # Fallback to Arial if OpenDyslexic is not available
                    return ("Arial", size, weight)
            except:
                # Fallback to Arial if there's an error
                return ("Arial", size, weight)
        else:
            if weight == "bold":
                return ("Calibri", size, "bold")
            return ("Calibri", size)
    
    def apply_settings(self):
        # Apply background color
        self.root.config(bg=self.settings["colors"]["background"])
        
        # Update theme for customtkinter
        ctk.set_appearance_mode("dark" if self.is_dark_color(self.settings["colors"]["background"]) else "light")
        
    def is_dark_color(self, hex_color):
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Calculate luminance
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance < 0.5
    
    def add_task(self):
        task_content = self.entry.get().strip()
        if not task_content:
            messagebox.showerror("Error", "Task cannot be empty")
            return
            
        # Parse due date
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
        
        # Create task
        task = Task(task_content, due_date, priority)
        self.tasks["todo"].append(task)
        
        # Create task widget
        self.create_task_widget(task, "todo")
        
        # Clear input
        self.entry.delete(0, tk.END)
        self.due_date_menu.set("No due date")
        self.priority_var.set("medium")
    
    def create_task_widget(self, task, column):
        # Determine which frame to add to
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
        
        # Due date if exists
        if task.due_date:
            due_date_str = task.due_date.strftime("%Y-%m-%d")
            due_label = ctk.CTkLabel(
                task_frame,
                text=f"Due: {due_date_str}",
                font=self.get_font(),
                text_color="#2b2d42"
            )
            due_label.pack(pady=2, padx=10, anchor="w")
            
            # Color code if task is overdue or due soon
            today = datetime.now().date()
            days_until_due = (task.due_date - today).days
            if days_until_due < 0:
                due_label.configure(text_color="#d90429", text=f"OVERDUE: {due_date_str}")
            elif days_until_due == 0:
                due_label.configure(text_color="#ff9e00", text=f"Due: Today")
            elif days_until_due <= 2:
                due_label.configure(text_color="#ff9e00", text=f"Due: {days_until_due} days")
        
        # Button frame
        button_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        button_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Buttons based on column
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
                text="Move",
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
                text="Move",
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
                text="Back",
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
        # Create edit dialog
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
        
        # If task has a due date, pre-select it
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
        
        # Save button
        def save_changes():
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
            
            # Update task
            task.content = new_content
            task.due_date = new_due_date
            task.priority = priority_var.get()
            
            # Find which column the task is in
            for col in ["todo", "doing", "done"]:
                if task in self.tasks[col]:
                    # Recreate the widget
                    task.widget.destroy()
                    self.create_task_widget(task, col)
                    break
            
            dialog.destroy()
        
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
        # Remove from current column
        self.tasks[from_column].remove(task)
        task.widget.destroy()
        
        # Add to new column
        self.tasks[to_column].append(task)
        self.create_task_widget(task, to_column)
    
    def delete_task(self, task, column):
        self.tasks[column].remove(task)
        task.widget.destroy()
    
    def move_all_tasks(self, from_column, to_column):
        if not self.tasks[from_column]:
            messagebox.showinfo("Info", f"No tasks to move from {from_column}")
            return
            
        # Move all tasks
        for task in self.tasks[from_column][:]:  # Use slice to copy list
            self.move_task(task, from_column, to_column)
    
    def clear_all_tasks(self, column):
        if not self.tasks[column]:
            messagebox.showinfo("Info", f"No tasks to clear from {column}")
            return
            
        # Confirm deletion
        if messagebox.askyesno("Confirm", f"Are you sure you want to clear all tasks from {column}?"):
            for task in self.tasks[column][:]:  # Use slice to copy list
                self.delete_task(task, column)
    
    def show_color_customization_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Customize Colors")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create a frame for the color options
        options_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        options_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ctk.CTkLabel(
            options_frame, 
            text="Customize Colors", 
            font=self.get_font("bold", 16),
            text_color=self.settings["colors"]["text"]
        )
        title_label.pack(pady=10)
        
        # Color options with dropdowns
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
        
        # Store the StringVars for each color option
        color_vars = {}
        
        for display_name, color_key in color_options:
            # Create a frame for each color option
            option_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
            option_frame.pack(fill=tk.X, pady=5)
            
            # Label
            label = ctk.CTkLabel(
                option_frame, 
                text=display_name + ":", 
                font=self.get_font(),
                text_color=self.settings["colors"]["text"],
                width=150,
                anchor="w"
            )
            label.pack(side=tk.LEFT, padx=5)
            
            # Current color display
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
            
            # Color selection button
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
        self.todo_frame.configure(fg_color=self.settings["colors"]["todo"])
        self.doing_frame.configure(fg_color=self.settings["colors"]["doing"])
        self.done_frame.configure(fg_color=self.settings["colors"]["done"])
    
    def toggle_dyslexia_mode(self):
        self.settings["dyslexia_mode"] = not self.settings["dyslexia_mode"]
        
        # Check if OpenDyslexic font is available
        try:
            available_fonts = list(tk.font.families())
            if self.settings["dyslexia_mode"] and "OpenDyslexic" not in available_fonts:
                messagebox.showwarning("Font Not Available", 
                                      "OpenDyslexic font is not installed on your system. "
                                      "Please install it for the best dyslexia-friendly experience. "
                                      "Using Arial as fallback.")
        except:
            pass
            
        self.update_fonts()
        self.save_settings()
        status = "enabled" if self.settings["dyslexia_mode"] else "disabled"
        messagebox.showinfo("Dyslexia Mode", f"Dyslexia mode {status}")
    
    def change_font_size(self):
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
        # Update all widgets with new font settings
        font = self.get_font()
        bold_font = self.get_font("bold")
        
        # Update frames
        for frame in [self.todo_frame, self.doing_frame, self.done_frame]:
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(font=bold_font)
        
        # Update input area
        self.entry.configure(font=font)
        self.due_date_menu.configure(font=font, dropdown_font=font)
        self.add_button.configure(font=bold_font)
        
        # Recreate all task widgets to update fonts
        for column in ["todo", "doing", "done"]:
            for task in self.tasks[column]:
                task.widget.destroy()
                self.create_task_widget(task, column)
    
    def reset_settings(self):
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
        
        # Recreate all task widgets to update colors
        for column in ["todo", "doing", "done"]:
            for task in self.tasks[column]:
                task.widget.destroy()
                self.create_task_widget(task, column)
                
        self.update_fonts()
        self.save_settings()
        messagebox.showinfo("Settings Reset", "All settings have been reset to defaults")
    
    def load_settings(self):
        try:
            if os.path.exists("kanban_settings.json"):
                with open("kanban_settings.json", "r") as f:
                    loaded_settings = json.load(f)
                    # Merge with default settings to ensure all keys exist
                    for key in self.settings:
                        if key in loaded_settings:
                            if isinstance(self.settings[key], dict):
                                self.settings[key].update(loaded_settings[key])
                            else:
                                self.settings[key] = loaded_settings[key]
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        try:
            with open("kanban_settings.json", "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KanbanBoard(root)
    root.mainloop()
