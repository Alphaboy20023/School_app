import os


migration_dirs = [
    'accounts_app/migrations',
    'school_app/migrations',
    'admin/migrations',
    'authtoken/migrations',
    'sessions/migrations',
]

for mig_dir in migration_dirs:
    if os.path.exists(mig_dir):
        for filename in os.listdir(mig_dir):
            file_path = os.path.join(mig_dir, filename)
            if filename != '__init__.py' and filename.endswith('.py'):
                print(f"Deleting {file_path}")
                os.remove(file_path)
    else:
        print(f"Directory {mig_dir} does not exist, skipping.")
