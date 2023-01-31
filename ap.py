from fastapi import  FastAPI , Response , status, HTTPException,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pymysql

app = FastAPI()
templates = Jinja2Templates(directory="html")


try:
    connection = pymysql.connect(host='localhost',user='root',password='vanshr123@&',db='sra',autocommit=True)
    cursor = connection.cursor()
    print("databasse connected")
except Exception as e:
    print("database failed to connect")
    print("error : ",e)
app.mount("/static", StaticFiles(directory="html"), name="static")

DB_table_name = 'eventdata1'
DB_table_name1 = 'signincheck'
table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    ( name VARCHAR(50)  ,
                     email VARCHAR(50) ,
                     facultyid VARCHAR(50) ,
                     date VARCHAR(50) ,
                     Auditorium VARCHAR(50) ,
                     timings VARCHAR(50) ,
                     PRIMARY KEY (date,timings,Auditorium));
                    """
table_sql1 = "CREATE TABLE IF NOT EXISTS " + DB_table_name1 + """
                    ( username VARCHAR(50)  ,
                     password VARCHAR(15) ,
                     PRIMARY KEY (username));
                    """
cursor.execute(table_sql)
cursor.execute(table_sql1)

@app.get("/")
def home(request:Request):
    return templates.TemplateResponse("event.html",{"request": request})


@app.post("/submit")
def login_check(request:Request,username:str=Form(...),password:str=Form(...)):
    try:
        cursor.execute(""" SELECT * FROM signincheck WHERE username=%s and password=%s""",(username,password))
        a=cursor.fetchone()
    except:
        return {"user not found"}
    if(a==None):
        return templates.TemplateResponse("event1.html",{"request": request})
    else:
        return templates.TemplateResponse("index.html",{"request": request})


@app.get("/home")
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.get("/register")
def home(request:Request):
    return templates.TemplateResponse("reg.html",{"request": request})

@app.get("/signout")
def home(request:Request):
    return templates.TemplateResponse("event.html",{"request": request})

@app.post("/submitevent")
def login_check(request:Request,name:str=Form(...),email:str=Form(...),facultyid:str=Form(...),date:str=Form(...),Auditorium:str=Form(...),timings:str=Form(...)):
    try:
        cursor.execute(""" INSERT INTO `abc`.`eventdata1`
(`name`,
`email`,
`facultyid`,
`date`,
`Auditorium`,
`timings`)
VALUES
(%s,%s,%s,%s,%s,%s);""",(name,email,facultyid,date,Auditorium,timings))
        id=name+" you have successfully registered the "+Auditorium +" for date "+date+" at "+timings
        return templates.TemplateResponse("reg.html",{"request": request,"id": id})
    except Exception as e:
        print(e)
        id="Auditorium is currently occupied for your specified timings"
        return templates.TemplateResponse("reg.html",{"request": request,"id": id})


