images_name := flavorie-celery
repository := hungngodev

all: build push

build:
	@docker build \
		--build-arg MONGO_URI="mongodb+srv://hungngo:Bibo12345@atlascluster.qejat3w.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster" \
		--build-arg REDIS_URL="redis://default:3aYjmSTuNibz866H23fYewQuLJWg4uwg@redis-13354.c244.us-east-1-2.ec2.redns.redis-cloud.com:13354" \
		--build-arg MONGO_DB_NAME="test" \
		-t ${images_name} .

push:
	@echo "push ${repository}/${images_name} to docker hub"
	@docker tag ${images_name} ${repository}/${images_name}
	@docker push ${repository}/${images_name}

clean:
	@docker rmi -f ${images_name}
