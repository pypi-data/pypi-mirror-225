# Author: Chen Wang

def ignore_files(filename):
    if not filename or filename == "":
        return True
    ignore_prefixes = ["/sys/", "/proc", "/etc/", "stdout", "stderr", "stdin"]
    for prefix in ignore_prefixes:
        if filename.startswith(prefix):
            return True
    if "pipe:" in filename:
        return True

    return False