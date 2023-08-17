import os
from tpds.devices import TpdsDevices
from .api.apis import router

TpdsDevices().add_device_info(os.path.dirname(__file__))
