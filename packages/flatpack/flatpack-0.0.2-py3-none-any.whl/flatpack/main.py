import requests
import sys

def fetch_github_dirs():
    url = "https://api.github.com/repos/romlingroup/flatpack-ai/contents/warehouse"
    response = requests.get(url)
    if response.status_code != 200:
        return ["Error fetching data from GitHub"]
    data = response.json()
    directories = [item['name'] for item in data if item['type'] == 'dir']
    return sorted(directories)

def list():
    dirs = fetch_github_dirs()
    return "\n".join(dirs)

def main():
    if len(sys.argv) < 2:
        print("Usage: flatpack.ai <command>")
        print("Available commands: help, list, test")
        return

    command = sys.argv[1]
    if command == "help":
        print("[HELP]")
    elif command == "list":
        print(list())
    elif command == "test":
        print("[TEST]")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
