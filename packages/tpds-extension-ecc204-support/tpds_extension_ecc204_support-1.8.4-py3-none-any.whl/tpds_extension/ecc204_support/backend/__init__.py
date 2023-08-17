import os
from tpds.devices import TpdsDevices
from tpds.xml_handler import XMLProcessingRegistry
from .api.apis import router
from .api.ecc204_xml_updates import ECC204_TA010_TFLXAUTH_XMLUpdates, ECC204_TA010_TFLXWPC_XMLUpdates

TpdsDevices().add_device_info(os.path.dirname(__file__))
XMLProcessingRegistry().add_handler('ECC204_TFLXAUTH', ECC204_TA010_TFLXAUTH_XMLUpdates('ECC204_TFLXAUTH'))
XMLProcessingRegistry().add_handler('ECC204_TFLXWPC', ECC204_TA010_TFLXWPC_XMLUpdates('ECC204_TFLXWPC'))
