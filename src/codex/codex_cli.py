import argparse
import sys
from codex.kernel import Kernel

def main():
    """Artemis-City Kernel CLI Entry Point"""
    parser = argparse.ArgumentParser(description="Artemis-City Kernel CLI")
    parser.add_argument("command", nargs="?", help="The command string to execute")
    parser.add_argument("--plan", help="Path to a plan file to execute")
    
    args = parser.parse_args()
    
    # Initialize Kernel
    try:
        kernel = Kernel()
    except Exception as e:
        print(f"Fatal: Kernel failed to boot. {e}")
        sys.exit(1)
    
    if args.command:
        # One-shot command
        request = {"type": "command", "content": args.command}
        result = kernel.process(request)
        print(result)
    elif args.plan:
        # Execute plan
        request = {"type": "exec", "path": args.plan}
        result = kernel.process(request)
        print(result)
    else:
        # Interactive mode
        print("Welcome to Artemis-City Codex (Kernel v1.0)")
        print("Type 'exit' to quit.")
        while True:
            try:
                cmd = input("codex> ")
                if cmd.strip().lower() in ["exit", "quit"]:
                    break
                if not cmd.strip():
                    continue
                
                request = {"type": "command", "content": cmd}
                result = kernel.process(request)
                print(result)
            except KeyboardInterrupt:
                print("\nGoodbye.")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
