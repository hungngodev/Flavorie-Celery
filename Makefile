GCLOUD_PROJECT := flavorie-434420
REPO := flavorie-celery
REGION := us-central1
IMAGE := flavorie-celery
IMAGE_TAG := ${REGION}-docker.pkg.dev/${GCLOUD_PROJECT}/${REPO}/${IMAGE}

all: build push

build:
	@docker build \
		--build-arg MONGO_URI="mongodb+srv://hungngo:Bibo12345@atlascluster.qejat3w.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster" \
		--build-arg REDIS_URL="redis://default:3aYjmSTuNibz866H23fYewQuLJWg4uwg@redis-13354.c244.us-east-1-2.ec2.redns.redis-cloud.com:13354" \
		--build-arg MONGO_DB_NAME="test" \
		-t ${IMAGE_TAG} .

push:
	@docker push ${IMAGE_TAG}

clean:
	@docker rmi -f ${images_name}
