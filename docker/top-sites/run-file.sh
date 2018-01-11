DOCKER_TAG=python3:latest
DOCKER_NAME=top-sites

SERVICE=10006
GIT_REPO=https://github.com/deeso/top-sites-check.git
TMP_DIR=tmp-git
BASE_DIR=$TMP_DIR
CONFIGS_DIR=$BASE_DIR/configs/

CONF_FILE=$CONFIGS_DIR/remote-config.toml
HOST_FILE=$CONFIGS_DIR/hosts

MAINS_DIR=$BASE_DIR/mains/
MAIN=$MAINS_DIR/run-all-multiprocess.py

git clone $GIT_REPO $TMP_DIR
DOCKER_ADD_HOST=
#MONGODB_HOST=$(cat $HOST_FILE | grep "mongodb-host")
#DOCKER_ADD_HOST="--add-host $MONGODB_HOST "
cp $MAIN main.py
cp $CONF_FILE config.toml
# hack
mkdir package
cp -r $BASE_DIR/src package/
cp -r $BASE_DIR/setup.py package/

# cleaup Docker
docker kill $DOCKER_NAME
docker rm $DOCKER_NAME

# setup dirs
DOCKER_BASE=/data
DOCKER_NB=$DOCKER_BASE/$DOCKER_NAME
DOCKER_LOGS=$DOCKER_NB/logs
DOCKER_DATA=$DOCKER_NB/data

DOCKER_PORTS="-p $SERVICE:$SERVICE"
DOCKER_ENV=""
DOCKER_VOL=""

mkdir -p $DOCKER_DATA
mkdir -p $DOCKER_LOGS
chmod -R a+rw $DOCKER_NB

# TODO comment below if you want to save to Mongo
echo "python main.py -config config.toml " > python_cmd.sh


cat python_cmd.sh

docker build --no-cache -t $DOCKER_TAG .

# clean up here
rm -fr config.toml python_cmd.sh main.py tmp-git package

# run command not 
echo "docker run $DOCKER_PORTS $DOCKER_VOL -it $DOCKER_ENV \
           --name $DOCKER_NAME $DOCKER_TAG"

docker run -d $DOCKER_ADD_HOST $DOCKER_PORTS $DOCKER_VOL -it $DOCKER_ENV \
           --name $DOCKER_NAME $DOCKER_TAG
