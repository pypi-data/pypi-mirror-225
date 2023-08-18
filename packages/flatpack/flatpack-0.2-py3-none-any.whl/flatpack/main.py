import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: flatpack <command>")
        print("Available commands: help, list, test")
        return

    command = sys.argv[1]
    if command == "help":
        print(help())
    elif command == "list":
        print(list())
    elif command == "test":
        print(test())
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
