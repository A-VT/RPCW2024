from TPC6.app.server import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/test', methods=['GET'])
def test():
    return 'it works!'
