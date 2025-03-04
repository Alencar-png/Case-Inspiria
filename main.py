
from fastapi.middleware.cors import CORSMiddleware
from routers.users import user
from routers.security import security
from routers.patients import patient
from routers.doctors import doctor
from routers.schedulings import scheduling
from routers.availability import availability
from fastapi import FastAPI
import uvicorn

app = FastAPI(title='Case-Inspiria - LolaBot', version='0.1.0')
# app.include_router(security, prefix='/api', tags=['security'])
# app.include_router(user, prefix='/api', tags=['users'])
app.include_router(patient, prefix='/api', tags=['patients'])
app.include_router(doctor, prefix='/api', tags=['doctors'])
app.include_router(scheduling, prefix='/api', tags=['schedulings'])
app.include_router(availability, prefix='/api', tags=['availability'])


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'], 
    allow_headers=['*']
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4200)
