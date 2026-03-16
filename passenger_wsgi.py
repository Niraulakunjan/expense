import sys
import os

# Redirect stderr to a log file for better debugging
path = os.path.dirname(os.path.abspath(__file__))
sys.stderr = open(os.path.join(path, 'passenger_stderr.log'), 'a')

# Bare minimum test application to verify if Passenger is running this file
def application(environ, start_response):
    status = '200 OK'
    output = b"Hello from Passenger! If you see this, the file is being executed correctly.\n"
    
    # Log to a file to be 100% sure
    with open(os.path.join(path, 'passenger_test.log'), 'a') as f:
        f.write("Application called successfully!\n")
        
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]

