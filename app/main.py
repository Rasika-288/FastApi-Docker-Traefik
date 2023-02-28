import io

from fastapi import FastAPI
import pandas as pd
from app.db import database, User
from fastapi import FastAPI
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import gzip
app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root():
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()



app = FastAPI()

@app.post("/file")
async def create_file(request: Request) -> Response:
    data = await request.json()
    df = pd.DataFrame.from_dict(data)
    csv_str = df.to_csv(index=False)
    gzipped = io.BytesIO()
    with gzip.GzipFile(mode='w', fileobj=gzipped) as f:
        f.write(csv_str.encode('utf-8'))
    response = Response(content=gzipped.getvalue())
    response.headers['Content-Type'] = 'application/gzip'
    response.headers['Content-Disposition'] = 'attachment; filename="file.csv.gz"'
    return response