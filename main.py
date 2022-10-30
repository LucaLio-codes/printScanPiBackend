from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules import fileSystem, printer

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(fileSystem.router)
app.include_router(printer.router)

@app.get("/")
def print_hi():
    return {"message": "we are live!"}


# Press the green button in the gutter to run the script.



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
