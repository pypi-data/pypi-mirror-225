# llmeval

LLM evaluation and test framework to build internal test harnesses and automate reliable deployment workflows

## Prerequisite Software

- `pdm` - `pip install pdm`

## Development

1. Run `pdm sync` to install all dependencies managed by pdm tool.
   - If you need to add new dependency, run `pdm add [dependency-name]`.
1. Run `python llmeval/main.py` for the cli.
1. Run `python llmeval/main.py eval hydra.mode=MULTIRUN` for evaluation.

## Format files

1. Run `black llmeval` to format all the py files.

## Build & Publish

1. Run `pdm build`
1. Run `pdm publish`
