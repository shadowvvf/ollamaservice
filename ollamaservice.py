import argparse
import ollama
from ollama import Client
import cmd
import sys
import urllib.parse

class OllamaCLI(cmd.Cmd):
    def __init__(self, client, host):
        super().__init__()
        self.client = client
        self.host = host
        self.update_prompt()

    def update_prompt(self):
        if self.host == "http://localhost:11434":
            self.prompt = 'ollama> '
        else:
            parsed_url = urllib.parse.urlparse(self.host)
            self.prompt = f'{parsed_url.hostname}> '

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

def execute_command(client, command, model=None, prompt=None, modelfile=None):
    try:
        if command == "chat":
            if not model or not prompt:
                raise ValueError("Both model and prompt are required for chat command")
            response = client.chat(model=model, messages=[{"role": "user", "content": prompt}])
            print(response['message']['content'])

        elif command == "generate":
            if not model or not prompt:
                raise ValueError("Both model and prompt are required for generate command")
            response = client.generate(model=model, prompt=prompt)
            print(response['response'])

        elif command == "list":
            models = client.list()
            for model in models['models']:
                print(f"Name: {model['name']}, Size: {model['size']}, Modified: {model['modified_at']}")

        elif command == "pull":
            if not model:
                raise ValueError("Model is required for pull command")
            client.pull(model)
            print(f"Successfully pulled model: {model}")

        elif command == "push":
            if not model:
                raise ValueError("Model is required for push command")
            client.push(model)
            print(f"Successfully pushed model: {model}")

        elif command == "create":
            if not model or not modelfile:
                raise ValueError("Both model and modelfile are required for create command")
            client.create(model=model, modelfile=modelfile)
            print(f"Successfully created model: {model}")

        elif command == "delete":
            if not model:
                raise ValueError("Model is required for delete command")
            client.delete(model)
            print(f"Successfully deleted model: {model}")

        elif command == "show":
            if not model:
                raise ValueError("Model is required for show command")
            info = client.show(model)
            print(f"Model information for {model}:")
            print(info)

    except ollama.ResponseError as e:
        print(f"Error: {e.error}")
        print(f"Status code: {e.status_code}")

def main():
    parser = argparse.ArgumentParser(description="Ollama client with remote server support and CLI mode")
    parser.add_argument("--host", default="http://localhost:11434", help="Ollama server host (default: http://localhost:11434)")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("command", nargs="?", choices=["chat", "generate", "list", "pull", "push", "create", "delete", "show"], help="Ollama command to execute")
    parser.add_argument("--model", help="Model name for relevant commands")
    parser.add_argument("--prompt", help="Prompt for chat or generate commands")
    parser.add_argument("--modelfile", help="Modelfile content for create command")
    args = parser.parse_args()

    client = Client(host=args.host)

    if args.cli:
        print("Ollama CLI Mode")
        print("Type 'help' for a list of commands or 'exit' to quit.")
        OllamaCLI(client, args.host).cmdloop()
    elif args.command:
        execute_command(client, args.command, args.model, args.prompt, args.modelfile)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
