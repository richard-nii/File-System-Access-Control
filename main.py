# main.py
from auth import authenticate
from users import create_group, add_user_to_group, get_user_groups
from filesystem import create_dir, create_file, list_dir, read_file
from permissions import has_permission
from acl import set_user_acl, set_group_acl, get_acl


current_user = None


def show_help():
    print("""
Available commands:
  help                                      (show this help message) 
  login <username> <password>               Login as a user
  logout                                    Logout current user 

  create_group <group>                      Create a new group
  add_user_to_group <user> <group>          Add user to group
  my_groups                                 Show groups of current user
          
  mkdir <path>                              Create a new directory        
  touch <path>                              Create a new file  

  ls                                        display files in current directory
  cat <file>                                display file contents 

  audit                                     display audit log
          
  setfacl_user <path> <user> <rw>           Set user ACL
  setfacl_group <path> <group> <rw>         Set group ACL      
  getacl <path>                             Get ACL of a file/directory
          
  exit
""")



def handle_login(args):
    global current_user

    if len(args) != 2:
        print("Usage: login <username> <password>")
        return

    username, password = args

    if authenticate(username, password):
        current_user = username
        print(f"User '{username}' logged in successfully")
    else:
        print("Authentication failed")



def handle_logout():
    global current_user
    if current_user is None:
        print("No user is currently logged in")
    else:
        print(f"User '{current_user}' logged out")
        current_user = None


def main():
    print("=== File System Access Control CLI ===")
    print("Type 'help' to see available commands")

    while True:
        prompt = f"{current_user if current_user else 'guest'}> "
        command = input(prompt).strip()

        if not command:
            continue

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "help":
            show_help()

        elif cmd == "login":
            handle_login(args)

        elif cmd == "logout":
            handle_logout()

        elif cmd == "exit":
            print("Exiting system...")
            break

        elif cmd == "create_group":
            if len(args) != 1:
                print("Usage: create_group <group>")
            elif create_group(args[0]):
                print("Group created")
            else:
                print("Group already exists")

        elif cmd == "add_user_to_group":
            if len(args) != 2:
                print("Usage: add_user_to_group <user> <group>")
            elif add_user_to_group(args[0], args[1]):
                print("User added to group")
            else:
                print("Failed to add user to group")

        elif cmd == "my_groups":
            if not current_user:
                print("You must be logged in")
            else:
                groups = get_user_groups(current_user)
                print("Groups:", ", ".join(groups) if groups else "None")

        elif cmd == "mkdir":
            if not current_user:
                print("Login required")
            elif create_dir(args[0], current_user, get_user_groups(current_user)[0]):
                print("Directory created")
            else:
                print("Directory exists")

        elif cmd == "touch":
            if not current_user:
                print("Login required")
            elif create_file(args[0], current_user, get_user_groups(current_user)[0]):
                print("File created")
            else:
                print("File exists")
        elif cmd == "ls":
            if not current_user:
                print("Login required")
                continue

            files = list_dir(current_user, get_user_groups(current_user))
            for f in files:
                print(f) 

        elif cmd == "cat":
            if not current_user:
                print("Login required")
                continue

            result = read_file(args[0], current_user, get_user_groups(current_user))

            if result == "PERMISSION_DENIED":
                print("Permission denied")
            elif result is None:
                print("File not found")
            else:
                print(result)

        elif cmd == "audit":
            with open("data/audit.log") as f:
                for line in f:
                    print(line.strip())
            continue

        elif cmd == "setfacl_user":
            if not current_user:
                print("Login required")
            elif set_user_acl(args[0], args[1], args[2], current_user):
                print("User ACL set")
            else:
                print("Failed to set User ACL")

        elif cmd == "setfacl_group":
            if not current_user:
                print("Login required")
            elif set_group_acl(args[0], args[1], args[2], current_user):
                print("Group ACL set")
            else:
                print("Failed to set Group ACL")

        elif cmd == "getacl":
            acl = get_acl(args[0])
            if acl is None:
                print("File not found")
            else:
                print("User ACLs:", acl["users"])
                print("Group ACLs:", acl["groups"])

        else:
            print(f"Unknown command: {cmd}. Type 'help' for assistance.")

        


if __name__ == "__main__":
    main()
