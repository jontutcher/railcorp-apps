IMAGE ?= reg.jtut.io/departures:01-multistage-before
PLATFORMS ?= linux/amd64,linux/arm64

.PHONY: run lock image push

run:
	uv run python app.py

lock:
	uv lock

image:
	docker buildx build --load -t $(IMAGE) .

push:
	docker buildx build --platform $(PLATFORMS) --sbom=true --provenance=true --push -t $(IMAGE) .
