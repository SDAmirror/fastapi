from uuid import uuid4

from fastapi import FastAPI, Request,Response, Form, HTTPException,Depends


from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from signalwire.relay import client

from pkg.session.sessionStorage import *
from pkg.DB import CRUD, schemas
from pkg.DB.DB import SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
app.mount('/static',StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#----------------------------------------------

@app.get('/check')
async def check(request: Request):
    return
@app.get("/sess")
async def sess(request: Request):
    return templates.TemplateResponse("sess.html",{"request":request})
@app.post("/create_session/")
async def create_session(request: Request,name: str = Form(...)):

    session = uuid4()
    data = SessionData(username=name,id= session)
    await backend.create(session, data)
    t = templates.TemplateResponse("ssss.html",{"request":request,"name":name,"session":data})
    cookie.attach_to_response(t, session)

    return t


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data

@app.post("/delete_session")
async def del_session(response: Response,request: Request, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"+str(request.cookies)

#----------------------------------------------


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post('/lofi/')
async def lofi(request: Request,user: str = Form(...),password: str = Form(...),):
    return templates.TemplateResponse("lofi.html",{'request':request,"username":user,'password':password})
@app.post('/register/')
async def register(request: Request,username: str = Form(...), password: str = Form(...),db: Session = Depends(get_db)):
    db_user = CRUD.get_user_by_username(db, username=username)
    user = schemas.UserCreate(password=password, username=username)

    print(user)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    u= CRUD.create_user(db=db, user=user)

    return templates.TemplateResponse("lofi.html",{'request':request,"username":u.username,'password':u.hashed_password,'user':u})
@app.post('/login/')
async def login(request: Request,username: str = Form(...),password: str = Form(...),db: Session = Depends(get_db)):
    pass

@app.get("/sign", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("sign.html", {"request": request})