PYTHON ?= python
.PHONY: reproduce quick setup serve clean corpus
reproduce:
	$(PYTHON) reproduce.py
quick:
	$(PYTHON) reproduce.py --quick
corpus:
	$(PYTHON) reproduce.py --rebuild-corpus
setup:
	Rscript bench/install_r_packages.R
	$(PYTHON) -m pip install -r requirements.txt
	npm ci
	npx playwright install chromium
serve:
	$(PYTHON) -m http.server 8080
clean:
	rm -rf results outputs
