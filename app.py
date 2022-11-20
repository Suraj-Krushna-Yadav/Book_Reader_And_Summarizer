# from crypt import methods
from turtle import heading
from unittest import result
from wsgiref.util import request_uri
from flask import Flask
from flask import render_template, request, redirect
import Functions as fn
import os
import shutil

try : 
    fn.create_null_db()
    fn.validate_resources_directory() # For covinience to create empty directories initially
except Exception as e:
    print(e)
    pass


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
        global pdfname
        pdfname = entries[0]
        # if ".pdf" in pdfname:type="PDF"
        # elif ".img" in pdfname or "jpg" in pdfname or "jpeg" in pdfname or ".png" in pdfname: type = "IMG"
        # elif ".txt" in pdfname : type = "TEXT"
        # global counter
        # fn.increment_counter()
        # counter = fn.get_counter()
        # fn.add_id_type_name(counter,type,pdfname)
    except:
        pdf = '----'
    return render_template('upload.html',pdf_name=pdfname)


@app.route('/upload/Text', methods=['POST'])
def show_text():
    try :
        pdf_path = "Resources\\PDF\\"+str(pdfname)
        res = fn.pdf2img2txt(pdf_path)
        shutil.move(pdf_path,"Resources\\PROCESSED PDF")
        return render_template('text.html', result = res, pdf_name = pdfname)
    except Exception as e:
        print("Error during show text is\n",e)
        return render_template('text.html', heading = "PDF not uploaded")

if __name__ == '__main__':
    app.run(debug=True)
