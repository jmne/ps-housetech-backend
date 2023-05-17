from api import create_app
from flask import jsonify
from flask import redirect

# create an instance of app
app = create_app()

if __name__ == '__main__':
    # run app on port 8000
    app.run(debug=True, port=8000)


@app.route('/api/health-check')
def health():  # dead: disable
    """Return health status of the API."""
    resp = jsonify(health='healthy')
    resp.status_code = 200

    return resp


@app.route('/api')
def redirect_to_docs():  # dead: disable
    """Redirect to API documentation."""
    return redirect(
        'https://ml-de.zivgitlabpages.uni-muenster.de/teaching/\
        ps-housetech/ps-housetech-website/api',
        code=302,
    )
