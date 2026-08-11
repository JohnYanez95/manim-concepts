.DEFAULT_GOAL := help
.PHONY: help venv hooks lint fmt test check list render render-all clean clean-drafts

# Resolutions treated as throwaway by `clean-drafts` — everything below the
# 1080p default. Kept as a list rather than inlined so adding a tier is a
# one-word change.
DRAFT_RES := 480p15 720p30

# Every concept module in the repo. The `_manim.py` suffix is what makes this
# glob unambiguous — topic directories also hold READMEs and, eventually,
# helper modules that are not themselves renderable.
CONCEPTS := $(wildcard */*_manim.py)

# Overridable on the command line: make render FILE=... QUALITY=draft SCENE=Name
QUALITY ?= high
SCENE   ?=

help:  ## Show available targets
	@grep -hE '^[a-z-]+:[[:space:]]+## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":[[:space:]]+## "}{printf "  %-12s %s\n", $$1, $$2}'

venv:  ## Build the environment from the lockfile (matches a clean checkout)
	uv sync --locked

hooks:  ## Install the pre-commit gate
	uv run pre-commit install

lint:  ## Ruff check (PEP 8)
	uv run ruff check .

fmt:  ## Ruff format
	uv run ruff format .

test:  ## Run the test suite
	uv run pytest -q

check:  ## Everything the pre-commit gate runs, plus tests, without committing
	uv run ruff check .
	uv run ruff format --check .
	uv run pytest -q
	uv run pre-commit run --all-files

list:  ## List every concept module and the scenes it defines
	@for f in $(CONCEPTS); do \
		echo "$$f"; \
		out=$$(uv run python "$$f" --list) || exit 1; \
		echo "$$out" | sed 's/^/    /'; \
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

clean-drafts:  ## Delete sub-1080p renders, keeping the final ones
	@found=$$(find media -type d \( $(foreach r,$(DRAFT_RES),-name '$(r)' -o) -false \) 2>/dev/null); \
	if [ -z "$$found" ]; then \
		echo "no draft renders to clear"; \
	else \
		echo "$$found" | sed 's/^/  removing /'; \
		echo "$$found" | xargs rm -rf; \
	fi
	@echo "drafts cleared; 1080p60 and 4K renders kept"

clean:  ## Delete all rendered output, drafts and finals alike
	rm -rf media/
