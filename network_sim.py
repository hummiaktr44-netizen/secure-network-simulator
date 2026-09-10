import tkinter as tk
from tkinter import ttk, messagebox

# In-memory "network" - list of connected devices
devices = []
next_ip_suffix = 1


class Device:
    def __init__(self, name, ip, access_level):
        self.name = name
        self.ip = ip
        self.access_level = access_level  # "Admin", "Read-Write", "Read-Only", "Blocked"
        self.allowed_ports = self.get_ports_for_level(access_level)

    @staticmethod
    def get_ports_for_level(level):
        if level == "Admin":
            return [22, 80, 443, 3389]  # SSH, HTTP, HTTPS, RDP
        elif level == "Read-Write":
            return [80, 443]
        elif level == "Read-Only":
            return [80]
        else:  # Blocked
            return []


def assign_next_ip():
    global next_ip_suffix
    ip = f"192.168.1.{next_ip_suffix}"
    next_ip_suffix += 1
    return ip


def add_device():
    name = name_entry.get().strip()
    level = access_var.get()

    if not name:
        messagebox.showwarning("Missing name", "Please enter a device name.")
        return

    ip = assign_next_ip()
    device = Device(name, ip, level)
    devices.append(device)

    refresh_table()
    name_entry.delete(0, tk.END)


def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for d in devices:
        ports_str = ", ".join(str(p) for p in d.allowed_ports) if d.allowed_ports else "None"
        tree.insert("", tk.END, values=(d.name, d.ip, d.access_level, ports_str))


def remove_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("No selection", "Select a device to remove.")
        return
    for item in selected:
        values = tree.item(item, "values")
        devices[:] = [d for d in devices if d.ip != values[1]]
    refresh_table()


def test_access():
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("No selection", "Select a device to test access for.")
        return

    values = tree.item(selected[0], "values")
    device_ip = values[1]
    device = next((d for d in devices if d.ip == device_ip), None)

    try:
        requested_port = int(port_entry.get().strip())
    except ValueError:
        messagebox.showwarning("Invalid port", "Enter a valid port number.")
        return

    if requested_port in device.allowed_ports:
        messagebox.showinfo(
            "Access Granted",
            f"{device.name} ({device.ip}) is ALLOWED on port {requested_port}."
        )
    else:
        messagebox.showerror(
            "Access Denied",
            f"{device.name} ({device.ip}) is BLOCKED on port {requested_port}.\n"
            f"Access level '{device.access_level}' does not permit this port."
        )


# ---------------- GUI Layout ----------------

root = tk.Tk()
root.title("Secure Network Simulation System")
root.geometry("700x450")

# Top frame - add device
top_frame = tk.Frame(root, padx=10, pady=10)
top_frame.pack(fill=tk.X)

tk.Label(top_frame, text="Device Name:").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(top_frame, width=20)
name_entry.grid(row=0, column=1, padx=5)

tk.Label(top_frame, text="Access Level:").grid(row=0, column=2, sticky="w")
access_var = tk.StringVar(value="Read-Only")
access_dropdown = ttk.Combobox(
    top_frame, textvariable=access_var,
    values=["Admin", "Read-Write", "Read-Only", "Blocked"],
    state="readonly", width=15
)
access_dropdown.grid(row=0, column=3, padx=5)

add_btn = tk.Button(top_frame, text="Add Device", command=add_device, bg="#2e7d32", fg="white")
add_btn.grid(row=0, column=4, padx=10)

# Table of devices
table_frame = tk.Frame(root, padx=10, pady=10)
table_frame.pack(fill=tk.BOTH, expand=True)

columns = ("Name", "IP Address", "Access Level", "Allowed Ports")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill=tk.BOTH, expand=True)

# Bottom frame - actions
bottom_frame = tk.Frame(root, padx=10, pady=10)
bottom_frame.pack(fill=tk.X)

remove_btn = tk.Button(bottom_frame, text="Remove Selected Device", command=remove_selected, bg="#c62828", fg="white")
remove_btn.grid(row=0, column=0, padx=5)

tk.Label(bottom_frame, text="Test Port:").grid(row=0, column=1, padx=5)
port_entry = tk.Entry(bottom_frame, width=8)
port_entry.grid(row=0, column=2, padx=5)

test_btn = tk.Button(bottom_frame, text="Test Access", command=test_access, bg="#1565c0", fg="white")
test_btn.grid(row=0, column=3, padx=5)

root.mainloop()