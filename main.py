from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from pydantic import BaseModel
import io
from jinja2 import Environment, FileSystemLoader, select_autoescape
import csv
from lxml import etree



app = FastAPI()

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def root():
    return {"message": "Service is running..."}





class QuantityAttributes(BaseModel):
    name: str
    calculation: str
    content: str

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
async def generate_pdf(attributes: QuantityAttributes):
    #
    # We will add jinja
    template = env.get_template('report_template.html')
    html_content = template.render(
        name=attributes.name,
        calculation=attributes.calculation,
        content=attributes.content
    )

    # pdf gen
    pdf = HTML(string=html_content).write_pdf()

    # run stream
    return StreamingResponse(io.BytesIO(pdf), media_type="application/pdf")


@app.post("/csv")
async def generate_csv(attributes: QuantityAttributes):
    # Create a CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Columns
    writer.writerow(['name', 'calculation', 'content'])

    # SOme data
    writer.writerow([attributes.name, attributes.calculation, attributes.content])

    # beginning
    output.seek(0)

    # Stream
    return StreamingResponse(io.StringIO(output.getvalue()), media_type="text/csv")


@app.post("/xml")
async def generate_xml(attributes: QuantityAttributes):
    # Create an XML root element
    root = etree.Element("Attributes")
    etree.SubElement(root, "Name").text = attributes.name
    etree.SubElement(root, "Calculation").text = attributes.calculation

    content_element = etree.SubElement(root, "Content")
    content_element.text = etree.CDATA(attributes.content)

    # Convert the XML element to a string
    def xml_stream():
        yield etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    # Stream
    return StreamingResponse(xml_stream(), media_type="application/xml")