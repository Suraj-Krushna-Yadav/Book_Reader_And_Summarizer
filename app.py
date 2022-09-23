# from crypt import methods
from wsgiref.util import request_uri
from flask import Flask
from flask import render_template, request, redirect
import os

app = Flask(__name__)

# path to save PDF Files
app.config["PDF_PATH"] = "C:\\Users\\Pratiksha Wagh\\Desktop\\Book Reader and summarizer\\static\\pdf"

# file extension funcyion is not completed yet
app.config["FILE_EXTENSION"] = ["PDF", ]


@app.route('/')
@app.route('/upload', methods=["POST", "GET"])
def Home():
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


if __name__ == '__main__':
    app.run(debug=True)
