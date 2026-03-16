import os
import sys

print("--- Django Diagnostic Check ---")

try:
    import pymysql
    pymysql.version_info = (2, 2, 1, 'final', 0)
    pymysql.install_as_MySQLdb()
    print("[SUCCESS] PyMySQL imported and patched.")
except ImportError:
    print("[ERROR] PyMySQL not found. Run: pip install pymysql")

try:
    import dotenv
    print("[SUCCESS] python-dotenv found.")
except ImportError:
    print("[ERROR] python-dotenv not found. Run: pip install python-dotenv")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_project.settings')

try:
    import django
    django.setup()
    print(f"[SUCCESS] Django initialized (Version: {django.get_version()}).")
except Exception as e:
    print(f"[ERROR] Django initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from django.db import connection
    connection.ensure_connection()
    print(f"[SUCCESS] Database connected (Engine: {connection.settings_dict['ENGINE']}).")
except Exception as e:
    print(f"[ERROR] Database connection failed: {e}")
    import traceback
    traceback.print_exc()

print("--- End of Check ---")
