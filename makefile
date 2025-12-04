include .env
export

CONTAINER = qdrant
IMAGE = qdrant/qdrant
DATA_DIR = $(PWD)/qdrant_data

.PHONY: run stop restart logs pull clean

stop:
	@docker rm -f $(CONTAINER) 2>/dev/null || true

run: stop
	@docker image rm -f $(IMAGE) 2>/dev/null || true
	@docker run -d \
	  --name $(CONTAINER) \
	  -p 6333:6333 \
	  -p 6334:6334 \
	  -e QDRANT__SERVICE__API_KEY=$(QDRANT_API_KEY) \
	  -v $(DATA_DIR):/qdrant/storage \
	  $(IMAGE)

restart:
	@$(MAKE) stop
	@docker run -d \
	  --name $(CONTAINER) \
	  -p 6333:6333 \
	  -p 6334:6334 \
	  -e QDRANT__SERVICE__API_KEY=$(QDRANT_API_KEY) \
	  -v $(DATA_DIR):/qdrant/storage \
	  $(IMAGE)

logs:
	@docker logs -f $(CONTAINER)
