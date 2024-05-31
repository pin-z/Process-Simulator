import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import psutil  # For system resource data

# Define a color scheme
bg_color = "#2C3E50"
text_color = "#ECF0F1"
button_color = "#3498DB"
error_color = "#E74C3C"

# Define a font scheme
font = "Arial 12"
font_bold = "Arial 12 bold"
font_mono = "Courier 10"  # Monospaced font for logs
# Define padding
pad_x = 20
pad_y = 10

# Root window setup
root = tk.Tk()
root.title("Process Simulator")
root.geometry("600x500")
root.configure(bg=bg_color)
root.withdraw()


def create_display_window(title, command):
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry("800x600")  # Adjusted size

    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text = tk.Text(window, font=font_mono, yscrollcommand=scrollbar.set, bg="#0E1621", fg="#FFFFFF", insertbackground="white")
    text.pack(fill=tk.BOTH, expand=True)

    # Run the command and write the output to the Text widget
    command_output = subprocess.check_output(command, shell=True).decode()
    text.insert(tk.END, command_output)

    scrollbar.config(command=text.yview)
    
# Login window setup
def login():
    def validate_login(event=None):
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "password":
            print("Login successful.")
            root.deiconify()
            login_window.destroy()
        else:
            error_label.config(text="Invalid username or password. Please try again.", fg=error_color)

    login_window = tk.Toplevel(root, bg=bg_color)
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username: ", bg=bg_color, fg=text_color, font=font).pack(pady=pad_y)
    username_entry = tk.Entry(login_window, font=font)
    username_entry.pack()

    tk.Label(login_window, text="Password: ", bg=bg_color, fg=text_color, font=font).pack(pady=pad_y)
    password_entry = tk.Entry(login_window, show="*", font=font)
    password_entry.pack()
    password_entry.bind("<Return>", validate_login)

    submit_button = tk.Button(login_window, text="Submit", command=validate_login, bg=button_color, fg=text_color, font=font_bold)
    submit_button.pack(pady=pad_y)

    error_label = tk.Label(login_window, bg=bg_color, font=font)
    error_label.pack()

    login_window.bind("<Return>", validate_login)

# Main menu setup
def main_menu():
    frame = tk.Frame(root, bg=bg_color)
    frame.pack(padx=pad_x, pady=pad_y, fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Welcome to the Process Simulator!", bg=bg_color, fg=text_color, font=font_bold).pack(pady=pad_y)
    tk.Button(frame, text="List of Running Processes", command=process_1, bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)
    tk.Button(frame, text="Terminate Process", command=process_2, bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)
    tk.Button(frame, text="High and Low Priority Processes", command=process_3, bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)
    tk.Button(frame, text="System Resource Monitoring", command=process_4, bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)
    tk.Button(frame, text="System Resource Graph", command=display_resource_graph, bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)
    tk.Button(frame, text="Process Logging", command=process_6, bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)
    tk.Button(frame, text="Quit", command=quit, bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)

# Define the functions for each menu option (process_1, process_2, process_3, process_4, process_6)
# ...
def process_1():
    create_display_window("List of Running Processes", "ps -ef")

def process_2():
    def terminate_process():
        process_id = process_id_entry.get()
        if process_id.isdigit():  # Check if the input is a number
            try:
                # Terminate the process using the provided process ID
                subprocess.run(["kill", "-9", process_id], check=True)
                messagebox.showinfo("Success", f"Process with ID {process_id} terminated successfully.")
            except subprocess.CalledProcessError:
                messagebox.showerror("Failure", f"Failed to terminate process with ID {process_id}.")
            except subprocess.SubprocessError:
                messagebox.showerror("Error", "An error occurred while terminating the process.")
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid process ID.")

    # create a new window to input the process ID
    window = tk.Toplevel(root, bg=bg_color)
    window.geometry("400x200")
    window.title("Terminate a Process")

    process_id_label = tk.Label(window, text="Process ID: ", bg=bg_color, fg=text_color)
    process_id_label.pack(pady=10)
    process_id_entry = tk.Entry(window)
    process_id_entry.pack()

    terminate_button = tk.Button(window, text="Terminate", command=terminate_process, bg=button_color, fg=text_color)
    terminate_button.pack(pady=10)

def process_3():
    window = tk.Toplevel(root)
    window.geometry("800x600")
    window.title("High and Low Priority Processes")

    # Create a single frame with a scrollbar
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Use a single Text widget with tags to differentiate high and low priority processes
    text = tk.Text(frame, font=font_mono, yscrollcommand=scrollbar.set, wrap="none", bg="#0E1621", fg="#FFFFFF")
    text.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=text.yview)

    # Define tags for high and low priority processes
    text.tag_config('high_priority', foreground='red')
    text.tag_config('low_priority', foreground='green')

    # Run the `ps -eo pid,user,ni,comm` command and split the output into lines
    ps_output = subprocess.check_output(["ps", "-eo", "pid,user,ni,comm"]).decode().split("\n")

    # Insert a heading
    text.insert(tk.END, "PID\tUSER\tNICE\tCOMMAND\n", 'heading')

    # Iterate over the lines of output and add them to the Text widget with appropriate tags
    for line in ps_output[1:]:
        if line:
            pid, user, nice, comm = line.split(maxsplit=3)
            tag = 'high_priority' if int(nice) < 0 else 'low_priority'
            text.insert(tk.END, f"{pid}\t{user}\t{nice}\t{comm}\n", tag)


