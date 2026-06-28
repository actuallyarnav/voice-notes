RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"


def write_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)
        print("file saved!")


def log_info(text):
    print(f"{BLUE}[INFO]: {text}{RESET}")


def log_success(text):
    print(f"{GREEN}[SUCCESS]: {text}{RESET}")


def log_fail(text):
    print(f"{RED}[FAIL]: {text}{RESET}")
