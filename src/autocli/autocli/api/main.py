from fastapi import FastAPI
from autocli.api.routers.network.vnet.azVnetapi  import router as vnetRouter
from autocli.api.routers.rg.azRGapi import router as rgRouter

app = FastAPI()

app.include_router(vnetRouter)
app.include_router(rgRouter)
