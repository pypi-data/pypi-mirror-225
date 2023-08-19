.DEFAULT_GOAL := help

.PHONY: help
help: 
	@echo "\n * push-to-pypi"
	@echo "\n"

.PHONY: push-to-pypi
push-to-pypi: 
	-rm -r dist/* 
	bumpversion --allow-dirty patch pyproject.toml
	python3 -m build
	python3 -m twine upload --repository pypi dist/* --username __token__ --password "pypi-AgEIcHlwaS5vcmcCJGEwYjUyMTMzLWJhNzUtNDA5YS05ZDZlLWViNmYyZDMzZTIxMwACFVsxLFsiZHJlYW0taGVscGVycyJdXQACLFsyLFsiMjdjZWE3NmQtMTUyNS00YTU4LTg2ZmQtMzg3NDY0YjI2NWNkIl1dAAAGIJ1vSRGdwq6YW4PRtV8HBmV48PV7gE-WRdky0aPGFRaR"

.PHONY: update-component
update-component: 
	@echo "\n || Remember to export KFPLIBCOMPONENT=xxx ||"
	make push-to-pypi
	sleep 10
	(cd ../dream-kfp-components && make build-component)