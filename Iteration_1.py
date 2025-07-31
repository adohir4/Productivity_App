import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class KanbanBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Kanban Board")
        self.root.geometry("980x500")
        self.root.config(bg="#2b2d42")
        
        self.root.grid_columnconfigure((0, 1, 2), weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.todo_frame = self.create_frame("To-Do", 0, "#707699")
        self.doing_frame = self.create_frame("Doing", 1, "#669ee8")
        self.done_frame = self.create_frame("Done", 2, "#82f5ff")
        
        self.entry = ctk.CTkEntry(
            self.root, 
            width=300,
            font=("Calibri", 16),
            fg_color="#8d99ae",
            text_color="#edf2f4",
            corner_radius=10
        )
        self.entry.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        
        self.add_button = ctk.CTkButton(
            self.root,
            text="Add Task",
            command=self.add_task,
            fg_color="#33a86f",
            hover_color="#00589e",
            font=("Calibri", 16, "bold"),
            corner_radius=8
        )
        self.add_button.grid(row=1, column=2, pady=10, padx=10)

    def create_frame(self, title, col, bg_color):
        frame = ctk.CTkFrame(
            self.root,
            fg_color=bg_color,
            corner_radius=15,  
            border_width=2,
            border_color="#8d99ae"
        )
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        
        label = ctk.CTkLabel(
            frame, 
            text=title,
            font=("Calibri", 16, "bold"),
            text_color="white",
            fg_color="transparent",  
            corner_radius=0,         
            width=120,              
            anchor="center"         
        )
        label.pack(side=tk.TOP, pady=(12, 5))  

        textbox = ctk.CTkTextbox(
            frame,
            height=200,
            width=200,
            corner_radius=10,
            fg_color="#edf2f4",
            text_color="#2b2d42",
            font=("Arial", 12),
            wrap="none"
        )
        textbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        frame.textbox = textbox
        
        if col == 0:
            move_button = ctk.CTkButton(
                frame, 
                text="Move to Doing",
                fg_color="#06d6a0",
                hover_color="#05a181",
                corner_radius=8,
                command=lambda: self.move_task(self.todo_frame, self.doing_frame)
            )
        elif col == 1:
            move_button = ctk.CTkButton(
                frame, 
                text="Move to Done",
                fg_color="#06d6a0",
                hover_color="#05a181",
                corner_radius=8,
                command=lambda: self.move_task(self.doing_frame, self.done_frame)
            )
        else: 
            move_button = ctk.CTkButton(
                frame, 
                text="Delete Task",
                fg_color="#ef233c",
                hover_color="#d90429",
                corner_radius=8,
                command=lambda: self.delete_task(self.done_frame)
            )
        move_button.pack(side=tk.BOTTOM, pady=10)
        
        return frame
    
    def add_task(self):
        task = self.entry.get().strip()
        if task:
            self.todo_frame.textbox.insert("end", task + "\n")
            self.entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Task cannot be empty")
    
    def move_task(self, from_frame, to_frame):
        try:
            task = from_frame.textbox.get("1.0", "end-1c").strip()
            if task:
                from_frame.textbox.delete("1.0", "end")
                to_frame.textbox.insert("end", task + "\n")
        except:
            messagebox.showerror("Error", "No task selected")
    
    def delete_task(self, frame):
        try:
            frame.textbox.delete("1.0", "end")
        except:
            messagebox.showerror("Error", "No task selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = KanbanBoard(root)
    root.mainloop()