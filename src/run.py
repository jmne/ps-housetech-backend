from flask import jsonify
from flask import redirect

from .api import create_app

# create an instance of app
app = create_app()

if __name__ == '__main__':
    # run app on port 8000
    app.run(debug=True, port=8000)


@app.route('/api/health-check-flask')
def health():  # dead: disable
    """Return health status of the API."""
    resp = jsonify(status='Running')
    resp.status_code = 200

    return resp


@app.route('/api')
def redirect_to_docs():  # dead: disable
    """Redirect to API documentation."""
    return redirect(
        'https://ml-de.zivgitlabpages.uni-muenster.de/teaching/ps-housetech/ps-housetech-website/api/einleitung',  # noqa: E501
        # noqa: E501
        code=302,
    )


@app.route('/api/help', methods=['GET'])
def help():  # dead: disable
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)
