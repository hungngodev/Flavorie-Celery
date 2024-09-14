GCLOUD_PROJECT := flavorie-434420
REPO := flavorie-celery
REGION := us-central1
IMAGE := flavorie-celery
IMAGE_TAG := ${REGION}-docker.pkg.dev/${GCLOUD_PROJECT}/${REPO}/${IMAGE}
REPO := hungngodev/flavorie-celery

all: build push

all_gcr: build_gcr push_to_gcr

build:
	@docker build \
		--build-arg MONGO_URI="mongodb+srv://hungngo:Bibo12345@atlascluster.qejat3w.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster" \
		--build-arg REDIS_URL="redis://default:3aYjmSTuNibz866H23fYewQuLJWg4uwg@redis-13354.c244.us-east-1-2.ec2.redns.redis-cloud.com:13354" \
		--build-arg MONGO_DB_NAME="test" \
		-t ${REPO} .

build_gcr:
	@docker build \
		--build-arg MONGO_URI="mongodb+srv://hungngo:Bibo12345@atlascluster.qejat3w.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster" \
		--build-arg REDIS_URL="redis://default:3aYjmSTuNibz866H23fYewQuLJWg4uwg@redis-13354.c244.us-east-1-2.ec2.redns.redis-cloud.com:13354" \
		--build-arg MONGO_DB_NAME="test" \
		-t ${IMAGE_TAG} .

push:
	@docker push ${REPO}

clean:
	@docker rmi -f ${images_name}

run:
	@docker run --cpus="5.0" --memory="16g" --shm-size="64g" -d ${IMAGE_TAG}

push_to_gcr:
	@gcloud auth configure-docker
	@docker push ${IMAGE_TAG}