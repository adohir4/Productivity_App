import tkinter as tk
from tkinter import messagebox, colorchooser, simpledialog
import customtkinter as ctk
import json
import os
from datetime import datetime, timedelta
from calendar import monthrange, month_name
from PIL import ImageTk, Image
import random

# Create main window
root = tk.Tk()
root.title("Motivation Pet & Task Manager")
root.geometry("1400x800")

# Load and prepare images for virtual pet
def load_scaled_image(image_path, scale_factor=0.6):
    """Load and scale images by a factor to maintain quality"""
    try:
        img = Image.open(image_path)
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        #return a blank image as fallback
        blank_img = Image.new('RGB', (100, 100), color='gray')
        return ImageTk.PhotoImage(blank_img)

#load all virtual pet images
scale_factor = 0.5

cat = load_scaled_image("images/cat1.png", scale_factor)
cat_interact = load_scaled_image("images/cat2.png", scale_factor)
cat_profile = load_scaled_image("images/caticon1.png", 0.4)
cat_profile_interact = load_scaled_image("images/caticon2.png", 0.4)

bunny = load_scaled_image("images/bunny1.png", scale_factor)
bunny_interact = load_scaled_image("images/bunny2.png", scale_factor)
bunny_profile = load_scaled_image("images/bunnyicon1.png", 0.4)
bunny_profile_interact = load_scaled_image("images/bunnyicon2.png", 0.4)

dog = load_scaled_image("images/dog1.png", scale_factor)
dog_interact = load_scaled_image("images/dog2.png", scale_factor)
dog_profile = load_scaled_image("images/dogicon1.png", 0.4)
dog_profile_interact = load_scaled_image("images/dogicon2.png", 0.4)

fish = load_scaled_image("images/fish1.png", scale_factor)
fish_interact = load_scaled_image("images/fish2.png", scale_factor)
fish_profile = load_scaled_image("images/fishicon1.png", 0.4)
fish_profile_interact = load_scaled_image("images/fishicon2.png", 0.4)

hampy = load_scaled_image("images/hamp1.png", scale_factor)
hampy_interact = load_scaled_image("images/hamp2.png", scale_factor)
hampy_profile = load_scaled_image("images/hampicon1.png", 0.4)
hampy_profile_interact = load_scaled_image("images/hampyicon2.png", 0.4)

class Pet:
    #the parent class for all the pet.
    def __init__(self, name, pet_type, image, interact_image, profile_image, profile_interact_image):
        self.name = name
        self.pet_type = pet_type
        self.image = image
        self.interact_image = interact_image
        self.profile_image = profile_image
        self.profile_interact_image = profile_interact_image
        self.custom_name = name.capitalize()  
        self.mood = "happy"
        self.last_interaction = datetime.now()
    
    def get_motivational_messages(self):
        #the children class get these motivational messages, and personalised ones based on the pet they are
        base_messages = [
            f"You're doing great, {self.custom_name} believes in you!",
            f"{self.custom_name} is cheering you on!",
            "One task at a time!",
            "You've got this!",
            f"{self.custom_name} is proud of your progress!",
            "Keep up the good work!",
            f"Every task completed makes {self.custom_name} happier!",
            "You're making amazing progress!"
        ]
        return base_messages
    
    def get_encouragements(self):
        #when the pet is clicked, the pet gives an encouraging message to enourage them into completing the task
        base_encouragements = [
            f"{self.custom_name} thinks you're doing amazing!",
            "Keep up the great work!",
            f"{self.custom_name} believes in you!",
            "One task at a time!",
            "You've got this!",
            "Stay focused!",
            f"{self.custom_name} is cheering for you!"
        ]
        return base_encouragements
    
    def get_celebrations(self):
        #when a task is completed, the pet congragulates the user for finishing 
        base_celebrations = [
            f"Great job! {self.custom_name} is so proud!",
            f"Your pet {self.custom_name} is celebrating with you!",
            "Task complete! You're amazing!",
            "Another task done! Keep going!",
            f"{self.custom_name} is inspired by your productivity!"
        ]
        return base_celebrations

