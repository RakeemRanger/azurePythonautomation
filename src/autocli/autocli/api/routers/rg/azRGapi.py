import json

from fastapi import FastAPI, APIRouter

from autocli.core.rg.az_rg_checker import ResourceGroupChecker
from autocli.core.network.vnets.az_vnet_create import ResourceGroupCreator
from autocli.core.lib.trackingId_util import TrackingIdGenerator

trackId = TrackingIdGenerator().trackingId()
router = APIRouter()


@router.get("/location/{location}/resourceGroup/{rg_name}")
def check_resource_group(rg_name: str, location: str):
    checker = ResourceGroupChecker(location=location, rg_name=rg_name, trackingId=trackId)
    response = checker.rg_check()
    response = json.loads(response)
    return response


@router.post("/location/{location}/resourceGroup/{rg_name}")
def create_resource_group(rg_name: str, location: str):
    creator = ResourceGroupCreator(location=location, rg_name=rg_name, trackingId=trackId)
    response = creator.rg_create()
    response = json.loads(response)
    return response


app = FastAPI()
app.include_router(router)
