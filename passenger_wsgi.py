import os
import sys
import pymysql
import traceback

# Mocking mysqlclient for Django compatibility
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

# Ensure the project directory is in the path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_project.settings')

# Log environment info for debugging
with open(os.path.join(path, 'passenger_debug.log'), 'a') as f:
    f.write(f"\n--- Startup: {sys.version} ---\n")
    f.write(f"Python path: {sys.path}\n")
    f.write(f"CWD: {os.getcwd()}\n")

try:
    from expense_project.wsgi import application
except Exception:
    with open(os.path.join(path, 'passenger_debug.log'), 'a') as f:
        f.write("\n--- WSGI Import Failed ---\n")
        traceback.print_exc(file=f)
    raise
