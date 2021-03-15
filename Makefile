MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

# all targets are phony
.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')


#.PHONY: run test clean help

run: ## run the program
	export INPUTDIR=data;python3 run.py

testrun: ## test run the program
	export INPUTDIR=tests;python3 run.py

test: ## Do the test
	# discover: tests directory 内のtest群を実行する。
	# -v verbose mode で実行する。
	# --locals トレースパック時のローカル変数を出力する。
	python3 -m unittest discover tests -v --locals

clean: ## Clean up mess
	rm -rf __pycache__
	rm -rf .mypy_cache
#	rm -rf ~/.pylint.d
	rm OpenBadgeBake.log
	rm -rf tests/__pycache__
	rm -rf output/*


help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
