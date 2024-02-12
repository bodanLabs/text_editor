import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class TextEditor:
    def __init__(self, root):
        # Main window
        self.root = root
        self.root.title("Simple Text Editor")
        
        # Text area with undo functionality
        self.textArea = tk.Text(root, undo=True)
        self.textArea.pack(fill=tk.BOTH, expand=1)
        
        # Variable to keep track of the current file name
        self.filename = None
        
        # Menu
        self.create_menu()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()

    def create_menu(self):
        # Create a menu bar
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Add File menu with commands
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_editor)
        
        # Add Edit menu with commands
        edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=lambda: self.textArea.edit_undo())
        edit_menu.add_command(label="Search", command=self.search_text)

    def bind_shortcuts(self):
        # Bind shortcuts for various actions
        self.textArea.bind('<Control-n>', self.new_file)
        self.textArea.bind('<Control-o>', self.open_file)
        self.textArea.bind('<Control-s>', self.save_file)
        self.textArea.bind('<Control-z>', lambda event: self.textArea.edit_undo())
        self.textArea.bind('<Control-f>', self.search_text)

    def new_file(self, event=None):
        # Clear the text area to start a new file
        self.textArea.delete(1.0, tk.END)
        self.filename = None

    def open_file(self, event=None):
        # Open an existing file
        self.filename = filedialog.askopenfilename(defaultextension=".txt",
                                                   filetypes=[("All Files", "*.*"),
                                                              ("Text Documents", "*.txt")])
        if self.filename:
            self.root.title(f"Simple Text Editor - {self.filename}")
            self.textArea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textArea.insert(1.0, f.read())

    def save_file(self, event=None):
        # Save the current file
        if not self.filename:
            # Ask for file name if not saved before
            self.filename = filedialog.asksaveasfilename(initialfile='Untitled.txt',
                                                         defaultextension=".txt",
                                                         filetypes=[("All Files", "*.*"),
                                                                    ("Text Documents", "*.txt")])
        if self.filename:
            with open(self.filename, "w") as f:
                f.write(self.textArea.get(1.0, tk.END))
            self.root.title(f"Simple Text Editor - {self.filename}")

    def exit_editor(self):
        # Confirm before exiting the application
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def search_text(self, event=None):
        # Search and highlight text in the document
        search_query = simpledialog.askstring("Search", "Enter search text:")
        if search_query:
            start_pos = '1.0'
            while True:
                start_pos = self.textArea.search(search_query, start_pos, tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_query)}c"
                self.textArea.tag_add(tk.SEL, start_pos, end_pos)
                self.textArea.tag_config(tk.SEL, background='yellow')
                start_pos = end_pos
            # Remove selection to not interfere with user selection
            self.textArea.tag_remove(tk.SEL, '1.0', tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    TextEditor(root)
    root.mainloop()
