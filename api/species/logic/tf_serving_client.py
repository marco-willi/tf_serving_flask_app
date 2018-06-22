from __future__ import print_function

import operator
import logging
import settings
import utils
import tensorflow as tf

# Communication to TensorFlow server via gRPC
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2


log = logging.getLogger(__name__)


def __get_tf_server_connection_params__():
    '''
    Returns connection parameters to TensorFlow Server

    :return: Tuple of TF server name and server port
    '''
    server_name = utils.get_env_var_setting('TF_SERVER_NAME', settings.DEFAULT_TF_SERVER_NAME)
    server_port = utils.get_env_var_setting('TF_SERVER_PORT', settings.DEFAULT_TF_SERVER_PORT)

    return server_name, server_port


def __create_prediction_request__(image):
    '''
    Creates prediction request to TensorFlow server for GAN model

    :param: Byte array, image for prediction
    :return: PredictRequest object
    '''
    # create predict request
    request = predict_pb2.PredictRequest()
    #log.debug("Image is: %s" % image[0:50])

    # Call model to make prediction on the image
    request.model_spec.name = settings.SPECIES_MODEL_NAME
    request.model_spec.signature_name = settings.SPECIES_MODEL_SIGNATURE_NAME
    request.inputs[settings.SPECIES_MODEL_INPUTS_KEY].CopyFrom(
        tf.contrib.util.make_tensor_proto(image, dtype=tf.string))

    return request


def __open_tf_server_channel__(server_name, server_port):
    '''
    Opens channel to TensorFlow server for requests

    :param server_name: String, server name (localhost, IP address)
    :param server_port: String, server port
    :return: Channel stub
    '''
    channel = implementations.insecure_channel(
        server_name,
        int(server_port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    return stub


def __make_prediction_and_prepare_results__(stub, request):
    '''
    Sends Predict request over a channel stub to TensorFlow server

    :param stub: Channel stub
    :param request: PredictRequest object
    :return: List of tuples, 3 most probable digits with their probabilities
    '''
    result = stub.Predict(request, 60.0)  # 60 secs timeout
    print("Result is %s" % result)
    print("Result outputs are %s" % result.outputs)

    res = result.outputs[settings.SPECIES_MODEL_OUTPUT_KEY]
    print("res is %s" % res)
    probs = res.float_val
    print("Probs are: %s" % probs)
    # Probs label/class: [0.06039385870099068, 0.9343334436416626, 0.005272684618830681]

    value_dict = {idx: prob for idx, prob in enumerate(probs)}
    sorted_values = sorted(
        value_dict.items(),
        key=operator.itemgetter(1),
        reverse=True)
    n_values = min([len(sorted_values), 5])

    return sorted_values[0:n_values]


def make_prediction(image):
    '''
    Predict the house number on the image using GAN model

    :param image: Byte array, images for prediction
    :return: List of tuples, 3 most probable digits with their probabilities
    '''
    # get TensorFlow server connection parameters
    server_name, server_port = __get_tf_server_connection_params__()
    log.info('Connecting to TensorFlow server %s:%s', server_name, server_port)

    # open channel to tensorflow server
    stub = __open_tf_server_channel__(server_name, server_port)

    # create predict request
    request = __create_prediction_request__(image)

    # make prediction
    return __make_prediction_and_prepare_results__(stub, request)
