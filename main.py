from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/pdf")
async def root():
    return {"message": "PDF should be here"}

