
# Makefile for Person Matcher AI

APP_NAME = person-matcher
PORT = 8501

.PHONY: build dev prod clean

# 🔨 Build the Docker image
build:
	docker build -t $(APP_NAME) .

# 🚀 Development mode (mount local code for live reload)
dev:
	mkdir -p data/labels
	docker run -it --rm \
		-p $(PORT):8501 \
		-v $(PWD):/app \
		$(APP_NAME)

# 🏗️ Production mode (use image's baked-in code)
prod:
	docker run -it --rm \
		-p $(PORT):8501 \
		$(APP_NAME)

# 🧹 Clean all containers/images related to the app
clean:
	docker container prune -f
	docker image rm -f $(APP_NAME) || true