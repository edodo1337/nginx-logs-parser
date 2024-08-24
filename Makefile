.PHONY: install_deps setup_precommit

install_deps:
	@echo "Installing dependencies..."
	curl -sSf https://rye.astral.sh/get | bash
	rye sync

setup_precommit:
	@echo "Setting up pre-commit hooks..."
	pre-commit install

format-ruff:
	ruff check --fix

lint:
	-ruff check .
	-mypy .

test:
	pytest -rf --disable-warnings .
	