# Secure Network Simulation System

A GUI-based network access control simulator built with Python (tkinter), demonstrating IP address assignment and role-based, port-level access control for connected devices.

## Why this project

Access control is a foundational cybersecurity concept: not every device on a network should have the same level of access. This simulator models a simplified version of that reality — devices are assigned an access level, and each level maps to a specific set of allowed ports, mirroring how real network access control lists (ACLs) and role-based permissions work.

## How it works

1. **Add a device** — enter a name and choose an access level (Admin, Read-Write, Read-Only, or Blocked). The system automatically assigns the next available IP address (192.168.1.x).
2. **Access levels map to allowed ports:**
   - Admin: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3389 (RDP)
   - Read-Write: 80, 443
   - Read-Only: 80
   - Blocked: no ports allowed
3. **Test access** — select any device in the table, enter a port number, and the system evaluates whether that device's access level permits the requested port, returning a clear Access Granted or Access Denied result.
4. Devices can also be removed from the simulated network at any time.

## Example output

**Full interface with devices added:**

![network simulator full view](Screenshot%202026-09-10%20194044.png)

**Access granted (Admin device requesting an allowed port):**

![access granted](Screenshot%202026-09-10%20193950.png)

**Access denied (Read-Only device requesting a restricted port):**

![access denied](Screenshot%202026-09-10%20194012.png)

## Tech stack

Python, `tkinter` (built-in GUI library). No external dependencies.

## Run it yourself

```bash
python network_sim.py
```

## What I learned

Building this reinforced how access control systems enforce the principle of least privilege in practice — mapping roles to specific, minimal permissions rather than granting broad access by default, and how a GUI can make these normally invisible network-layer decisions visible and testable.

## Possible extensions

- Persist devices to a file/database instead of in-memory storage
- Add IP-based restrictions alongside port-based ones
- Simulate multiple simultaneous access attempts with a request log
