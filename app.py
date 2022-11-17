# from crypt import methods
from turtle import heading
from unittest import result
from wsgiref.util import request_uri
from flask import Flask
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import Functions
import os
import sqlite3
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS uploaded(
            file_id integer primary key,
            file_name text,
            file_path text,
            full_txt_path text,
            audio_path text,
            summary_path text
            )""")
c.execute("""CREATE TABLE IF NOT EXISTS pdf2img(
            pi_id integer primary key,
            file_id integer,
            file_name text,
            img_no integer,
            img_path text,
            img_txt_path text,
            audio_path text
            )""")


def upload_insert_file(file):
    query="INSERT INTO uploaded(file_name,file_path) VALUES(?,?);"
    c.execute(query,(str(file),str("Resources\\PDF\\"+str(file),)))


conn.commit()

try : Functions.validate_resources_directory() # For covinience to create empty directories initially
except: pass


app = Flask(__name__)

# path to save PDF Files
# Add the path of your pdf folder
app.config["PDF_PATH"] = "Resources\\PDF"

# file extension funcyion is not completed yet
app.config["FILE_EXTENSION"] = ["PDF", ]



@app.route('/')
def start():
    return render_template('Index.html')
@app.route('/upload', methods=["POST", "GET"])
def Home():
    # try:
    #     entries = os.listdir("Files\\PDF\\")
    #     os.remove("Files\\PDF\\"+str(entries[0]))
    # except:
    #     pass
    if request.method == "POST":
        if request.files:

            myFile = request.files["myfile"]

            if myFile.filename == "":
                print("Must have filename")
                return render_template('text.html', heading = "PDF not selected")
           
           
            # saving  file to pdf location
            myFile.save(os.path.join(app.config["PDF_PATH"], myFile.filename))
            
            print("File uploaded sucessfully...")
            return redirect(request.url)

    try:
        entries = os.listdir("Resources\\PDF\\")
        pdf = entries[0]
    except:
        pdf = '----'
    return render_template('upload.html',pdf_name=pdf)


@app.route('/upload/Text', methods=['POST'])
def show_text():
    try :
        entries = os.listdir("Resources\\PDF\\")
        pdfname=entries[0]
        pdf = "Resources\\PDF\\"+str(entries[0]) 
        res = Functions.pdf2img2txt(pdf)
        os.remove(pdf)
        return render_template('text.html', result = res, pdf_name = pdfname)
    except:
        return render_template('text.html', heading = "PDF not uploaded")

if __name__ == '__main__':
    app.run(debug=True)