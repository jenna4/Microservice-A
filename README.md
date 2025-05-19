# Login Microservice – Text File Communication Contract
This microservice handles user registration and login functionality using plain text files as the communication pipe. This contract outlines how your main application should send requests and receive responses from the microservice.

# How to Request Data from the Microservice
To request data, your program must create a file named request.txt in the root directory. This file must contain three lines in the following key=value format:
- action – Either register or login
- username – The username to register or log in with
- password – The corresponding password

Example: Register a New User
action=register
username=demo_user
password=abc123

Example: Log in an Existing User
action=login
username=demo_user
password=abc123

Do not write anything else in the file. The microservice reads only these three lines.

# How to Recieve Data from the Microservice
After processing the request, the microservice will write a file named response.txt with two lines:
- status – Either success or error
- message – A explanation of the result

Example: Successful Registration Response
status=success
message=Account created successfully.

Example: Failed Login Response
status=error
message=Incorrect username or password.

To receive data:
Wait for response.txt to appear. Open and read its contents using standard file I/O.

# Important Notes
users.txt is used internally by the microservice to store registered accounts. Only one request should be in progress at a time. Always wait for response.txt to be written before sending another request.txt.

# UML Sequence Diagram
Client Program Login Microservice Filesystem
Client Program            Login Microservice              Filesystem
     |                           |                              |
     |-- write request.txt ----> |                              |
     |                           |-- check if request.txt ----> | (os.path.exists)
     |                           |-- open & read request.txt -->|
     |                           |                              |
     |                           |-- process_request()          |
     |                           |   |                          |
     |                           |   |-- load_users() --------->| (read users.txt)
     |                           |   |                          |
     |                           |   |-- check action           |
     |                           |   |   |                      |
     |                           |   |   |-- if register        |
     |                           |   |   |   |-- save_user() -->| (append users.txt)
     |                           |   |   |                      |
     |                           |   |   |-- or                 |
     |                           |   |   |-- if login           |
     |                           |   |                          |
     |                           |   |-- write_response() ----> | (write response.txt)
     |                           |   |                          |
     |                           |   |-- delete request.txt --->| (os.remove)
     |                           |                              |
     |<-- read response.txt -----|                              |
     |                           |                              |

     
First, the client program initiates the process by writing a request.txt file to the shared directory. This file includes three key-value pairs: action, username, and password. The login microservice continuously monitors for the presence of this file. Once it detects it, the microservice reads the contents, processes the request according to the specified action (either to register a new user or to authenticate an existing one), and then generates a corresponding response.txt file. This response file contains a status (such as "success" or "error") and a descriptive message. After the response is written, the client program reads the response.txt file to determine the result of its original request.

