# File System Access Control

A Python-based file system with Access Control Lists (ACL) and permission management. This project implements a secure file system with user authentication, role-based access control, and comprehensive audit logging.

## Features

- **User Authentication**: Login system with username and password validation
- **Group Management**: Create groups and manage user group memberships
- **File System Operations**: Create, read, and list files and directories
- **Access Control Lists (ACL)**: Fine-grained permission control at user and group levels
- **Unix-style Permissions**: Traditional rwx permission model (owner, group, others)
- **Audit Logging**: Track all system operations for security and compliance
- **Multi-level Permission Checks**: ACL-based access with Unix permission fallback

## Project Structure

```
├── main.py              # CLI interface and command handler
├── auth.py              # User authentication module
├── users.py             # User and group management
├── filesystem.py        # File system operations
├── permissions.py       # Permission validation logic
├── acl.py               # Access Control List management
├── audit.py             # Audit logging functionality
├── setup_users.py       # Initial user setup script
├── data/                # Persistent data storage
│   ├── users.json       # User credentials and metadata
│   ├── groups.json      # Group definitions
│   ├── filesystem.json  # File system structure
│   └── acl.json         # ACL configurations
├── tests/               # Test suite
│   └── test_access.py   # Access control tests
└── README.md            # This file
```

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone or download the project
2. Navigate to the project directory
3. Initialize users with the setup script:
   ```bash
   python3 setup_users.py
   ```

## Usage

Start the interactive CLI:

```bash
python3 main.py
```

### Available Commands

#### Authentication

- `login <username> <password>` - Login as a user
- `logout` - Logout current user

#### Group Management

- `create_group <group>` - Create a new group
- `add_user_to_group <user> <group>` - Add user to group
- `my_groups` - Show groups of current user

#### File System

- `mkdir <path>` - Create a new directory
- `touch <path>` - Create a new file
- `ls` - List files in current directory
- `cat <file>` - Display file contents

#### Access Control

- `setfacl_user <path> <user> <rw>` - Set ACL for a user (e.g., `rw` for read+write)
- `setfacl_group <path> <group> <rw>` - Set ACL for a group
- `getacl <path>` - View ACL for a file/directory

#### System

- `audit` - Display audit log
- `help` - Show help message
- `exit` - Exit the program

## Permission System

### Permission Model

The system uses a 3-tier permission evaluation:

1. **User ACL** (Highest Priority) - Direct user permissions
2. **Group ACL** - Permissions via group membership
3. **Unix Permissions** (Fallback) - Traditional rwx model
   - Owner permissions (first 3 characters)
   - Group permissions (middle 3 characters)
   - Others permissions (last 3 characters)

### Permission Types

- `r` - Read
- `w` - Write
- `x` - Execute

## Data Storage

All data is persisted in JSON format in the `data/` directory:

- **users.json**: User accounts and hashed passwords
- **groups.json**: Group definitions and members
- **filesystem.json**: File system tree with metadata
- **acl.json**: ACL configurations

## Testing

Run the test suite:

```bash
python3 -m pytest tests/
```

## Security Features

- Password hashing for stored credentials
- Audit trail for all operations
- Multi-level permission checks
- Group-based access control
- ACL overrides for granular control

## Architecture

### Core Modules

- **auth.py**: Handles user authentication
- **users.py**: Manages users and groups
- **filesystem.py**: File and directory operations
- **permissions.py**: Permission validation logic
- **acl.py**: ACL management
- **audit.py**: Event logging

## License

This project is provided as-is for educational and development purposes.
