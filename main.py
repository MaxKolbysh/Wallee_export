from fastapi import FastAPI, Request, Response, status, HTTPException
from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from fastapi.responses import JSONResponse, StreamingResponse
from xhtml2pdf import pisa 
from io import BytesIO

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def root():
    return {"message": "Service is running..."}





class QuantityAttributes(BaseModel):
    name: str
    calculation: str

# class DataTableValues(BaseModel):
#     values: List[str]

# class DataTable(BaseModel):
#     data_table: List[DataTableValues]

# class Images(BaseModel):
#     logo_head: HttpUrl
#     logo_footer: HttpUrl

# class Wall(BaseModel):
#     category: str
#     gde: Optional[dict]  # You can adjust the type of 'gde' accordingly
#     system_image: HttpUrl
#     quantity_attributes: List[QuantityAttributes]
#     data_table: List[DataTableValues]

# class MyPydanticModel(BaseModel):
#     datetime: str
#     images: Images
#     walls: List[Wall]   

@app.post("/pdf")
async def generate_pdf_post(pdf_data: QuantityAttributes):
  # Create an HTML template
  template = """
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Quantity Attributes</title>
  </head>
  <body>
    <h1>Quantity Attributes</h1>
    <p>Quantity Name: {{ item.name }}</p>
    <p>Quantity Calculation: {{ item.calculation }}</p>
  </body>
  </html>
  """

  # Load the JSON data into a dictionary
  item = pdf_data.dict()

  # Render the HTML to bytes
  bytes_io = BytesIO()
  pisa.CreatePDF(template.render(item), bytes_io)
  response = StreamingResponse(bytes_io, media_type="application/pdf")
  response.headers["Content-Disposition"] = "inline; filename=quantity_attributes.pdf"
  return response