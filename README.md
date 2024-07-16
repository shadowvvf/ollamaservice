# Ollama Client

This project provides a Python-based client for interacting with Ollama, an AI model server. It includes a command-line interface for easy interaction.

[![](https://github-readme-stats.vercel.app/api/pin/?username=shadowvvf&repo=ollamaservice)](https://github.com/anuraghazra/github-readme-stats)

## Features

- Remote server support
- CLI mode for interactive use
- Commands for model management (list, pull, push, delete, create)
- Text generation and chat capabilities
- Model information retrieval

## Installation

To use this client, you need to have Python installed on your system. Clone this repository and install the required dependencies:

```
git clone https://github.com/shadowvvf/ollamaservice
cd ollamaservice
pip install -r requirements.txt
```

## Usage

You can run the client in CLI mode or use it as a library in your Python projects.

### CLI Mode

To start the CLI mode:

```
python ollamaservice.py --cli
```

By default, it connects to `http://localhost:11434`. To connect to a different Ollama server:

```
python ollamaservice.py --cli --host http://your-ollama-server:11434
```

### Commands

Here are some example commands you can use:

1. List available models:
   ```
   ollama> list
   ```
   or
   ```
   python3 ollamaservice.py --list
   ```

2. Pull a model:
   ```
   ollama> pull llama2
   ```
   or
   ```
   python3 ollamaservice.py --pull llama2
   ```
   (in other examples its same with cli mode and just arguments)

3. Generate text:
   ```
   ollama> generate llama2 "Write a haiku about programming"
   ```

4. Chat with a model:
   ```
   ollama> chat llama2 "Explain quantum computing in simple terms"
   ```

5. Show model information:
   ```
   ollama> show llama2
   ```

6. Create a new model:
   ```
   ollama> create mymodel path/to/modelfile
   ```

7. Delete a model:
   ```
   ollama> delete mymodel
   ```

8. Push a model:
   ```
   ollama> push mymodel
   ```

9. Exit the CLI:
   ```
   ollama> exit
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
