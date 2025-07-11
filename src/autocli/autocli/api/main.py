from fastapi import FastAPI
from autocli.api.azVnetapi import router as vnetRouter
from autocli.api.azRGapi import router as rgRouter

app = FastAPI()

app.include_router(vnetRouter)
app.include_router(rgRouter)