# openshift-pod-terminal-haproxy
Install OpenShift on CRC, proxy the k8s API server through HAProxy, and connect the FastAPI WebSocket to the pod

# Install
pip install fastapi pydantic "uvicorn[standard]" kubernetes==25.3.0 Jinja2

# Usage
```
pip install requirements.txt
python3 main.py

config.load_kube_config(config_file="/root/openshift-client/openshift-requests-client/kubeconfig")
```
I am using haproxy proxy 6443, API port. If the websocket automatically disconnects within 1 minute, I need to increase the following two parameters
```
timeout client 5m
timeout server 5m
```

reference resources:
https://github.com/yuanleyou/kubeshell-backend/tree/master

