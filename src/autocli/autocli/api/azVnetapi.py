import json

from fastapi import FastAPI, APIRouter

from autocli.core.az_vnet_checker import VnetChecker
from autocli.core.az_vnet_create import VirtualNetworkCreator
from autocli.core.lib.trackingId_util import TrackingIdGenerator

trackId = TrackingIdGenerator().trackingId()
router = APIRouter()


@router.get("/resourceGroup/{rg_name}/location/{location}/virtual-network/{vnet_name}")
def check_resource_group(rg_name: str, location: str, vnet_name: str):
    checker = VnetChecker(location=location, rg_name=rg_name, vnet_name=vnet_name, trackingId=trackId)
    response = checker.vnet_check()
    response = json.loads(response)
    return response


@router.post("/resourceGroup/{rg_name}/location/{location}/virtual-network/{vnet_name}")
def create_resource_group(rg_name: str, location: str, vnet_name: str):
    creator = VirtualNetworkCreator(rg_name=rg_name, location=location, trackingId=trackId, vnet_name=vnet_name)
    response = creator.vnet_create()
    response = json.loads(response)
    return response


app = FastAPI()
app.include_router(router)
