import tkinter as tk
from tkinter import messagebox, scrolledtext
import errors
from plot import plot_with_error_bars


class ErrorCalculationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Error Calculations")

        self.file_frame = tk.LabelFrame(self.root, text="File Options")
        self.file_frame.pack(padx=10, pady=5, fill="x")
        self.create_file_var = tk.BooleanVar()
        self.create_file_checkbox = tk.Checkbutton(
            self.file_frame, text="Create File", variable=self.create_file_var, command=self.toggle_file_options
        )
        self.create_file_checkbox.grid(row=0, column=0, sticky="w")

        tk.Label(self.file_frame, text="File Name:").grid(row=1, column=0, sticky="w")
        self.file_name_entry = tk.Entry(self.file_frame, width=50, state=tk.DISABLED)
        self.file_name_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(self.file_frame, text="Prefix and endfix aren't mandatory\n they may found useful with latex extantions in docs which require $$ at the end and start").grid(row=2, column=0)

        tk.Label(self.file_frame, text="Prefix:").grid(row=3, column=0, sticky="w")
        self.file_prefix_entry = tk.Entry(self.file_frame, width=50, state=tk.DISABLED)
        self.file_prefix_entry.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(self.file_frame, text="Endfix:").grid(row=4, column=0, sticky="w")
        self.file_endfix_entry = tk.Entry(self.file_frame, width=50, state=tk.DISABLED)
        self.file_endfix_entry.grid(row=4, column=1, padx=5, pady=2)

        self.stats_frame = tk.LabelFrame(self.root, text="Calculate Stats with Delta")
        self.stats_frame.pack(padx=10, pady=5, fill="x")
        self.create_stats_widgets()

        self.error_frame = tk.LabelFrame(self.root, text="Calculate Error with Propagation")
        self.error_frame.pack(padx=10, pady=5, fill="x")
        self.create_error_widgets()

        self.n_sigma_frame = tk.LabelFrame(self.root, text="Calculate N-Sigma")
        self.n_sigma_frame.pack(padx=10, pady=5, fill="x")
        self.create_n_sigma_widgets()

        self.plot_frame = tk.LabelFrame(self.root, text="Plot Data with Error Bars")
        self.plot_frame.pack(padx=10, pady=5, fill="x")
        self.create_plot_widgets()

    def toggle_file_options(self):
        if self.create_file_var.get():
            self.file_name_entry.config(state=tk.NORMAL)
            self.file_prefix_entry.config(state=tk.NORMAL)
            self.file_endfix_entry.config(state=tk.NORMAL)
        else:
            self.file_name_entry.config(state=tk.DISABLED)
            self.file_prefix_entry.config(state=tk.DISABLED)
            self.file_endfix_entry.config(state=tk.DISABLED)

    def append_to_file(self, content, title=""):
        if not self.create_file_var.get():
            return
        file_name = self.file_name_entry.get().strip()
        prefix = self.file_prefix_entry.get()
        endfix = self.file_endfix_entry.get()

        if not file_name:
            messagebox.showerror("File Error", "File name is required to append content.")
            return

        try:
            with open(file_name, "a") as file:
                if title:
                    file.write(f"{title}\n")
                for line in content.split("\n"):
                    if line:
                        file.write(f"{prefix}{line}{endfix}\n")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not write to file: {e}")

    def create_stats_widgets(self):
        tk.Label(self.stats_frame, text="Numbers (comma-separated):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.stats_numbers_entry = tk.Entry(self.stats_frame, width=50)
        self.stats_numbers_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.stats_frame, text="Variable Name:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.stats_varname_entry = tk.Entry(self.stats_frame)
        self.stats_varname_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.stats_frame, text="Variable Unit:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.stats_unit_entry = tk.Entry(self.stats_frame)
        self.stats_unit_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.stats_frame, text="Delta M:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.stats_delta_m_entry = tk.Entry(self.stats_frame)
        self.stats_delta_m_entry.grid(row=3, column=1, padx=5, pady=2)

        self.stats_append_var = tk.BooleanVar()
        self.stats_append_checkbox = tk.Checkbutton(
            self.stats_frame, text="Append to File", variable=self.stats_append_var, command=self.toggle_stats_title
        )
        self.stats_append_checkbox.grid(row=4, column=0, sticky="w", padx=5, pady=2)

        tk.Label(self.stats_frame, text="Title:").grid(row=4, column=1, sticky="e", padx=5, pady=2)
        self.stats_title_entry = tk.Entry(self.stats_frame, width=50, state=tk.DISABLED)
        self.stats_title_entry.grid(row=4, column=2, padx=5, pady=2)

        self.stats_calculate_button = tk.Button(self.stats_frame, text="Calculate Stats", command=self.calculate_stats)
        self.stats_calculate_button.grid(row=5, column=1, pady=5)

        self.stats_result_text = scrolledtext.ScrolledText(self.stats_frame, height=10, width=70, state=tk.DISABLED)
        self.stats_result_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    def toggle_stats_title(self):
        if self.stats_append_var.get():
            self.stats_title_entry.config(state=tk.NORMAL)
        else:
            self.stats_title_entry.delete(0, tk.END)
            self.stats_title_entry.config(state=tk.DISABLED)

    def calculate_stats(self):
        try:
            numbers_str = self.stats_numbers_entry.get()
            if not numbers_str:
                raise ValueError("Please enter numbers.")
            numbers = list(map(float, numbers_str.split(',')))
            var_name = self.stats_varname_entry.get().strip()
            unit = self.stats_unit_entry.get().strip()
            delta_m_str = self.stats_delta_m_entry.get().strip()
            if not delta_m_str:
                raise ValueError("Please enter Delta M.")
            delta_m = float(delta_m_str)

            result = errors.calculate_stats_with_delta(numbers, var_name, delta_m, unit)

            self.stats_result_text.config(state=tk.NORMAL)
            self.stats_result_text.delete(1.0, tk.END)
            self.stats_result_text.insert(tk.END, result)
            self.stats_result_text.config(state=tk.DISABLED)

            if self.stats_append_var.get():
                title = self.stats_title_entry.get().strip()
                self.append_to_file(result, title)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def create_error_widgets(self):
        tk.Label(self.error_frame, text="Formula:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.error_formula_entry = tk.Entry(self.error_frame, width=50)
        self.error_formula_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.error_frame, text="Calculated Variable:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.error_calculated_variable_entry = tk.Entry(self.error_frame, width=50)
        self.error_calculated_variable_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.error_frame, text="Calculated Variable Unit:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.error_calculated_variable_unit_entry = tk.Entry(self.error_frame, width=50)
        self.error_calculated_variable_unit_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.error_frame, text="Variables (name=value, comma-separated):").grid(row=3, column=0, sticky="w",
                                                                                         padx=5, pady=2)
        self.variables_entry = tk.Entry(self.error_frame, width=50)
        self.variables_entry.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(self.error_frame, text="Errors (variable=value, comma-separated):").grid(row=4, column=0, sticky="w",
                                                                                          padx=5, pady=2)
        self.errors_entry = tk.Entry(self.error_frame, width=50)
        self.errors_entry.grid(row=4, column=1, padx=5, pady=2)

        self.error_append_var = tk.BooleanVar()
        self.error_append_checkbox = tk.Checkbutton(
            self.error_frame, text="Append to File", variable=self.error_append_var, command=self.toggle_error_title
        )
        self.error_append_checkbox.grid(row=5, column=0, sticky="w", padx=5, pady=2)

        tk.Label(self.error_frame, text="Title:").grid(row=5, column=1, sticky="e", padx=5, pady=2)
        self.error_title_entry = tk.Entry(self.error_frame, width=50, state=tk.DISABLED)
        self.error_title_entry.grid(row=5, column=2, padx=5, pady=2)

        self.error_calculate_button = tk.Button(self.error_frame, text="Calculate Error", command=self.calculate_error)
        self.error_calculate_button.grid(row=6, column=1, pady=5)

        self.error_result_text = scrolledtext.ScrolledText(self.error_frame, height=10, width=70, state=tk.DISABLED)
        self.error_result_text.grid(row=7, column=0, columnspan=3, padx=5, pady=5)


    def toggle_error_title(self):
        if self.error_append_var.get():
            self.error_title_entry.config(state=tk.NORMAL)
        else:
            self.error_title_entry.delete(0, tk.END)
            self.error_title_entry.config(state=tk.DISABLED)

    def calculate_error(self):
        try:
            formula = self.error_formula_entry.get().strip()
            if not formula:
                raise ValueError("Please enter a formula.")
            calculated_variable = self.error_calculated_variable_entry.get().strip()
            if not calculated_variable:
                raise ValueError("Please enter the calculated variable.")
            unit = self.error_calculated_variable_unit_entry.get().strip()
            variables_str = self.variables_entry.get().strip()
            if not variables_str:
                raise ValueError("Please enter variables.")
            variables = {var.split('=')[0].strip(): float(var.split('=')[1].strip()) for var in
                         variables_str.split(',')}

            errors_str = self.errors_entry.get().strip()
            if not errors_str:
                raise ValueError("Please enter errors.")
            errors_dict = {err.split('=')[0].strip(): float(err.split('=')[1].strip()) for err in errors_str.split(',')}

            value, delta, result = errors.calculate_error_with_propagation(
                formula, calculated_variable, variables, errors_dict, unit
            )

            self.error_result_text.config(state=tk.NORMAL)
            self.error_result_text.delete(1.0, tk.END)
            self.error_result_text.insert(tk.END, result)
            self.error_result_text.config(state=tk.DISABLED)

            if self.error_append_var.get():
                title = self.error_title_entry.get().strip()
                self.append_to_file(result, title)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def create_n_sigma_widgets(self):
        tk.Label(self.n_sigma_frame, text="Theoretical Result:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.theoretical_result_entry = tk.Entry(self.n_sigma_frame, width=50)
        self.theoretical_result_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.n_sigma_frame, text="Experimental Result:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.experimental_result_entry = tk.Entry(self.n_sigma_frame, width=50)
        self.experimental_result_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.n_sigma_frame, text="Theoretical Error:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.theoretical_error_entry = tk.Entry(self.n_sigma_frame, width=50)
        self.theoretical_error_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.n_sigma_frame, text="Experimental Error:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.experimental_error_entry = tk.Entry(self.n_sigma_frame, width=50)
        self.experimental_error_entry.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(self.n_sigma_frame, text="Calculated Variable Name:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.n_sigma_variable_entry = tk.Entry(self.n_sigma_frame, width=50)
        self.n_sigma_variable_entry.grid(row=4, column=1, padx=5, pady=2)

        self.n_sigma_append_var = tk.BooleanVar()
        self.n_sigma_append_checkbox = tk.Checkbutton(
            self.n_sigma_frame, text="Append to File", variable=self.n_sigma_append_var
        )
        self.n_sigma_append_checkbox.grid(row=5, column=0, sticky="w", padx=5, pady=2)

        tk.Label(self.error_frame, text="Title:").grid(row=5, column=1, sticky="e", padx=5, pady=2)
        self.n_sigma_title_entry = tk.Entry(self.n_sigma_frame, width=50, state=tk.DISABLED)
        self.n_sigma_title_entry.grid(row=5, column=2, padx=5, pady=2)

        self.n_sigma_button = tk.Button(self.n_sigma_frame, text="Calculate N-Sigma", command=self.calculate_n_sigma)
        self.n_sigma_button.grid(row=6, column=1, padx=5, pady=5)

        self.n_sigma_result_text = scrolledtext.ScrolledText(self.n_sigma_frame, height=5, width=70, state=tk.DISABLED)
        self.n_sigma_result_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def calculate_n_sigma(self):
        try:
            theoretical_result = float(self.theoretical_result_entry.get().strip())
            experimental_result = float(self.experimental_result_entry.get().strip())
            theoretical_error = float(self.theoretical_error_entry.get().strip())
            experimental_error = float(self.experimental_error_entry.get().strip())
            variable_name = self.n_sigma_variable_entry.get().strip()

            if not variable_name:
                raise ValueError("Variable name is required for N-Sigma calculation.")

            delta_k, n_sigma, latex_output = errors.calculate_n_sigma(
                theoretical_result, experimental_result, theoretical_error, experimental_error, variable_name
            )

            self.n_sigma_result_text.config(state=tk.NORMAL)
            self.n_sigma_result_text.delete(1.0, tk.END)
            self.n_sigma_result_text.insert(tk.END, latex_output)
            self.n_sigma_result_text.config(state=tk.DISABLED)

            if self.n_sigma_append_var.get():
                title = self.error_title_entry.get().strip()
                self.append_to_file(latex_output, title)

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during N-Sigma calculation: {e}")

    def create_plot_widgets(self):
        tk.Label(self.plot_frame, text="X Values (comma-separated):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.x_values_entry = tk.Entry(self.plot_frame, width=50)
        self.x_values_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.plot_frame, text="Y Values (comma-separated):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.y_values_entry = tk.Entry(self.plot_frame, width=50)
        self.y_values_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.plot_frame, text="X Errors (comma-separated):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.x_errors_entry = tk.Entry(self.plot_frame, width=50)
        self.x_errors_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.plot_frame, text="Y Errors (comma-separated):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.y_errors_entry = tk.Entry(self.plot_frame, width=50)
        self.y_errors_entry.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(self.plot_frame, text="Tick Amount:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.tick_amount_entry = tk.Entry(self.plot_frame, width=50)
        self.tick_amount_entry.grid(row=4, column=1, padx=5, pady=2)

        self.plot_button = tk.Button(self.plot_frame, text="Plot Data", command=self.plot_data)
        self.plot_button.grid(row=5, column=1, pady=5)

    def plot_data(self):
        try:
            x_str = self.x_values_entry.get().strip()
            y_str = self.y_values_entry.get().strip()
            x_errors_str = self.x_errors_entry.get().strip()
            y_errors_str = self.y_errors_entry.get().strip()
            tick_amount_str = self.tick_amount_entry.get().strip()

            if not all([x_str, y_str, x_errors_str, y_errors_str, tick_amount_str]):
                raise ValueError("Please fill in all fields for plotting.")

            x = list(map(float, x_str.split(',')))
            y = list(map(float, y_str.split(',')))
            x_errors = list(map(float, x_errors_str.split(',')))
            y_errors = list(map(float, y_errors_str.split(',')))
            tick_amount = int(tick_amount_str)

            if not (len(x) == len(y) == len(x_errors) == len(y_errors)):
                raise ValueError("X, Y, X Errors, and Y Errors must have the same number of elements.")

            self.root.after(0, lambda: self.execute_plot(x, y, x_errors, y_errors, tick_amount))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while plotting: {e}")

    def execute_plot(self, x, y, x_errors, y_errors, tick_amount):
        try:
            plot_with_error_bars(
                x, y, x_errors, y_errors,
                x_label="X-axis", y_label="Y-axis",
                plot_title="Error Bar Plot",
                amount_of_ticks=tick_amount
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while plotting: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ErrorCalculationApp(root)
    root.mainloop()
