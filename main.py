import tkinter as tk
from tkinter import messagebox, scrolledtext
import errors

class ErrorCalculationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Error Calculations")

        self.stats_frame = tk.LabelFrame(self.root, text="Calculate Stats with Delta")
        self.stats_frame.pack(padx=10, pady=5, fill="x")

        self.create_stats_widgets()

        self.error_frame = tk.LabelFrame(self.root, text="Calculate Error with Propagation")
        self.error_frame.pack(padx=10, pady=5, fill="x")

        self.create_error_widgets()

    def create_stats_widgets(self):
        tk.Label(self.stats_frame, text="Numbers (comma-separated):").grid(row=0, column=0, sticky="w")
        self.stats_numbers_entry = tk.Entry(self.stats_frame, width=50)
        self.stats_numbers_entry.grid(row=0, column=1)

        tk.Label(self.stats_frame, text="Variable Name:").grid(row=1, column=0, sticky="w")
        self.stats_varname_entry = tk.Entry(self.stats_frame)
        self.stats_varname_entry.grid(row=1, column=1)

        tk.Label(self.stats_frame, text="Variable Unit:").grid(row=2, column=0, sticky="w")
        self.stats_unit_entry = tk.Entry(self.stats_frame)
        self.stats_unit_entry.grid(row=2, column=1)

        tk.Label(self.stats_frame, text="Delta M:").grid(row=3, column=0, sticky="w")
        self.stats_delta_m_entry = tk.Entry(self.stats_frame)
        self.stats_delta_m_entry.grid(row=3, column=1)

        self.stats_calculate_button = tk.Button(self.stats_frame, text="Calculate Stats", command=self.calculate_stats)
        self.stats_calculate_button.grid(row=4, column=1, pady=5)

        self.stats_result_text = scrolledtext.ScrolledText(self.stats_frame, height=10, width=60)
        self.stats_result_text.grid(row=5, column=0, columnspan=2, pady=5)

    def create_error_widgets(self):
        tk.Label(self.error_frame, text="Formula:").grid(row=0, column=0, sticky="w")
        self.error_formula_entry = tk.Entry(self.error_frame, width=50)
        self.error_formula_entry.grid(row=0, column=1)

        tk.Label(self.error_frame, text="Calculated Variable:").grid(row=1, column=0, sticky="w")
        self.error_calculated_variable_entry = tk.Entry(self.error_frame, width=50)
        self.error_calculated_variable_entry.grid(row=1, column=1)

        tk.Label(self.error_frame, text="Calculated Variable Unit: ").grid(row=2, column=0, sticky="w")
        self.error_calculated_variable_unit_entry = tk.Entry(self.error_frame, width=50)
        self.error_calculated_variable_unit_entry.grid(row=2, column=1)

        tk.Label(self.error_frame, text="Variables (name=value, comma-separated):").grid(row=3, column=0, sticky="w")
        self.variables_entry = tk.Entry(self.error_frame, width=50)
        self.variables_entry.grid(row=3, column=1)

        tk.Label(self.error_frame, text="Errors (variable=value, comma-separated):").grid(row=4, column=0, sticky="w")
        self.errors_entry = tk.Entry(self.error_frame, width=50)
        self.errors_entry.grid(row=4, column=1)

        self.error_calculate_button = tk.Button(self.error_frame, text="Calculate Error", command=self.calculate_error)
        self.error_calculate_button.grid(row=5, column=1, pady=5)

        self.error_result_text = scrolledtext.ScrolledText(self.error_frame, height=10, width=60)
        self.error_result_text.grid(row=6, column=0, columnspan=2, pady=5)

    def calculate_stats(self):
        try:
            numbers = list(map(float, self.stats_numbers_entry.get().split(',')))
            var_name = self.stats_varname_entry.get()
            unit = self.stats_unit_entry.get()
            delta_m = float(self.stats_delta_m_entry.get())
            result = errors.calculate_stats_with_delta(numbers, var_name, delta_m, unit)
            self.stats_result_text.delete(1.0, tk.END)
            self.stats_result_text.insert(tk.END, result)
            self.stats_result_text.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def calculate_error(self):
        try:
            formula = self.error_formula_entry.get()
            calculated_variable = self.error_calculated_variable_entry.get()
            unit = self.error_calculated_variable_unit_entry.get()
            variables = {var.split('=')[0].strip(): float(var.split('=')[1].strip())
                         for var in self.variables_entry.get().split(',')}
            errors_dict = {err.split('=')[0].strip(): float(err.split('=')[1].strip())
                           for err in self.errors_entry.get().split(',')}
            value, delta, result = errors.calculate_error_with_propagation(formula, calculated_variable, variables, errors_dict, unit)
            self.error_result_text.delete(1.0, tk.END)
            self.error_result_text.insert(tk.END, result)
            self.error_result_text.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ErrorCalculationApp(root)
    root.mainloop()