def process_4():
    create_display_window("System Resource Usage", "top -b -n 1")
    


    
def process_6():
    def display_logs(log_path):
        # Create a new window to display the log
        log_window = tk.Toplevel(root)
        log_window.title(f"Log - {log_path}")
        log_window.geometry("800x600")  # Adjusted size

        # Search bar to filter logs
        search_frame = tk.Frame(log_window, bg=bg_color)
        search_frame.pack(fill=tk.X)
        search_label = tk.Label(search_frame, text="Search:", bg=bg_color, fg=text_color, font=font)
        search_label.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)
        search_entry = tk.Entry(search_frame, font=font)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=pad_x, pady=pad_y)

        # Text widget with a scrollbar
        scrollbar = tk.Scrollbar(log_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        log_text = tk.Text(log_window, font=font_mono, yscrollcommand=scrollbar.set, wrap="none", bg="#0E1621", fg="#FFFFFF")
        log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=log_text.yview)

        # Function to refresh the logs
        def refresh_logs():
            log_text.delete(1.0, tk.END)
            try:
                with open(log_path, "r") as file:
                    log_text.insert(tk.END, file.read())
            except FileNotFoundError:
                log_text.insert(tk.END, f"Log file '{log_path}' not found.")

        # Function to search the logs
        def search_logs():
            search_query = search_entry.get()
            log_text.tag_remove('search', '1.0', tk.END)
            if search_query:
                idx = '1.0'
                while True:
                    idx = log_text.search(search_query, idx, nocase=True, stopindex=tk.END)
                    if not idx: break
                    lastidx = f"{idx}+{len(search_query)}c"
                    log_text.tag_add('search', idx, lastidx)
                    idx = lastidx
                log_text.tag_config('search', background='green')

        # Button to trigger log search
        search_button = tk.Button(search_frame, text="Search", command=search_logs, bg=button_color, fg=text_color, font=font)
        search_button.pack(side=tk.RIGHT, padx=pad_x, pady=pad_y)

        # Button to refresh log display
        refresh_button = tk.Button(log_window, text="Refresh", command=refresh_logs, bg=button_color, fg=text_color, font=font)
        refresh_button.pack(pady=pad_y)

        # Initial log loading
        refresh_logs()

    logging_window = tk.Toplevel(root, bg=bg_color)
    logging_window.title("Process Logging")

    tk.Label(logging_window, text="Welcome to Process Logging", bg=bg_color, fg=text_color, font=font_bold).pack(pady=pad_y)

    tk.Button(logging_window, text="System Log", command=lambda: display_logs("/var/log/syslog"), bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)
    tk.Button(logging_window, text="Security Log", command=lambda: display_logs("/var/log/auth.log"), bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)
    tk.Button(logging_window, text="Kernel Log", command=lambda: display_logs("/var/log/kern.log"), bg=button_color, fg=text_color, font=font).pack(fill=tk.X, padx=pad_x, pady=pad_y)

def display_resource_graph():
    # Create a new Tkinter window
    graph_window = tk.Toplevel(root)
    graph_window.title("System Resource Graph")
    graph_window.geometry("600x400")

    # Create a figure and a subplot
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Gather system resource data, for example, CPU usage
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

    # Plot the data
    ax.plot(cpu_usage, marker='o', linestyle='-', color='b')
    ax.set_title('CPU Usage Over Time')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('CPU Usage (%)')

    # Embed the graph in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Add a refresh button to update the graph
    refresh_button = tk.Button(graph_window, text="Refresh", command=lambda: update_graph(ax, canvas))
    refresh_button.pack()

    def update_graph(ax, canvas):
        # Clear the current plot
        ax.cla()

        # Re-plot the data
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        ax.plot(cpu_usage, marker='o', linestyle='-', color='b')
        ax.set_title('CPU Usage Over Time')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('CPU Usage (%)')

        # Redraw the canvas
        canvas.draw()

def quit():
    print("Exiting...")
    root.destroy()

root = tk.Tk()
root.title("Process Simulator")
root.geometry("400x300")
root.withdraw()

# Start the application
login()
main_menu()
root.mainloop()
