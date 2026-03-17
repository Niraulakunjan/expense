import os
import sys

# Mocking mysqlclient for Django compatibility
import pymysql
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

# Ensure the project directory is in the path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_project.settings')

# Log startup for debugging
LOG_FILE = os.path.join(path, 'passenger_debug.log')
with open(LOG_FILE, 'a') as f:
    f.write(f"\n--- [STARTUP] {sys.version} ---\n")
    f.write(f"CWD: {os.getcwd()}\n")
    f.write(f"PID: {os.getpid()}\n")

try:
    from expense_project.wsgi import application
    with open(LOG_FILE, 'a') as f:
        f.write("[SUCCESS] WSGI application imported successfully.\n")
except Exception:
    with open(LOG_FILE, 'a') as f:
        f.write("\n--- [CRASH] WSGI Import Failed ---\n")
        traceback.print_exc(file=f)
    raise
