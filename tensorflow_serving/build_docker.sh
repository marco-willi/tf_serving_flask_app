""" Build Tensorflow Serving Docker """
git clone https://github.com/tensorflow/serving.git
cd ./serving/tensorflow_serving/tools/docker/

# OPTIONAL: Optimized build - Use Dockerfile.devel and adjust compile flags
# bazel build -c opt --copt=-msse4.1 --copt=-msse4.2 tensorflow_serving/...
# sudo docker build --pull -t $USER/tensorflow-serving-devel-cpu -f Dockerfile.devel .

# Modify the Dockerfile to remove the entrypoint
# add this CMD ["/bin/bash"] (like in the Dockerfile.devel)
sudo docker build --pull -t $USER/tensorflow-serving-devel-cpu -f Dockerfile .

sudo docker run -it -p 9000:9000 $USER/tensorflow-serving-devel-cpu /bin/bash
