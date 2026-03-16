import os
import sys
import pymysql

# Mocking mysqlclient for Django compatibility
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

# Ensure the project directory is in the path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_project.settings')

from expense_project.wsgi import application
