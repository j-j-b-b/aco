from flask import Flask, render_template, jsonify, make_response
import main
from flask_sse import sse
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')
cors = CORS(app)  # 解决跨域问题


@app.route('/')
def index():
    main.new()
    return render_template('index.html')


@app.route('/canvas')
def canvas():
    list_json, shortest_distance = main.search_path()
    sse.publish({"status": 200, "best_path": list_json, "shortest_distance": shortest_distance}, type='greeting')
    sse.publish({"gogogo":list_json}, type='go')
    return render_template('canvas.html')



@app.route('/api/json', methods=['GET', 'POST'])
def api_json():
    list_json, shortest_distance = main.search_path()
    return jsonify({
        "distance_x_y": list_json,
        "shortest_distance": shortest_distance
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6379, threaded=True)
