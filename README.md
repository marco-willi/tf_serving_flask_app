# TensorFlow Serving client hosted by Flask web framework

Deploy a Tensorflow model and send requests via Flask. The requests are json files with a field 'url' that contains
a URL to an image. The client will download the image and serve it to the model.

## Pre-Requisites

An exported model from here (https://github.com/marco-willi/camera-trap-classifier)

## Tensorflow-Serving Docker

The first step is to generate a docker image by compiling Tensorflow-Serving. The commands are described in
tensorflow_serving/build_docker.sh

We compile the CPU version of Tensorflow-Serving to make it deployable on cheap EC2 instances. The compilation can
take a few hours to complete.

## Copying the Models

The models have to be copied to the server where this service is being run. The command in docker-compose.yaml has to
be adapted such that it points to the model export root directory. Tensorflow Serving automatically switches to new
versions of a model if it detects new exports in that directory.

```
--model_base_path=/host/data_hdd/ctc/ss/example/deploy/
```

## Send a Request

The server can be tested by running this command on the running instance:

```
curl -X POST -d '{"url": "https://static.zooniverse.org/www.snapshotserengeti.org/subjects/standard/50c213e88a607540b9033aed_0.jpg"}' -H 'Content-Type: application/json' http://0.0.0.0:5000/tf_api/species_client/prediction
```



## Acknowledgements

The code has been forked from here:
https://github.com/Vetal1977/tf_serving_flask_app