class Cat(Pet): #one of the child classes, the cat in particular
    def __init__(self):
        super().__init__("cat", "playful", cat, cat_interact, cat_profile, cat_profile_interact)
    
    def get_motivational_messages(self):
        base_messages = super().get_motivational_messages()
        cat_messages = [
            f"Meow! {self.custom_name} knows you can do it!",
            f"Purr-fect work so far, {self.custom_name} approves!",
            f"Your feline friend {self.custom_name} believes in you!",
            f"Keep chasing those tasks like {self.custom_name} chases toys!",
            f"You're the cat's meow, {self.custom_name} says!"
        ]
        return base_messages + cat_messages
    
    def get_encouragements(self):
        base_encouragements = super().get_encouragements()
        cat_encouragements = [
            f"Purr... {self.custom_name} thinks you're doing great!",
            f"Meow! {self.custom_name} says stay focused!",
            f"{self.custom_name} is purring with pride!"
        ]
        return base_encouragements + cat_encouragements

class Bunny(Pet): #another child class, the bunny
    def __init__(self):
        super().__init__("bunny", "energetic", bunny, bunny_interact, bunny_profile, bunny_profile_interact)
    
    def get_motivational_messages(self):
        base_messages = super().get_motivational_messages()
        bunny_messages = [
            f"Hop to it! {self.custom_name} knows you've got this!",
            f"{self.custom_name} is bouncing with excitement for you!",
            f"Keep hopping through those tasks with {self.custom_name}!",
            f"You're moving faster than {self.custom_name} on a carrot hunt!",
            f"Your energetic friend {self.custom_name} believes in you!"
        ]
        return base_messages + bunny_messages
    
    def get_encouragements(self):
        base_encouragements = super().get_encouragements()
        bunny_encouragements = [
            f"Hop hop! {self.custom_name} says you're doing great!",
            f"{self.custom_name} is doing happy jumps for you!",
            f"Keep that {self.custom_name} energy going!"
        ]
        return base_encouragements + bunny_encouragements

class Dog(Pet): #another child class, the dog
    def __init__(self):
        super().__init__("dog", "loyal", dog, dog_interact, dog_profile, dog_profile_interact)
    
    def get_motivational_messages(self):
        base_messages = super().get_motivational_messages()
        dog_messages = [
            f"Woof! {self.custom_name} thinks you're the best!",
            f"Your loyal companion {self.custom_name} believes in you!",
            f"Good human! {self.custom_name} says keep going!",
            f"You're fetching those tasks like {self.custom_name} fetches balls!",
            f"{self.custom_name} is wagging their tail for you!"
        ]
        return base_messages + dog_messages
    
    def get_encouragements(self):
        base_encouragements = super().get_encouragements()
        dog_encouragements = [
            f"Woof woof! {self.custom_name} thinks you're amazing!",
            f"{self.custom_name} is so proud of you!",
            f"Good human! {self.custom_name} says keep it up!"
        ]
        return base_encouragements + dog_encouragements

class Fish(Pet): #another child class, the fish
    def __init__(self):
        super().__init__("fish", "calm", fish, fish_interact, fish_profile, fish_profile_interact)
    
    def get_motivational_messages(self):
        base_messages = super().get_motivational_messages()
        fish_messages = [
            f"Just keep swimming! {self.custom_name} knows you've got this!",
            f"{self.custom_name} is calmly watching your progress!",
            f"Stay calm and focused like your friend {self.custom_name}!",
            f"You're making waves with {self.custom_name} cheering you on!",
            f"Your aquatic friend {self.custom_name} believes in you!"
        ]
        return base_messages + fish_messages
    
    def get_encouragements(self):
        base_encouragements = super().get_encouragements()
        fish_encouragements = [
            f"Blub blub! {self.custom_name} says you're doing swimmingly!",
            f"{self.custom_name} is doing happy circles for you!",
            f"Stay calm and keep going with {self.custom_name}!"
        ]
        return base_encouragements + fish_encouragements

