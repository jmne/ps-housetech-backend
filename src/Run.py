from flask import jsonify

from .api import create_app

# create an instance of app
app = create_app()

if __name__ == '__main__':
    # run app on port 8000
    app.run(debug=True, port=8000)


@app.route('/health')
def health():
    resp = jsonify(health="healthy")
    resp.status_code = 200
    return resp
