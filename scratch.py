import tkinter as tk

class ItemFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Item Filter App")

        self.items = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape']
        self.filtered_items = self.items.copy()

        self.listbox = tk.Listbox(root, width=30, height=10)
        self.listbox.pack()

        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(root, text="Show only items with more than 5 letters", variable=self.checkbox_var, command=self.update_list)
        self.checkbox.pack()

        self.populate_listbox(self.filtered_items)

    def populate_listbox(self, items):
        self.listbox.delete(0, tk.END)  # Clear the Listbox
        for item in items:
            self.listbox.insert(tk.END, item)

    def update_list(self):
        if self.checkbox_var.get():  # If checkbox is checked
            self.filtered_items = [item for item in self.items if len(item) > 5]  # Filter condition
        else:  # If checkbox is unchecked
            self.filtered_items = self.items.copy()  # Remove filters

        self.populate_listbox(self.filtered_items)

if __name__ == "__main__":
    root = tk.Tk()
    app = ItemFilterApp(root)
    root.mainloop()
