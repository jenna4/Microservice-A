import os
import time
print("Current working directory:", os.getcwd())


USER_FILE = "users.txt"
REQUEST_FILE = "request.txt"
RESPONSE_FILE = "response.txt"

# load users from file into a dictionary
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                # split into username and password at the colon
                if ":" in line:
                    username, password = line.strip().split(":")
                    #assign password to username in user data dictionary
                    users[username] = password
    return users

# save a new user to file
def save_user(username, password):
    # open file in append mode and write the user/password to it
    with open(USER_FILE, "a") as f:
        f.write(f"{username}:{password}\n")

# process a request
def process_request():
    
    # find request
    if not os.path.exists(REQUEST_FILE):
        return  # no request yet

    # read the request
    with open(REQUEST_FILE, "r") as f:
        # empty data dictionary 
        data = {}
        # repeat for each line 
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1) # remove whitespace and split at most once
                data[key] = value #store in dictionary for later use 

    #get data and store in vars
    action = data.get("action")
    username = data.get("username")
    password = data.get("password")

    users = load_users()

    # determine the response
    if action == "register":
        # if already exists
        if username in users:
            write_response("error", "Username already exists.")
        #if new user
        else:
            save_user(username, password)
            write_response("success", "Account created successfully.")

    elif action == "login":
        # sucessful login
        if username in users and users[username] == password:
            write_response("success", f"Welcome back, {username}.")
        #unsuccessful login
        else:
            write_response("error", "Incorrect username or password.")
    else:
        write_response("error", "Invalid action.")

# write to response.txt
def write_response(status, message):
    with open(RESPONSE_FILE, "w") as f:
        f.write(f"status={status}\n")
        f.write(f"message={message}\n")
        f.flush()
        os.fsync(f.fileno())  # ensure the write completes immediately

# main loop to monitor requests
if __name__ == "__main__":
    print("Microservice started. Watching for requests...")
    while True:
        process_request()
        time.sleep(1)  # check every 1 second
