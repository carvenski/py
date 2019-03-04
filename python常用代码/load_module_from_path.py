

# import docker from sys path, not current dir, because there is a docker.py in  current dir ! conflict.
import sys
import imp
try:
    fn_, path_, desc_ = imp.find_module('docker', sys.path[1:])
    dockerSDK = imp.load_module('dockerSDK', fn_, path_, desc_)
except ImportError:
    raise Exception("=> please run [pip install docker==3.4.0] first ! <=")


