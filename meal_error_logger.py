def log_error(file: str, error_msg):
    with open(file, 'a') as f:
        f.write(f"{error_msg}\n")