from flask import jsonify


def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404


def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# class WeatherDataError(Exception):
#     def __init__(self, message):
#         self.message = message
#
#     def __str__(self):
#         return f'WeatherDataError: {self.message}'
