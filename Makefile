PYTHON = python
MANAGE = $(PYTHON) manage.py
LOAD = $(MANAGE) loaddata

VACCINES_FIXTURE = vaccines/fixtures/petvaxx_seed_data_fixture.json
PETS_FIXTURE = pets/fixtures/pets_data.json
PLANNER_FIXTURE = planner/fixtures/plans_and_doses.json

.PHONY: all load-vaccines load-pets load-planner load-all

all: load-all

load-vaccines:
	$(LOAD) $(VACCINES_FIXTURE)

load-pets:
	$(LOAD) $(PETS_FIXTURE)

load-planner:
	$(LOAD) $(PLANNER_FIXTURE)

load-all: load-vaccines load-pets load-planner
