"""flask封装

参考：
1. https://flask.palletsprojects.com/en/2.3.x/quickstart/
2. https://github.com/flasgger/flasgger
3. https://pypi.org/project/prometheus-flask-exporter/
"""
from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
from prometheus_flask_exporter import PrometheusMetrics
import logging

app = Flask(__name__)
swagger = Swagger(app)
metrics = PrometheusMetrics(app)

error_codes = {
    "SUCCESS": '0',
    "SERVICE_UNKOWN_EXCEPTION": '500',
    "REFRESH_TOPICS_EXCEPTION": '11001'
}

@app.errorhandler(404)
def page_not_found(error):
    return {'state': error_codes["SERVICE_UNKOWN_EXCEPTION"]}

@app.errorhandler(500)
def not_found(error):
    return {'state': error_codes["SERVICE_UNKOWN_EXCEPTION"]}


def run(application_name, version = "0.0.1", host = "0.0.0.0", port = 8080, debug = False):
    """启动服务
    http服务集成了swagger和prometheus
    
    http服务约定：

    1. rest风格，并且返回{state: "code码", msg: "描述", data: any}


    ----
    Args:
      application_name: 应用名
      version: 应用版本号
      port: 端口号
      debug: debug模式
    """      

    # static information as metric
    metrics.info(application_name, application_name, version = version)
    logging.info(f"http服务启动, application: {application_name}, version: {version}")
    logging.info(f"使用 http://127.0.0.1:{port}/apidocs 查看服务接口")
    logging.info(f"使用 http://127.0.0.1:{port}/metrics 查看应用指标")
    app.run(debug = debug, host = host, port = port)


