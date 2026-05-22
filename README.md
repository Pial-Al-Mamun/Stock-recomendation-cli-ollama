
# Stock recommendation CLI (Ollama)

Run everything with Docker (no local Python installs needed).

## Start

1) Start Ollama:

```bash
docker compose up -d ollama
```

2) (First run only) Pull the model inside the Ollama container:

```bash
docker compose exec ollama ollama pull llama3
```

3) Run the CLI app (interactive):

```bash
docker compose run --rm app
```

The CLI container calls Ollama at `http://ollama:11434`.

## Notes

- he default model name is set in `config.py` as `OLLAMA_MODEL = "llama3"`.
- Ollama models are persisted in the `ollama` docker volume.

