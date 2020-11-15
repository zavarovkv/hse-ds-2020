# Run on web-server: uvicorn main:app --reload

import os
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def root(request: Request, message='Hello, Coursera students'):
    # return {'message': 'Hello World'}
    return templates.TemplateResponse('index.html',
                                      {'request': request, 'message': message})


@app.get('/lib')
async def get_lib(request: Request):
    books = os.listdir('static/lib')
    # return {'Books': books}
    return templates.TemplateResponse('lib.html',
                                      {'request': request, 'books': books})


@app.post('upload_book')
async def upload(request: Request,
                 name: str = Form(...),
                 book_file: UploadFile = File(...)):
    file_name = '_'.join(name.split()) + '.txt'
    save_path = f'static/lib/{file_name}'

    with open(save_path, 'wb') as f:
        for line in book_file.file:
            f.write(line)

    return {'result': 'success'}
