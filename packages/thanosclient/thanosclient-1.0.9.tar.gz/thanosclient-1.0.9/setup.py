from setuptools import setup, find_packages

from thanosclient import __version__

setup(name="thanosclient",
      version=__version__,
      description="cipher client",
      author="ams",
      packages=find_packages(),
      install_requires=['protobuf>=3.12', 'grpcio>=1.31', 'grpc-service-ams>=1.7.7'],
      long_description="""cipher gRPC client"""
)
