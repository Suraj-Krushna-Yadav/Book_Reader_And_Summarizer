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
                return render_template('Index.html',msg = "Please Choose File !")
            
            elif myFile.filename[-4:] != ".pdf":
                return render_template('Index.html', msg = "It is not a PDF file, Choose only PDF file!")
           
            # saving  file to pdf location
            try:
                entries = os.listdir("Resources\\PDF\\")
                for pdf in entries:
                    os.remove("Resources\\PDF\\"+str(pdf))
            except:
                pass
            myFile.save(os.path.join(app.config["PDF_PATH"], myFile.filename))
            global pdfname
            pdfname = myFile.filename
            global pdf_path
            pdf_path = "Resources\\PDF\\"+str(pdfname)

            print("File uploaded sucessfully...")
            return redirect(request.url)

    return render_template('upload.html',pdf_name=pdfname)


@app.route('/upload/Text', methods=['POST'])
def show_text():
    try :
        res = fn.pdf2img2txt2aud(pdf_path)
        try:
            shutil.move(pdf_path,"Resources\\PROCESSED PDF")
        except:
            pass
        return render_template('text.html', result = res, pdf_name = pdfname)

    except Exception as e:
        return render_template('fileerror.html', msg = e)


@app.route('/upload/Text/audio', methods=['POST'])
def play_audio():
    return render_template('textaudio.html', pdf_name = pdfname)


if __name__ == '__main__':
    app.run(debug=True)
