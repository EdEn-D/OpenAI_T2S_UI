import tkinter as tk
from tkinter import filedialog, ttk, messagebox, Canvas, Scrollbar, Frame
from tkinter import *
from os import getcwd
from t2s_logic import T2SConverter

# def get_sentences():
#     # Placeholder function that returns a list of sentences
#     return ["Sentence 1", "Sentence 2", "Sentence 3", "Sentence 1", "Sentence 2", "Sentence 3", "Sentence 1", "SenSentenceSentSentenceSentenceSentenceSentenceSentenceSentenceenceSentenceSentenceSentenceSentenceSentenceSentencetence 2", "Sentence 3","Sentence 1", "Sentence 2", "Sentence 3", "Sentence 1", "Sentence 2", "Sentence 3", ]


def select_file():
    file_types = [
        ('Excel files', '*.xlsx *.xls'),
        ('CSV files', '*.csv'),
        ('Text files', '*.txt')
    ]
    file_path = filedialog.askopenfilename(filetypes=file_types)
    if file_path:
        file_label.config(text=file_path)
        # Check if the selected file is an Excel file
        if file_path.endswith(('.xlsx', '.xls')):
            load_rows_into_ui(file_path)

checkboxes = []

# Called after file is selected, populates rows of the scrollable area
def load_rows_into_ui(file_path):
    global checkboxes
    checkboxes = []  # Reset the list for new file
    rows = T2SConverter.load_excel_rows(file_path)
    # Clear existing checkboxes
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Populate checkboxes with new rows
    for i, sentence in enumerate(rows):
        row_label = tk.Label(scrollable_frame, text=str(i + 1), bg="white")
        row_label.grid(row=i, column=0, sticky='w', padx=5)

        chk_var = IntVar()
        chk = tk.Checkbutton(scrollable_frame, text=sentence, bg="white", variable=chk_var)
        chk.grid(row=i, column=1, sticky='w', padx=5)
        chk.select()
        checkboxes.append(chk_var)  # Store the row number and checkbox variable
        #print(chk_var.get())


    # Resize the window after it's displayed
    current_width = root.winfo_width()
    current_height = root.winfo_height()
    new_width = current_width + 10
    new_height = current_height
    root.geometry(f"{new_width}x{new_height}")
    #root.geometry("810x450")


def callback_notification(message):
    # Update the UI here, e.g., show a message
    messagebox.showinfo("Notification", message)

def call_t2s_function():
    active_lines = []
    for i, c in enumerate(checkboxes):
        if c.get() == 1:
            active_lines.append(i +1)

    file_path = file_label.cget("text")
    output_dir = dir_label.cget("text")
    selected_option = combo_box.get()
    if file_path not in ["", "No file selected"]:
        converter = T2SConverter(file_path, output_dir, callback_notification)
        converter.process_rows(active_lines, selected_option)

    #     get_t2s_from_file(file_path, output_dir, selected_option, callback_notification)

def select_output_directory():
    directory = filedialog.askdirectory(initialdir=getcwd())
    directory = directory if directory else getcwd()
    dir_label.config(text=directory)

# Create the main window
root = tk.Tk()
root.title("File Selector with T2S")
root.geometry("800x450")

# Grid configuration for layout
root.columnconfigure(0, weight=1)  # Buttons column
root.columnconfigure(1, weight=3)  # Labels column

# Add a button to select a file
select_button = tk.Button(root, text="Select File", command=select_file)
select_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

# Label to display the selected file path
file_label = tk.Label(root, text="No file selected", anchor="w")
file_label.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

# Add a button to select the output directory
dir_button = tk.Button(root, text="Select Output Directory", command=select_output_directory)
dir_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

# Label to display the selected directory
dir_label = tk.Label(root, text=getcwd(), anchor="w")
dir_label.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

# Label for the dropdown menu
voice_label = tk.Label(root, text="Voice: ")
voice_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

# Dropdown Menu (Combobox)
combo_values = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
combo_box = ttk.Combobox(root, values=combo_values, state="readonly")
combo_box.current(0)  # Set the first item as the default selection
combo_box.grid(row=2, column=1, padx=10, pady=10, sticky='w')

##########################################scrollable area - start##########################################################
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def select_all_checkboxes():
    for widget in scrollable_frame.winfo_children():
        if isinstance(widget, tk.Checkbutton):
            widget.select()

def deselect_all_checkboxes():
    for widget in scrollable_frame.winfo_children():
        if isinstance(widget, tk.Checkbutton):
            widget.deselect()


# Scrollable area for checkboxes
canvas = Canvas(root,width=500)
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

# Bind the mousewheel event to the canvas
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Configure canvas and scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


# Add frame to canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Grid configuration for scrollable area
canvas.grid(row=3, column=0, sticky='ew')
scrollbar.grid(row=3, column=1, sticky='ns')

# Set the background color for the scrollable frame
scrollable_frame.config(bg="white")

select_all_button = tk.Button(root, text="Select All", command=select_all_checkboxes)
select_all_button.grid(row=4, column=0, padx=10, pady=10, sticky='ew')

deselect_all_button = tk.Button(root, text="Deselect All", command=deselect_all_checkboxes)
deselect_all_button.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

########################################scrollable area - end############################################################

# Add a button to perform T2S
t2s_button = tk.Button(root, text="Get T2S", command=call_t2s_function)
# t2s_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='s')
t2s_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky='e')

# Start the GUI event loop
root.mainloop()