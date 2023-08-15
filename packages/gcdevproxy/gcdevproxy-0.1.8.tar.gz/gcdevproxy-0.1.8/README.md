# GoodCam Device Proxy

[![Documentation Status](https://readthedocs.org/projects/gcdevproxy-py/badge/?version=latest)](https://gcdevproxy-py.readthedocs.io/en/latest/?badge=latest)

This library simplifies creating HTTP proxies that can be used to communicate
with GoodCam devices in various networks. GoodCam devices contain a
[built-in client](https://goodcam.github.io/goodcam-api/#tag/cloud) that
can be configured to connect automatically to a given proxy. Once
connected, the devices will wait for incoming HTTP requests. The proxy
simply forwards incoming HTTP requests to the connected devices.

## Installation

This library is just a wrapper over
[the Rust version](https://github.com/GoodCam/device-proxy-lib) of the same
library. You can install this library using pip:

```bash
pip install gcdevproxy
```

If there is no binary wheel available, pip will try to build also the
underlying Rust library. You will need the Rust compiler installed on your
system to do this. You can install it easily using:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

See https://www.rust-lang.org/tools/install for more information.

Even though the Rust version of this library can be built for any platform
supported by Rust, this Python wrapper is currently available only for Linux
systems.

The Rust version of this library also requires OpenSSL (version 1.0.1 or newer)
or LibreSSL (version 2.5 or newer). Ubuntu/Debian users can install OpenSSL
development files using:

```bash
sudo apt-get install libssl-dev
```

Fedora users can install them using:

```bash
sudo dnf install openssl-devel
```

## Usage example

The library supports both blocking and asynchronous API, though the
asynchronous API should be preferred due to a better performance. To use the
asynchronous API, simply use the `create_proxy` and `RequestHandler`
equivalents from the `gcdevproxy.aio` module.

Please keep in mind that **when using the blocking API, your request handler
MUST be thread-safe!** The proxy runtime may call your handler from multiple
threads at the same time. You don't have to worry about this when using the
asynchronous API because your handler will be called only from the thread
running the Python's asyncio event loop (usually the main thread).

### Asynchronous API

```python
from gcdevproxy.aio import RequestHandler

...

class MyRequestHandler(RequestHandler):
    async def handle_device_request(self, authorization: Authorization) -> 'DeviceHandlerResult':
        ...

    async def handle_client_request(self, request: Request) -> 'ClientHandlerResult':
        ...

async def main():
    config = ProxyConfig()
    config.http_bindings = [('0.0.0.0', 8080)]
    config.request_handler = MyRequestHandler()

    proxy = await gcdevproxy.aio.create_proxy(config)

    await proxy.run()

if __name__ == '__main__':
    asyncio.run(main())
```

### Blocking API

```python
from gcdevproxy import RequestHandler

...

class MyRequestHandler(RequestHandler):
    def handle_device_request(self, authorization: Authorization) -> 'DeviceHandlerResult':
        ...

    def handle_client_request(self, request: Request) -> 'ClientHandlerResult':
        ...

def main():
    config = ProxyConfig()
    config.http_bindings = [('0.0.0.0', 8080)]
    config.request_handler = MyRequestHandler()

    proxy = gcdevproxy.create_proxy(config)

    proxy.run()

if __name__ == '__main__':
    main()
```

### More examples

See the `examples` directory in the root of this repository for ready-to-use
examples.
