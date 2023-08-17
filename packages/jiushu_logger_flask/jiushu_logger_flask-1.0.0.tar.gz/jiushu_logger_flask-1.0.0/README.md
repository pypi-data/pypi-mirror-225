![logo.png](logo.png)

# jiushu-logger-flask【九书 Flask 路由专用】

## 简介

JF 专用格式化 logger 的 Flask 路由特供版，专门输出请求日志。

## 使用方法

```python
import orjson
from flask import Flask, g

from jiushu_logger_flask import RouteLogging

app = Flask(__name__)

# Logging for routes.
# You can set which route should be skipped, 
#   or which pattern the route matches should be skipped.
RouteLogging(app,
             skip_routes=['/api/health'],
             skip_regexes=[r'''^.*skip.*$'''])


@app.get('/api/test')
def _test():
    # You can get trace id of *this* request.
    # If apache-skywalking is used, this trace_id will be the ID tracing by skywalking.
    print(g.trace_id)
    return b'Hello, world!', 200


@app.get('/api/health')
def _health():
    return orjson.dumps({'status': 'UP'}), 200, {'Content-Type': 'application/json'}


app.run('0.0.0.0', 8080)
```