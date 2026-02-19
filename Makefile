VACCINES_FIXTURE = vaccines/fixtures/petvaxx_seed_data_fixture.json
PETS_FIXTURE = pets/fixtures/pets_data.json
PLANNER_FIXTURE = planner/fixtures/plans_and_doses.json

.PHONY: all load-vaccines load-pets load-planner load-all

all: load-all

load-vaccines:
	python manage.py loaddata $(VACCINES_FIXTURE)

load-pets:
	python manage.py loaddata $(PETS_FIXTURE)

load-planner:
	python manage.py loaddata $(PLANNER_FIXTURE)

load-all: load-vaccines load-pets load-planner
