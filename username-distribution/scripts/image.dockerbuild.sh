TAG=${TAG:-latest}
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path/.."
echo "Building code in $(pwd) with docker"
# Build local source code using docker
docker build -t username-distribution:$TAG -f scripts/Dockerfile .
