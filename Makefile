.DEFAULT_GOAL := help
.PHONY: help venv hooks lint fmt check list render render-all clean

# Every concept module in the repo. The `_manim.py` suffix is what makes this
# glob unambiguous — topic directories also hold READMEs and, eventually,
# helper modules that are not themselves renderable.
CONCEPTS := $(wildcard */*_manim.py)

# Overridable on the command line: make render FILE=... QUALITY=draft SCENE=Name
QUALITY ?= high
SCENE   ?=

help:  ## Show available targets
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-12s %s\n", $$1, $$2}'

venv:  ## Build the environment from the lockfile (matches a clean checkout)
	uv sync --locked

hooks:  ## Install the pre-commit gate
	uv run pre-commit install

lint:  ## Ruff check (PEP 8)
	uv run ruff check .

fmt:  ## Ruff format
	uv run ruff format .

check:  ## Everything the pre-commit gate runs, without committing
	uv run ruff check .
	uv run ruff format --check .
	uv run pre-commit run --all-files

list:  ## List every concept module and the scenes it defines
	@for f in $(CONCEPTS); do \
		echo "$$f"; \
		uv run python "$$f" --list | sed 's/^/    /'; \
	done

render:  ## Render one module: make render FILE=topic/x_manim.py [QUALITY=] [SCENE=]
	@[ -n "$(FILE)" ] || { \
		echo "usage: make render FILE=<topic>/<concept>_manim.py [QUALITY=draft|medium|high|4k] [SCENE=Name]"; \
		echo "available:"; \
		for f in $(CONCEPTS); do echo "    $$f"; done; \
		exit 2; \
	}
	uv run python $(FILE) --quality $(QUALITY) $(if $(SCENE),--scene $(SCENE))

render-all:  ## Render every concept module (QUALITY=draft for a fast sweep)
	@for f in $(CONCEPTS); do \
		echo "== $$f"; \
		uv run python "$$f" --quality $(QUALITY) || exit 1; \
	done

clean:  ## Delete all rendered output
	rm -rf media/
