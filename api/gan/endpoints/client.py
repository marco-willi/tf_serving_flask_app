import io
import urllib.request as req

from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.gan.logic.tf_serving_client import make_prediction


# create dedicated namespace for model client
ns = api.namespace('model_client', description='Operations for Model client')


@ns.route('/prediction')
class GanPrediction(Resource):
    @ns.doc(description='Predict camera trap images. ' +
            'Return the 5 most probable classe with their probabilities',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    def post(self):
        try:
            req_data = request.get_json()
            print("got req_data: %s" % req_data)
            image_url = req_data['url']
            print("got url: %s" % image_url)
            with req.urlopen(image_url) as url:
                bytes = io.BytesIO(url.read())
                image = bytes.getvalue()

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400

        try:
            results = make_prediction(image)
            print("results is: %s" % results)
            # results is: [(1, 0.9343334436416626), (0, 0.06039385870099068), (2, 0.005272684618830681)]

            results_json = [{'class': res[0], 'prob': res[1]} for res in results]
            return {'prediction_result': results_json}, 200

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500
