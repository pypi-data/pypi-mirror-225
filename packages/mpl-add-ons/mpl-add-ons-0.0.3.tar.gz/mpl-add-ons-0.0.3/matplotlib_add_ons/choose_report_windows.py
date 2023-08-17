from tkinter import filedialog
from matplotlib.backends.backend_pdf import PdfPages
import tkinter as tk


class ChooseReportWindows:
    def __init__(self, figures):
        root = tk.Tk()
        root.title("Save Report")
        self.figures = figures
        self.num_checkboxes = len(figures)
        self.selected_values = []
        self.save_location = None
        # create the checkbox widgets
        self.checkboxes = []
        for i in range(self.num_checkboxes):
            var = tk.IntVar(value=1)
            checkbox = tk.Checkbutton(root, text=f"Window {i + 1}", variable=var)
            checkbox.grid(row=i + 1, column=0, sticky='w', padx=10)
            self.checkboxes.append(var)

        # create the save location label and entry box
        save_location_label = tk.Label(root, text="Save Location:")
        save_location_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.save_location_entry = tk.Entry(root)
        self.save_location_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # create the Save As button
        save_button = tk.Button(root, text="Choose Save Location", command=self.choose_save_location)
        save_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        # create the submit button
        submit_button = tk.Button(root, text="Save", command=self.submit)
        submit_button.grid(row=self.num_checkboxes + 1, column=0, columnspan=2, pady=10)

        # create the cancel button
        cancel_button = tk.Button(root, text="Exit Widget", command=root.destroy)
        cancel_button.grid(row=self.num_checkboxes + 1, column=1, columnspan=2, pady=10)
        root.mainloop()

    def choose_save_location(self):
        file_path = filedialog.asksaveasfilename(title="Choose Save Location", defaultextension=".pdf",
                                                 filetypes=(("Pdf", "*.pdf"), ("All Files", "*.*")))
        if file_path:
            self.save_location_entry.delete(0, 'end')
            self.save_location_entry.insert(0, file_path)

    def submit(self):
        # get the values of the selected checkboxes
        self.selected_values = []
        for i in range(self.num_checkboxes):
            if self.checkboxes[i].get() == 1:
                self.selected_values.append(i + 1)

        # get the save location
        self.save_location = self.save_location_entry.get()
        self.save_figures(self.save_location, self.selected_values)

    def save_figures(self, file_path, selected_figures):
        # Create a PDF file and save the figures in it
        if file_path and len(selected_figures) != 0:
            with PdfPages(file_path) as pdf:
                for i, figure in enumerate(self.figures):
                    if i + 1 in selected_figures:
                        pdf.savefig(figure)
            print(f"Report Saved to location: {file_path}")
        else:
            print("Could not save due to missing save location or no windows selected.")


if __name__ == '__main__':
    pass