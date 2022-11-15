from pathlib import Path
import pytesseract
from PIL import Image
import PyPDF2 as p2
from pdf2image import convert_from_path
import os
import sqlite3

def cn():
    conn = sqlite3.connect('DATABASE.sqlite3')
    return conn

def create_null_db(): 
    conn = cn()
    conn.execute('''create table if not exists book(
        id integer primary key,
        file_type text,
        file_name text,
        total_pgs integer,
        page_no integer,
        img_path text,
        text_path text,
        audio_path text,
        summary_path text,
        summary_audio_path text
        );
                    ''')
    conn.execute('''CREATE TABLE IF NOT EXISTS other(
        id integer primary key,
        counter integer,
        password text
        );
                    ''')
    conn.commit()
    initialize_counter()

def initialize_counter():
    conn = cn()
    query = "INSERT INTO other(id,counter) VALUES(1,1);"
    conn.execute(query)
    conn.commit()

def get_counter():
    conn =cn()
    query = "select counter from other;"
    for i in conn.execute(query): return i[0]

def set_counter(val):
    conn=cn()
    query = "update other set counter = ? where id==1;"
    conn.execute(query,(val,))
    conn.commit()

def increment_counter():
    set_counter(get_counter()+1)

def fill_row(id,type,name,pg,no,img,txt):
    conn = cn()
    query = "insert into book(id,file_type,file_name,total_pgs,page_no,img_path,text_path) values(?,?,?,?,?,?,?);"
    conn.execute(query,(id,type,name,pg,no,img,txt,))
    conn.commit()

def add_id_type_name(id,type,name):
    conn = cn()
    query = "insert into book(id,file_type,file_name) values(?,?,?);"
    conn.execute(query,(id,type,name,))
    conn.commit()

def add_total_pgs_pgno(total_no_pg,page_no,id):
    conn = cn()
    query = "update book set total_pgs = ?, page_no = ? where id == ?;"
    conn.execute(query,(total_no_pg,page_no,id,))
    conn.commit()

def add_img_path(img_path,id):
    conn = cn()
    query = "update book set img_path = ? where id == ?;"
    conn.execute(query,(img_path,id,))
    conn.commit()

def add_text_path(text_path,id):
    conn = cn()
    query = "update book set text_path = ? where id == ?;"
    conn.execute(query,(text_path,id,))
    conn.commit()


def binary_extraction(pdf_path):
    pdf2 = p2.PdfFileReader(pdf_path)   # Using PyPDF2 for Text Extraction
    pdf_name = pdf_path[13:-4]
    with Path('Resources\\TEXT\\'+pdf_name+'.txt').open('w') as op_file:
        text=''
        for page in pdf2.pages:
            text += page.extractText()
        op_file.write(text)




def pdf2img(pdf_path):
    # Store Pdf with convert_from_path function
    images = convert_from_path(pdf_path, poppler_path=r'C:\\poppler-0.68.0\bin')
    pdf_name = pdf_path[13:-4]
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('Resources\\IMG\\'+pdf_name+'-'+str(i)+'.jpg','JPEG')




def ocr_text_extraction(img_path):
    img_name = img_path[13:-4]
    img = Image.open(img_path)
    pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    res = pytesseract.image_to_string(img)              # for english
    #res = pytesseract.image_to_string(img, lang="hin") # for hindi

    with Path('Resources\\TEXT\\'+img_name+'.txt').open('w', encoding = 'utf-8') as op_file:
            op_file.write(res)



def pdf2img2txt(pdf_path):
    counter = get_counter()
    pdf_name = pdf_path[14:-4]
    full_text = ""

    images = convert_from_path(pdf_path, poppler_path=r'C:\\poppler-0.68.0\bin')
    pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    no_img = len(images)


    for i in range(no_img):
        counter = get_counter()

        # Save pages as images in the pdf
        img_path = 'Resources\\IMG\\'+pdf_name+'-'+str(i)+'.jpg'
        images[i].save(img_path,'JPEG')

        img = Image.open(img_path)

        full_text += "\n"
        res = pytesseract.image_to_string(img)              # for english
        #res = pytesseract.image_to_string(img, lang="hin") # for hindi
        full_text += res

        text_path = 'Resources\\TEXT\\'+pdf_name+'-'+str(i)+'.txt'
        with Path(text_path).open('w', encoding = 'utf-8') as op_file:
            op_file.write(res)
        try:
          fill_row(counter,"PDF",pdf_name,no_img,i+1,img_path,text_path)
        except Exception as e:
            print("\n\n1st Erroer due to : ",e)
        try:
            increment_counter()
        except Exception as e:
            print("\n\n2nd Erroer due to : ",e)

    full_text_path = 'Resources\\TEXT\\'+pdf_name+'.txt'
    with Path(full_text_path).open('w', encoding = 'utf-8') as op_file:
        op_file.write(full_text)
    return full_text




def validate_resources_directory():
    try :
        os.mkdir("Resources")
        validate_sub_resources_directory()
    except :
        validate_sub_resources_directory()

def validate_sub_resources_directory(): 
    entries = os.listdir("Resources\\")
    for sub_resource in "IMG",'PDF','TEXT','SUMMARY','AUDIO', "PROCESSED PDF":
        if sub_resource not in entries:
            os.mkdir("Resources\\"+str(sub_resource))
