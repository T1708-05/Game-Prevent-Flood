import json

class UserDatabase:
    
    def __init__(self, filename = 'user_data.json'):
        self.filename = filename
        self.users = {}
        self.load_data()

    # Load data from json database
    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty dictionary
            self.users = {}

    # Save data to json database
    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.users, f, indent=3)

    # Register a new user with username and password -> save to json database
    def register_user(self, username, password):
        if username in self.users or username == '':
            return False                    # Dang ki that bai
        self.users[username] = {'password': password}   ## Khoi tao cac thong so khac cua user
        self.save_data()
        return True                         # Dang ki thanh cong
    
    # Login user with username and password 
    # -> return tuple of (username, password) if success, False if fail
    def login_user(self, username, password):
        if username in self.users:
            if self.users[username]['password'] == password:
                return (username, password)
            else:
                return False # wrong password
        else:
            return False # wrong username

