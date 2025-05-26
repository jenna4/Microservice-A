import time
import os
print("Current working directory:", os.getcwd())

#pull request tested

REQUEST_FILE = "request.txt"
RESPONSE_FILE = "response.txt"
USERS_FILE = "users.txt"

# helper: clean up before each test
def reset_files():
    if os.path.exists(RESPONSE_FILE):
        os.remove(RESPONSE_FILE)
    if os.path.exists(REQUEST_FILE):
        os.remove(REQUEST_FILE)


# helper: run a test case
def run_test(test_name, action, username, password, wait=5):
    print(f"\n=== {test_name} ===")
    reset_files()

    # write request.txt
    with open(REQUEST_FILE, "w") as f:
        f.write(f"action={action}\n")
        f.write(f"username={username}\n")
        f.write(f"password={password}\n")
    time.sleep(0.5)  # give microservice a moment to process

    print(f"→ {action.upper()} request written for '{username}'.")
    print("Waiting for microservice to process...")

    # wait for response file (timeout after 10s)
    for _ in range(20):
        if os.path.exists(RESPONSE_FILE):
            time.sleep(0.2)
            break
        time.sleep(0.5)

    # display the response
    if os.path.exists(RESPONSE_FILE):
        print("Response received:")
        with open(RESPONSE_FILE, "r") as f:
            print(f.read())
    else:
        print("No response received.")

    # wait to run next test
    input("Press Enter to continue to the next test...")




#clear users.txt before testing
if os.path.exists(USERS_FILE):
    os.remove(USERS_FILE)

reset_files()

# test cases
run_test("TEST 1: Register a new user", "register", "demo_user", "abc123", wait=10)
run_test("TEST 2: Try to register existing user", "register", "demo_user", "abc123", wait=10)
run_test("TEST 3: Log in with correct password", "login", "demo_user", "abc123", wait=10)
run_test("TEST 4: Log in with incorrect password", "login", "demo_user", "wrongpass", wait=10)

print("\nAll tests completed.")