class Hamster(Pet): #final child class, the hamster
    def __init__(self):
        super().__init__("hamster", "curious", hampy, hampy_interact, hampy_profile, hampy_profile_interact)
    
    def get_motivational_messages(self):
        base_messages = super().get_motivational_messages()
        hamster_messages = [
            f"Keep running on that wheel of productivity with {self.custom_name}!",
            f"Your curious hamster {self.custom_name} is excited for you!",
            f"You're storing up accomplishments like {self.custom_name} stores food!",
            f"Your little friend {self.custom_name} is cheering you on!",
            f"Stay curious and keep exploring those tasks with {self.custom_name}!"
        ]
        return base_messages + hamster_messages
    
    def get_encouragements(self):
        base_encouragements = super().get_encouragements()
        hamster_encouragements = [
            f"Squeak squeak! {self.custom_name} says you're doing great!",
            f"{self.custom_name} is running excitedly for you!",
            f"Stay curious and keep going with {self.custom_name}!"
        ]
        return base_encouragements + hamster_encouragements

class VirtualPet:
    def __init__(self, parent):
        self.parent = parent
        self.current_pet = None
        self.last_interaction = datetime.now()
        
        # Create pet instances
        self.pets = {
            "cat": Cat(),
            "bunny": Bunny(),
            "dog": Dog(),
            "fish": Fish(),
            "hamster": Hamster()
        } 
        # Create main container for virtual pet, making sure it only covers 1/3 of the screen
        self.main_frame = tk.Frame(parent, bg='#2b2d42', relief='raised', borderwidth=2)
        # Load pet stats, in particular the name
        self.load_pet_stats()
        #the selection screen at the start, that needs to cover the whole screen
        self.show_selection_screen_full()
    
    def load_pet_stats(self):
        #the pet stats that have been saved in a json file, in particular the name
        try:
            if os.path.exists("pet_stats.json"):
                with open("pet_stats.json", "r") as f:
                    stats = json.load(f)
                    pet_name = stats.get("current_pet")
                    if pet_name in self.pets:
                        self.current_pet = self.pets[pet_name]
                        # Load custom names for all pets
                        pets_data = stats.get("pets", {})
                        for species, pet_data in pets_data.items():
                            if species in self.pets:
                                self.pets[species].custom_name = pet_data.get("custom_name", species.capitalize())
        except Exception as e:
            print(f"Error loading pet stats: {e}")
    
    def save_pet_stats(self):
        #saving the pet name into a json file for future reference
        try:
            pets_data = {}
            for species, pet in self.pets.items():
                pets_data[species] = {
                    "custom_name": pet.custom_name
                }
            stats = {
                "current_pet": self.current_pet.name if self.current_pet else None,
                "pets": pets_data
            }
            with open("pet_stats.json", "w") as f:
                json.dump(stats, f, indent=4)
        except Exception as e:
            print(f"Error saving pet stats: {e}")
    
    def show_selection_screen_full(self):
        #show the pet selection screen that needs to fill the entire screen
        self.main_frame.pack_forget()
        # Get current background color from kanban settings if user has changed the colors
        bg_color = "#42484B"  # Default colors
        text_color = "#edf2f4"  # Default colors
        # Creating the full-screen selection frame
        self.selection_frame = tk.Frame(self.parent, bg=bg_color)
        self.selection_frame.pack(fill=tk.BOTH, expand=True)
        # Creating the selection screen
        selection_label = tk.Label(self.selection_frame, text="Choose Your Motivation Pet!", 
                                  font=("Arial", 24, "bold"), bg=bg_color, fg=text_color)
        selection_label.pack(pady=40)
        instruction_label = tk.Label(self.selection_frame, 
                                   text="Your pet will cheer you on as you complete tasks!",
                                   font=("Arial", 14), bg=bg_color, fg=text_color)
        instruction_label.pack(pady=(0, 40))
        #creating the frame for pet profiles
        profiles_frame = tk.Frame(self.selection_frame, bg=bg_color)
        profiles_frame.pack(pady=30)
        #creating the pet selection buttons
        self.profile_buttons = {}
        #making all the pets be in a neat row
        for i, (pet_name, pet) in enumerate(self.pets.items()):
            #create a frame for each pet
            pet_frame = tk.Frame(profiles_frame, bg=bg_color)
            pet_frame.grid(row=0, column=i, padx=20)
            #create profile button with border
            btn = tk.Label(pet_frame, image=pet.profile_image, cursor="hand2", 
                          bg=bg_color, relief='raised', borderwidth=3)
            btn.pack()
            # binding the mouse events for hover effect when the user hovers over the pet profile
            btn.bind("<Enter>", lambda e, p=pet_name: self.on_profile_hover(p, True))
            btn.bind("<Leave>", lambda e, p=pet_name: self.on_profile_hover(p, False))
            btn.bind("<Button-1>", lambda e, p=pet_name: self.select_pet(p))
            # pet name and type
            name_label = tk.Label(pet_frame, text=pet.custom_name, 
                                 font=("Arial", 12, "bold"), bg=bg_color, fg=text_color)
            name_label.pack(pady=(10, 2))
            
            type_label = tk.Label(pet_frame, text=f"({pet.pet_type})", 
                                 font=("Arial", 10), bg=bg_color, fg=text_color)
            type_label.pack(pady=(0, 5))
            
            self.profile_buttons[pet_name] = btn
    
    def on_profile_hover(self, pet_name, is_hovering):
        #the profile change after the mouse hovers over the pet
        pet = self.pets[pet_name]
        if is_hovering:
            self.profile_buttons[pet_name].config(
                image=pet.profile_interact_image
            )
        else:
            self.profile_buttons[pet_name].config(
                image=pet.profile_image
            )
    
    def select_pet(self, pet_name):
        #selecting the pet and destroying the selection screen to show the kanban board and calendar
        pet = self.pets[pet_name]
        #asks user for pet's name
        while True:
            custom_name = simpledialog.askstring(
                "Name Your Pet", 
                f"Enter a name for your {pet_name}:",
                initialvalue=pet.custom_name
            )
            #if user cancels, break and keep current name
            if custom_name is None:
                break  
            #if user enters nothing, show error and ask again
            if not custom_name.strip():
                messagebox.showerror("Error", "Pet name cannot be empty. Please enter a name.")
                continue    
            pet.custom_name = custom_name.strip()
            break
        self.current_pet = pet
        self.save_pet_stats()
        #destroying the full screen selection 
        self.selection_frame.destroy()
        #the main application with kanban board, calendar and virtual pet appears
        self.show_main_application()
    
    def show_main_application(self):
        #making sure the virtual pet is on 1/3 of the screen and on the left
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        #making sure the kanban board and calendar is filling 2/3 of the screen and on the right
        self.kanban_board = KanbanBoard(self.parent, self)
        self.kanban_board.show()
        #ensuring that the pet background is the same color as the kanban board/calendar background
        self.update_pet_background()
        #show the pet screen
        self.show_pet_screen()
    
    def update_pet_background(self):
        #ensuring that the pet background color is the same as the kanban board background color.
        if hasattr(self, 'kanban_board'):
            kanban_bg = self.kanban_board.settings["colors"]["background"]
            self.main_frame.configure(bg=kanban_bg)
            if self.current_pet:
                self.refresh_pet_screen()
    
    def refresh_pet_screen(self):
        #refresh the pet screen to ensure the color is correct
        if self.current_pet:
            self.show_pet_screen()
    
    def show_pet_screen(self):
        #clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        #get background color from kanban board
        bg_color = self.kanban_board.settings["colors"]["background"]
        text_color = self.kanban_board.settings["colors"]["text"]
        #create a header with back button and name change button
        header_frame = tk.Frame(self.main_frame, bg=bg_color)
        header_frame.pack(fill=tk.X, pady=8)
        back_btn = tk.Button(header_frame, text="← Change Pet", 
                            command=self.return_to_selection,
                            font=("Arial", 10), bg=bg_color, fg=text_color,
                            relief="flat", activebackground=bg_color, activeforeground=text_color)
        back_btn.pack(side=tk.LEFT, padx=10)
        # the pet name shows up with an edit button so the user can edit the pet's name
        name_frame = tk.Frame(header_frame, bg=bg_color)
        name_frame.pack(side=tk.RIGHT, padx=10)
        name_label = tk.Label(name_frame, text=self.current_pet.custom_name, 
                             font=("Arial", 14, "bold"), bg=bg_color, fg=text_color)
        name_label.pack(side=tk.LEFT)
        edit_name_btn = tk.Button(name_frame, text="✏️", 
                                 command=self.change_pet_name,
                                 font=("Arial", 10), bg=bg_color, fg=text_color,
                                 relief="flat", activebackground=bg_color, activeforeground=text_color)
        edit_name_btn.pack(side=tk.LEFT, padx=(5, 0))
        #create the main content area
        content_frame = tk.Frame(self.main_frame, bg=bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        #create the pet display with a border
        pet_display_frame = tk.Frame(content_frame, borderwidth=3, relief="sunken", bg=bg_color)
        pet_display_frame.pack(expand=True, pady=10)
        self.pet_display = tk.Label(pet_display_frame, 
                                   image=self.current_pet.image,
                                   cursor="hand2", bg=bg_color)  # ensuring it matches the background color
        self.pet_display.pack(padx=10, pady=10)
        #bind the click event to pet image
        self.pet_display.bind("<Button-1>", self.on_pet_click)
        # making the frame for the motivational messages
        motivation_frame = tk.Frame(content_frame, bg=bg_color)
        motivation_frame.pack(fill=tk.X, pady=15)
        #the design of the motivational messages at the bottom
        self.motivation_label = tk.Label(motivation_frame, 
                                        text=random.choice(self.current_pet.get_motivational_messages()),
                                        font=("Arial", 12, "italic"), 
                                        bg=bg_color, fg=text_color,
                                        wraplength=300)
        self.motivation_label.pack()
        status_frame = tk.Frame(content_frame, bg=bg_color)
        status_frame.pack(pady=10)
        #telling the user that the pet is interactable
        tk.Label(status_frame, text=f"Click {self.current_pet.custom_name} for encouragement!", 
                font=("Arial", 10), bg=bg_color, fg=text_color).pack()
        #updates the motivational message periodically so it's not always on the same message
        self.update_motivational_message()
    
    def change_pet_name(self):
        #change the pet's current name into something else
        if not self.current_pet:
            return
        while True:
            new_name = simpledialog.askstring(
                "Change Pet Name", 
                f"Enter a new name for {self.current_pet.custom_name}:",
                initialvalue=self.current_pet.custom_name
            )
            #if user cancels, the screen gets destroyed and keeps the old name
            if new_name is None:
                break
            #if the user enters an empty space, an error message shows up
            if not new_name.strip():
                messagebox.showerror("Error", "Pet name cannot be empty. Please enter a name.")
                continue
            #if no error occurs, the name is changed into the new name
            self.current_pet.custom_name = new_name.strip()
            self.save_pet_stats()
            self.refresh_pet_screen()  #refreshes to ensure that the pet has the correct name
            break
    
    def return_to_selection(self):
        #return to the main menu screen
        self.main_frame.pack_forget()#hide the main application screen (kanban board, calendar, virtual pet)
        if hasattr(self, 'kanban_board'):
            # Hide both kanban board and calendar view
            self.kanban_board.main_frame.pack_forget()
            self.kanban_board.calendar_view.hide()  # Ensure calendar is also hidden
        #show the full-screen selection with the pet menu
        self.show_selection_screen_full()
    
    def update_motivational_message(self):
        #periodically updating the motivational message so it's not on the same thing all the time
        if self.current_pet:
            new_message = random.choice(self.current_pet.get_motivational_messages())
            self.motivation_label.config(text=new_message)
        #updates every 30 seconds to not feel bland
        self.parent.after(30000, self.update_motivational_message)
    
    def on_pet_click(self, event):
        #the pet interaction when clicked
        if not self.current_pet:
            return      
        # changes into the interactive image
        self.pet_display.config(
            image=self.current_pet.interact_image
        )
        #the encouragement image shows up alongside an encouraging message
        encouragements = self.current_pet.get_encouragements()
        self.motivation_label.config(text=random.choice(encouragements), fg='#e74c3c')
        #the image returns back to normal afterwards
        self.parent.after(500, self.revert_pet_image)
    
    def revert_pet_image(self):
        #changes pet image back to original state
        if self.current_pet:
            self.pet_display.config(
                image=self.current_pet.image
            )
    
    def task_completed(self):
        #when task is complete, the task is called
        if not self.current_pet:
            return
        #update motivational message for completing task
        celebrations = self.current_pet.get_celebrations()
        if hasattr(self, 'motivation_label'):
            self.motivation_label.config(text=random.choice(celebrations), fg='#27ae60')
        # updates and saves the new stats
        self.save_pet_stats()

class Task: #the task class with the info
    def __init__(self, content, due_date=None, priority="medium"):
        self.content = content
        self.due_date = due_date
        self.priority = priority
        self.id = id(self)
    
    def to_dict(self):
        #converts task to dictionary for JSON serialization
        return {
            "content": self.content,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "id": self.id
        }
    
    @classmethod
    def from_dict(cls, data):
        #creates task from dictionary
        due_date = datetime.fromisoformat(data["due_date"]).date() if data["due_date"] else None
        task = cls(data["content"], due_date, data["priority"])
        task.id = data["id"]
        return task

class CalendarView:
    #the calendar class that shows the calendar view with all the tasks
    def __init__(self, parent, kanban_board):
        self.parent = parent
        self.kanban_board = kanban_board
        #create the main calendar frame
        self.main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        #calendar state
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
    
    def show(self):
        #show the calendar by packing the main frame
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.update_calendar()
    
    def hide(self):
        #hide the calendar
        self.main_frame.pack_forget()
    
    def update_calendar(self):
        #update the calendar display with current tasks
        #clear the calendar frame first
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Add toggle button for calendar view
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
        
        #create calendar header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill=tk.X, pady=10)
        
        #previous month button
        prev_btn = ctk.CTkButton(
            header_frame,
            text="◀ Previous",
            font=self.kanban_board.get_font("bold"),
            command=lambda: self.change_calendar_month(-1),
            fg_color="#4cc9f0",
            hover_color="#3a97b8"
        )
        prev_btn.pack(side=tk.LEFT, padx=10)
        
        #month and year label
        month_label = ctk.CTkLabel(
            header_frame,
            text=f"{month_name[self.current_month]} {self.current_year}",
            font=self.kanban_board.get_font("bold", 20),
            text_color="black"  # Changed to black for better visibility
        )
        month_label.pack(side=tk.LEFT, expand=True)
        
        #next month button
        next_btn = ctk.CTkButton(
            header_frame,
            text="Next ▶",
            font=self.kanban_board.get_font("bold"),
            command=lambda: self.change_calendar_month(1),
            fg_color="#4cc9f0",
            hover_color="#3a97b8"
        )
        next_btn.pack(side=tk.RIGHT, padx=10)
        
        #create days of week header
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
        
        #create calendar grid
        calendar_grid = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        calendar_grid.pack(fill=tk.BOTH, expand=True, pady=10)
        
        #get number of days in month and first weekday
        num_days = monthrange(self.current_year, self.current_month)[1]
        first_weekday = monthrange(self.current_year, self.current_month)[0]
        
        #get all tasks with due dates
        all_tasks = []
        for status in ["todo", "doing", "done"]:
            all_tasks.extend(self.kanban_board.tasks[status])
        
        #group tasks by due date
        tasks_by_date = {}
        for task in all_tasks:
            if task.due_date:
                #check if task due date falls in current month
                if (task.due_date.year == self.current_year and 
                    task.due_date.month == self.current_month):
                    date_str = task.due_date.strftime("%Y-%m-%d")
                    if date_str not in tasks_by_date:
                        tasks_by_date[date_str] = []
                    tasks_by_date[date_str].append(task)
        
        #create empty cells for days before the first day of the month
        row = 0
        col = 0
        for i in range(first_weekday):
            empty_cell = ctk.CTkFrame(calendar_grid, width=140, height=120, fg_color="transparent")
            empty_cell.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
        
        #create cells for each day of the month
        today = datetime.now().date()
        
        for day in range(1, num_days + 1):
            if col > 6:
                col = 0
                row += 1
            
            #create day cell
            cell_bg = "#edf2f4"
            cell_date = datetime(self.current_year, self.current_month, day).date()
            
            #highlight today
            if (cell_date == today and 
                self.current_month == today.month and 
                self.current_year == today.year):
                cell_bg = "#ffe66d"  #yellow highlight for today
            
            cell = ctk.CTkFrame(calendar_grid, width=140, height=120, 
                               corner_radius=10, border_width=2,
                               border_color="#8d99ae", fg_color=cell_bg)
            cell.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            #day number
            day_label = ctk.CTkLabel(
                cell,
                text=str(day),
                font=self.kanban_board.get_font("bold", 14),
                text_color="black"  # Changed to black for better visibility
            )
            day_label.place(x=5, y=5)
            
            #check if this day has tasks
            date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
            if date_str in tasks_by_date:
                tasks = tasks_by_date[date_str]
                
                #show task count
                count_label = ctk.CTkLabel(
                    cell,
                    text=f"{len(tasks)} task(s)",
                    font=self.kanban_board.get_font(size=10),
                    text_color="black"  # Changed to black for better visibility
                )
                count_label.place(x=5, y=30)
                
                #show task preview (first task only)
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
        
        #configure grid weights for proper resizing
        for i in range(7):
            calendar_grid.columnconfigure(i, weight=1)
        for i in range(6):  #maximum 6 rows in a month
            calendar_grid.rowconfigure(i, weight=1)
    
    def change_calendar_month(self, delta):
        #change the calendar month by delta (-1 for previous, 1 for next)
        self.current_month += delta
        
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        
        self.update_calendar()

class KanbanBoard: #the kanban board class with all the information within
    def __init__(self, parent, virtual_pet):
        self.root = parent
        self.virtual_pet = virtual_pet
        
        # Create main container for Kanban board (2/3 of width)
        self.main_frame = tk.Frame(parent)
        
        # Default settings
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
        
        # Apply initial settings
        self.apply_settings()
        
        # Now create the rest of the UI components
        self.create_menu()
        self.create_view_toggle()
        
        # Create frames
        self.todo_frame = self.create_frame("To-Do", 0, self.settings["colors"]["todo"])
        self.doing_frame = self.create_frame("Doing", 1, self.settings["colors"]["doing"])
        self.done_frame = self.create_frame("Done", 2, self.settings["colors"]["done"])
        
        # Create input area
        self.create_input_area()
        
        # Create calendar instance
        self.calendar_view = CalendarView(parent, self)
        
        # Store tasks
        self.tasks = {
            "todo": [],
            "doing": [],
            "done": []
        }
        
        # Load saved tasks
        self.load_tasks()
        
    def show(self):
        """Show the kanban board"""
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_view_toggle(self):
        """Create a button to toggle between Kanban and Calendar views"""
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
        """Toggle between Kanban and Calendar views"""
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
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
        
        # Task input
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
        
        # Due date input
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
        self.main_frame.config(bg=self.settings["colors"]["background"])
        
        # Update theme for customtkinter
        ctk.set_appearance_mode("dark" if self.is_dark_color(self.settings["colors"]["background"]) else "light")
        
        # Update virtual pet background
        if hasattr(self, 'virtual_pet'):
            self.virtual_pet.update_pet_background()
        
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
        
        # Save tasks to JSON
        self.save_tasks()
    
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
            
            # Update calendar if it's visible
            if hasattr(self.calendar_view, 'main_frame') and self.calendar_view.main_frame.winfo_ismapped():
                self.calendar_view.update_calendar()
            
            # Save tasks to JSON
            self.save_tasks()
            
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
        
        # Notify virtual pet when task is moved to done
        if to_column == "done" and from_column != "done":
            self.virtual_pet.task_completed()
        
        # Update calendar if it's visible
        if hasattr(self.calendar_view, 'main_frame') and self.calendar_view.main_frame.winfo_ismapped():
            self.calendar_view.update_calendar()
        
        # Save tasks to JSON
        self.save_tasks()
    
    def delete_task(self, task, column):
        self.tasks[column].remove(task)
        task.widget.destroy()
        
        # Update calendar if it's visible
        if hasattr(self.calendar_view, 'main_frame') and self.calendar_view.main_frame.winfo_ismapped():
            self.calendar_view.update_calendar()
        
        # Save tasks to JSON
        self.save_tasks()
    
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
        #load settings that have been set from previous times (such as color, font size)
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
    
    def load_tasks(self):
        #Load previously written tasks from JSON file
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
                                    # Create the task widget
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
        #Save tasks to JSON file
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

# Create the virtual pet application
try:
    virtual_pet = VirtualPet(root)
    print("Application started successfully")
except Exception as e:
    print(f"Error starting application: {e}")
    messagebox.showerror("Error", f"Failed to start application: {e}")

# Start the application
root.mainloop()
