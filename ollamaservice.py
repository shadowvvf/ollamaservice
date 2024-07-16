import argparse
import ollama
from ollama import Client
import cmd
import sys

class OllamaCLI(cmd.Cmd):
    prompt = 'ollama> '
    
    def __init__(self, client):
        super().__init__()
        self.client = client

    def do_chat(self, arg):
        """Chat with a model: chat <model> <prompt>"""
        args = arg.split(maxsplit=1)
        if len(args) != 2:
            print("Usage: chat <model> <prompt>")
            return
        model, prompt = args
        try:
            response = self.client.chat(model=model, messages=[{"role": "user", "content": prompt}])
            print(response['message']['content'])
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")

    def do_generate(self, arg):
        """Generate text: generate <model> <prompt>"""
        args = arg.split(maxsplit=1)
        if len(args) != 2:
            print("Usage: generate <model> <prompt>")
            return
        model, prompt = args
        try:
            response = self.client.generate(model=model, prompt=prompt)
            print(response['response'])
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")

    def do_list(self, arg):
        """List available models"""
        try:
            models = self.client.list()
            for model in models['models']:
                print(f"Name: {model['name']}, Size: {model['size']}, Modified: {model['modified_at']}")
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")

    def do_pull(self, arg):
        """Pull a model: pull <model>"""
        if not arg:
            print("Usage: pull <model>")
            return
        try:
            self.client.pull(arg)
            print(f"Successfully pulled model: {arg}")
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")

    def do_push(self, arg):
        """Push a model: push <model>"""
        if not arg:
            print("Usage: push <model>")
            return
        try:
            self.client.push(arg)
            print(f"Successfully pushed model: {arg}")
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")

    def do_create(self, arg):
        """Create a model: create <model> <modelfile>"""
        args = arg.split(maxsplit=1)
        if len(args) != 2:
            print("Usage: create <model> <modelfile>")
            return
        model, modelfile = args
        try:
            self.client.create(model=model, modelfile=modelfile)
            print(f"Successfully created model: {model}")
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")

    def do_delete(self, arg):
        """Delete a model: delete <model>"""
        if not arg:
            print("Usage: delete <model>")
            return
        try:
            self.client.delete(arg)
            print(f"Successfully deleted model: {arg}")
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")

    def do_show(self, arg):
        """Show information for a model: show <model>"""
        if not arg:
            print("Usage: show <model>")
            return
        try:
            info = self.client.show(arg)
            print(f"Model information for {arg}:")
            print(info)
        except ollama.ResponseError as e:
            print(f"Error: {e.error}")

    def do_exit(self, arg):
        """Exit the CLI"""
        print("Goodbye!")
        return True

    def do_quit(self, arg):
        """Exit the CLI"""
        return self.do_exit(arg)

def main():
    parser = argparse.ArgumentParser(description="Ollama client with remote server support and CLI mode")
    parser.add_argument("--host", default="http://localhost:11434", help="Ollama server host (default: http://localhost:11434)")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    args = parser.parse_args()

    client = Client(host=args.host)

    if args.cli:
        print("Ollama CLI Mode")
        print("Type 'help' for a list of commands or 'exit' to quit.")
        OllamaCLI(client).cmdloop()
    else:
        print("For CLI mode, use the --cli flag")
        print("Usage: python ollama_client.py --cli")
        sys.exit(1)

if __name__ == "__main__":
    main()

