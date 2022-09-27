# from crypt import methods
from wsgiref.util import request_uri
from flask import Flask
from flask import render_template, request, redirect
import Functions
import os

try : Functions.mkres() # For covinience to create empty directories initially
except: pass


app = Flask(__name__)

# path to save PDF Files
# Add the path of your pdf folder
app.config["PDF_PATH"] = "Resources\\PDF"

# file extension funcyion is not completed yet
app.config["FILE_EXTENSION"] = ["PDF", ]


@app.route('/')
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
                return redirect(request_uri)
           
            # saving  file to pdf location
            myFile.save(os.path.join(app.config["PDF_PATH"], myFile.filename))

            print("File uploaded sucessfully...")
            return redirect(request.url)

    return render_template('Index.html')


@app.route('/upload/Text', methods=['POST'])
def upload_text():
    entries = os.listdir("Resources\\PDF\\")
    pdf = "Resources\\PDF\\"+str(entries[0]) 
    res = Functions.pdf2img2txt(pdf)
    return render_template('text.html', result=res)


if __name__ == '__main__':
    app.run(debug=True)
