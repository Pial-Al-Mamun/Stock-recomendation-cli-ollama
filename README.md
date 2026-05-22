
# Stock recommendation CLI (Ollama)

Run everything with Docker (no local Python installs needed).

## Start

1) Start Ollama:

```bash
docker compose up -d ollama
```

2) Run the CLI app (interactive):

```bash
docker compose run --rm app
```

The CLI container calls Ollama at `http://ollama:11434`.  
**Note:** On first run, the app will automatically pull the configured model (this takes a few minutes).

## Notes

- The default model name is set in `config.py` as `OLLAMA_MODEL = "llama3"`.
- Ollama models are persisted in the `ollama` docker volume.

