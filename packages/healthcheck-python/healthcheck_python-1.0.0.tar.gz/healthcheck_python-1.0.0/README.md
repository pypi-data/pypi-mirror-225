### A Health Check API Library for Multiprocessing Python Apps

![passing](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cagdasbas/07e196561fb7496e619da3ef402209a6/raw/passing.json)
![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cagdasbas/07e196561fb7496e619da3ef402209a6/raw/coverage.json)
![version](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cagdasbas/07e196561fb7496e619da3ef402209a6/raw/version.json)
[![license](https://img.shields.io/badge/license-Apache%202-blue)](LICENSE)

This library adds a health check REST API to your multiprocessing apps. You can add health check function calls to your 
functions and library will track the function calls. This library supports ```multiprocessing``` threads. You can fetch
a single overall app status by fetching
```http://<ip>:<port>/healthcheck```, a single overall app liveness by fetching
```http://<ip>:<port>/liveness```. 

Influenced by prometheus client mp exporter. Health check functions will write healthy and liveness results `<pid>.json` 
file located in directory defined by `PY_HEALTH_MULTIPROC_DIR`. If the directory doesn't exist, health checks won't work. 

**Please clear the directory content before running your app.** REST API 

Each health check class will be run every 10 seconds by default. You can change this value by setting `PY_HEALTH_RUN_PERIOD`.

#### Usage

You can register your functions with ```add_check()``` decorator.
You can set a timeout for your functions with ```set_timeout()``` if you process needs to check in regularly.

```python
import multiprocessing as mp
import time

import healthcheck_python as hp


class P1(mp.Process):
	def __init__(self):
		super().__init__()
		self._stop_bit = mp.Event()

	def close(self) -> None:
		self._stop_bit.set()

	def healthcheck(self):
		return True, "Healthcheck is OK"

	def do_something(self):
		time.sleep(5)

	def run(self):
		hp.add_check(self.healthcheck)
		hp.set_timeout(10)

		hp.live()
		while not self._stop_bit.is_set():
			hp.healthy()
			self.do_something()


hp.start_http_server()

p1 = P1()
p1.start()

time.sleep(30)

p1.close()
p1.join()
```

```shell
$ curl http://localhost:8080/healthcheck
{"hostname": "my_app", "status": "success", "timestamp": 1684406235.474363, "results": [[{"checker": "healthcheck", "output": "Healthcheck is OK", "passed": true, "timestamp": 1684406230.9507005, "response_time": 5e-06}, {"checker": "P1", "output": "", "passed": true, "timestamp": 1684406230.9507082, "response_time": 0}]]}
$ curl http://localhost:8080/liveness
{"hostname": "my_app", "liveness": true, "timestamp": 1684406208.784097}
```

Set `PY_HEALTH_TEST_MODE` to disable the functionality. Your functions will run without any intervention and no port will be listened