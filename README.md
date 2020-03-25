# DB Auto Import Script

This script resolves user definer issue while importing databases from one sql server to another (e.g. production server to local dev server). It modifies user definer entry on all views/stored procedures inside sql dump files. After modifying the definer it will automatically import specified databases.

### Requirements

* OS - Linux/MacOS
* Python >= 3.6
* MySQL, MariaDB or Percona

__NOTE__ - If you are using Percona, comment out line 58 and uncomment line 60

```
# default mysql
# grant_db_permissions = f"GRANT ALL PRIVILEGES ON {db_name}.* TO {db_user}@{db_host} IDENTIFIED BY {db_password};"
# percona specific
grant_db_permissions = f"GRANT ALL PRIVILEGES ON {db_name}.* TO {db_user}@{db_host};"
```

### Configuration

Open the db_auto_import.py script in your favorite text editor and edit the lines below.

```
# Dump file path - here you can set your own path 
dump_path = "./dumps/"
# Set the list of dump file names to import
dump_files = ["testing.sql"]
# Set the list of definer names (inside dump file) you want to replace with your local db definer
dump_definers = ["DEFINER=`prod`@`some-host.com`"]

# MySQL local root username
db_root_user = "root"
# Set db names for each dump file - this must be in correct order
db_names = ["testing"]

# Local db user info
db_user = "testing"
db_password = "testing"
db_host = "localhost"
```

### How to run the script

First we need to copy/paste all production dump files to /dumps/ folder. Dump file names must match the names specified in dump_files list. Double check your config and run the command below.

```
python db_auto_import.py
```



