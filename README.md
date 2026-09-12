# know-your-llm

A small Python tool that checks your hardware and tells you which LLMs you can actually run on your machine.

I built this because I kept seeing people recommend models without any context on whether your PC can handle them. This just looks at your specs and gives you a straight answer.

## What it checks

- RAM
- Storage
- GPU (NVIDIA only for now)
- CPU cores and frequency

## Usage

```bash
uv run main.py
```

## Requirements

- Python 3.13+
- NVIDIA GPU recommended (CPU inference works but is slow)

## Status

Work in progress - the recommendation logic is coming next.
