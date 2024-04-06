import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for
from modules.api_request import get_weather
from modules.cache import read_cache, write_cache, remove_expired_cache
from dotenv import load_dotenv


from flask_caching import Cache
# config = {
#     "DEBUG": True,          # some Flask specific configs
#     "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
#     "CACHE_DEFAULT_TIMEOUT": 7200
# }
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('API_SEC_KEY')
git_val = os.getenv('GIT_VAL')
git_key = os.getenv('GIT_KEY')

if git_val is not None and git_key is not None:
    vault_key = git_key + ' ' + git_val
else:
    vault_key=''
#vault_key = os.getenv('GIT_VAL') + os.getenv('GIT_KEY')
# app.config.from_mapping(config)
# cache = Cache(app)


@app.route('/', methods=['GET', 'POST'])
def input_page():
    """
    this function happens when the app first uploads.
    it renders the input.html
    and will redirect to the weather with the location written (if exist)
    :return:
    """
    api_key = os.getenv('VC_API_KEY')
    error = ""
    if request.method == 'POST':
        location = request.form['location']
        remove_expired_cache()
        api_response = read_cache(location)
        if api_response:
            session['api_response_filter'] = api_response
            return redirect(url_for('weather', location=location))
        else:
            api_response = get_weather(location,api_key)
            if api_response:
                remove_expired_cache()
                write_cache(location, api_response)
                session['api_response_filter'] = api_response
                return redirect(url_for('weather', location=location))
            else:
                error = f"{location} was not found"
    return render_template('input.html', error=error, vault_key=vault_key)


@app.route('/weather/<location>', methods=['POST', 'GET'])
def weather(location):
    """
    this function happens when the rout includes: /weather
    it will render the html file with the apo request of the weather.
    """
    data = session.get('api_response_filter')
    return render_template('result.html', location=location, forecast=data[1:], datetime=datetime)


if __name__ == '__main__':
    app.run(debug=True)

