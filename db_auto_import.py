import getpass
import os
import time

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

# Generate definer name from local db config - desired definer
# You can hard-code this value if you wish 
local_definer = f"DEFINER=`{db_user}`@`{db_host}`"

# ------------------------------------------------------------------------------
# You are all set - Leave the rest of the code as it is
# ------------------------------------------------------------------------------

# SQL connection config
mysql_config = f"mysql -u {db_root_user}"


def fix_dump_definer(dump_file):
    dump_file_path = dump_path + dump_file

    print("Fixing dump file:", dump_file)

    # Read file
    with open(dump_file_path, "rb") as file:
        file_data = file.read()

    # Replace the target string bytes
    for dump_definer in dump_definers:
        file_data = file_data.replace(dump_definer.encode(), local_definer.encode())

    # Write the file out again
    with open(dump_file_path, "wb") as file:
        file.write(file_data)

    print("Fixing dump file done:", dump_file)


def create_db(db_name):
    drop_db = f"DROP DATABASE IF EXISTS {db_name};"
    recreate_db = f"CREATE DATABASE {db_name} CHARACTER SET utf8 COLLATE utf8_general_ci;"
    # default mysql
    grant_db_permissions = f"GRANT ALL PRIVILEGES ON {db_name}.* TO {db_user}@{db_host} IDENTIFIED BY {db_password};"
    # percona specific
    # grant_db_permissions = f"GRANT ALL PRIVILEGES ON {db_name}.* TO {db_user}@{db_host};"
    flush_db_privileges = "FLUSH PRIVILEGES;"

    recreate_db_queries = f'{mysql_config} -e "{drop_db}{recreate_db}{grant_db_permissions}{flush_db_privileges}"'

    print("Creating database:", db_name)

    os.system(recreate_db_queries)

    print("Await MySQL restart")

    time.sleep(10)

    print("Creating database done:", db_name)


def import_db(db_name, dump_file):
    # Set dump file path
    dump_file_path = f"{dump_path}{dump_file}"

    print("Importing db:", db_name)

    import_db = f"{mysql_config} {db_name} < {dump_file_path}"

    os.system(import_db)

    time.sleep(5)

    print("Import done:", db_name)


def manage_db_import(db_name, dump_file):
    fix_dump_definer(dump_file)
    create_db(db_name)
    import_db(db_name, dump_file)


def main_script():
    try:
        print("--------------------------------------------------------------------------------")
        print("WARNING - This script is used for development purposes only.")
        print("Please don't try roning it on production environment!")
        print("--------------------------------------------------------------------------------")

        # Get db_names and dump_files list length
        db_count = len(db_names)
        dump_count = len(dump_files)

        # Check if lists have the same length
        if db_count != dump_count:
            return "db_names and dump_files must have the same length."

        # e.g. db_count = 11 result will be 100 - 1
        import_all_option = (10 ** ((db_count // 10) + 1)) - 1

        print("Please select one of the options below:")

        for index, dump_file in enumerate(dump_files):
            db_name = db_names[index]

            print(f"{index} - Import {db_name}")

        print(f"{import_all_option} - Import all databases")
        print(f"{import_all_option + 1} - Exit script")

        selected_option = int(input("Select option: "))

        # Exit the script
        if selected_option == import_all_option + 1:
            return "Exiting script."

        # Input MySQL root password
        db_root_password = getpass.getpass(prompt="Enter MySQL root password: ", stream=None)

        # If password exists, modify mysql_config global variable
        if db_root_password:
            global mysql_config
            mysql_config = f"{mysql_config} -p{db_root_password}"

        print("If you continue with this operation existing database(s) will be deleted.")
        continue_import = input("Would you like to continue (y/n)? ")

        if continue_import != "y":
            return "Exiting script."

        if selected_option == import_all_option:
            print("Importing all databases please wait...")

            for index, dump_file in enumerate(dump_files):
                db_name = db_names[index]

                manage_db_import(db_name, dump_file)
        elif selected_option in range(0, db_count):
            db_name = db_names[selected_option]
            dump_file = dump_files[selected_option]

            print(f"Importing {db_name} please wait...")

            manage_db_import(db_name, dump_file)
        else:
            return "Invalid input, exiting script."

        return "DB import finished."
    except Exception as ex:
        print(str(ex))
        return "Something went wrong, exiting script."


# Call the main function
main_script_output = main_script()

print(main_script_output)
