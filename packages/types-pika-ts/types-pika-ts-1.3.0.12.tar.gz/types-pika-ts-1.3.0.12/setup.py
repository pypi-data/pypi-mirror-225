from setuptools import setup

name = "types-pika-ts"
description = "Typing stubs for pika"
long_description = '''
## Typing stubs for pika

This is a PEP 561 type stub package for the `pika` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pika`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pika. All fixes for
types and metadata should be contributed there.

The `types-pika` package contains alternate, more complete type stubs, that are maintained outside of typeshed.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `695d41f4870aede6e7027cf23bb65b07b59eedc6` and was tested
with mypy 1.4.1, pyright 1.1.323, and
pytype 2023.8.14.
'''.lstrip()

setup(name=name,
      version="1.3.0.12",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pika.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pika-stubs'],
      package_data={'pika-stubs': ['__init__.pyi', 'adapters/__init__.pyi', 'adapters/asyncio_connection.pyi', 'adapters/base_connection.pyi', 'adapters/blocking_connection.pyi', 'adapters/gevent_connection.pyi', 'adapters/select_connection.pyi', 'adapters/tornado_connection.pyi', 'adapters/twisted_connection.pyi', 'adapters/utils/__init__.pyi', 'adapters/utils/connection_workflow.pyi', 'adapters/utils/io_services_utils.pyi', 'adapters/utils/nbio_interface.pyi', 'adapters/utils/selector_ioloop_adapter.pyi', 'amqp_object.pyi', 'callback.pyi', 'channel.pyi', 'compat.pyi', 'connection.pyi', 'credentials.pyi', 'data.pyi', 'delivery_mode.pyi', 'diagnostic_utils.pyi', 'exceptions.pyi', 'exchange_type.pyi', 'frame.pyi', 'heartbeat.pyi', 'spec.pyi', 'tcp_socket_opts.pyi', 'validators.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
