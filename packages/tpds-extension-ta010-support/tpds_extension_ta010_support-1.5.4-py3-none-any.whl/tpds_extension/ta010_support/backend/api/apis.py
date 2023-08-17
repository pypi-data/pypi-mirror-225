from fastapi.routing import APIRouter
from .models import ConfiguratorMessageReponse, TFLXAUTHConfiguratorMessage, TFLXWPCConfiguratorMessage
from .tflxauth_ta010 import TA010TFLXAuthPackage, ta010_tflxauth_proto_prov_handle
from .tflxwpc_ta010 import TA010TFLXWPCPackage, ta010_tflxwpc_proto_prov_handle

router = APIRouter(prefix="/ta010", tags=["TA010_APIs"])


@router.post('/generate_tflxauth_xml', response_model=ConfiguratorMessageReponse)
def generate_tflxauth_xml(config_string: TFLXAUTHConfiguratorMessage):
    resp = TA010TFLXAuthPackage(config_string.json())
    return resp.get_response()


@router.post('/provision_tflxauth_device')
def provision_tflxauth_device(config_string: TFLXAUTHConfiguratorMessage) -> None:
    print("generate_tflxauth_xml")
    resp = ta010_tflxauth_proto_prov_handle(config_string.json())
    return resp


@router.post('/generate_tflxwpc_xml', response_model=ConfiguratorMessageReponse)
def generate_tflxwpc_xml(config_string: TFLXWPCConfiguratorMessage):
    resp = TA010TFLXWPCPackage(config_string.json())
    return resp.get_response()


@router.post('/provision_tflxwpc_device')
def provision_tflxwpc_device(config_string: TFLXWPCConfiguratorMessage) -> None:
    resp = ta010_tflxwpc_proto_prov_handle(config_string.json())
    return resp
