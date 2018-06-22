# TensorFlow Serving client hosted by Flask web framework

Deploy a Tensorflow model and send requests via Flask. The requests are json files with a field 'url' that contains a list with URLs to images. The client will download the images and serve it to the model.

## Pre-Requisites

An exported model from here (https://github.com/marco-willi/camera-trap-classifier)

## Tensorflow-Serving Docker

The first step is to generate a docker image by compiling Tensorflow-Serving. The commands are described in
tensorflow_serving/build_docker.sh

We can compile the CPU version of Tensorflow-Serving to make it deployable on cheap EC2 instances. The compilation can take a few hours to complete.

## Copying the Models

The models have to be copied to the server where this service is being run. The command in docker-compose.yaml has to be adapted such that it points to the model export root directory. Tensorflow Serving automatically switches to new versions of a model if it detects new exports in that directory.

```
--model_base_path=/host/data_hdd/ctc/ss/example/deploy/
```

## Example Request

The server can be tested by running this command on the running instance:

```
# Elephant and Zebra and Lion
curl -X POST -d '{"url": ["https://panoptes-uploads.zooniverse.org/production/subject_location/9e4556a3-5aba-46d0-a932-1f0e9e158d0d.jpeg", "https://s3-eu-west-1.amazonaws.com/pantherabucket1/17_2013/CS38_40185_20130427_101803.jpg","https://static.zooniverse.org/www.snapshotserengeti.org/subjects/standard/50c213e88a607540b9033aed_0.jpg"]}' -H 'Content-Type: application/json' http://0.0.0.0:5000/tf_api/species_client/prediction
```

## Example Response

This is an example response. It would be possible to incorporate the real class-mappings of the model - instead of 'class': 1 it would be 'species': 'Elephant' for example.
 
```
{
    "prediction_result": [
        [
            {
                "prob": 0.9343334436416626,
                "class": 1
            },
            {
                "prob": 0.06039385870099068,
                "class": 0
            },
            {
                "prob": 0.005272689741104841,
                "class": 2
            }
        ],
        [
            {
                "prob": 0.9999719858169556,
                "class": 2
            },
            {
                "prob": 1.4948362149880268e-05,
                "class": 1
            },
            {
                "prob": 1.306723333982518e-05,
                "class": 0
            }
        ],
        [
            {
                "prob": 0.6617377996444702,
                "class": 0
            },
            {
                "prob": 0.24102909862995148,
                "class": 2
            },
            {
                "prob": 0.09723305702209473,
                "class": 1
            }
        ]
    ]
}
```


## Acknowledgements

The code has been forked from here:
https://github.com/Vetal1977/tf_serving_flask_app
