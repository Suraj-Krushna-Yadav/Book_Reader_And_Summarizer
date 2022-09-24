from pathlib import Path
import pytesseract
from PIL import Image
import PyPDF2 as p2
from pdf2image import convert_from_path



def binary_extraction(pdf_path):
    pdf2 = p2.PdfFileReader(pdf_path)   # Using PyPDF2 for Text Extraction

    with Path('Files\\TEXT\\'+pdf_path[:-4]+'.txt').open('w') as op_file:
        text=''
        for page in pdf2.pages:
            text += page.extractText()
        op_file.write(text)




def pdf2img(pdf_path):
    # Store Pdf with convert_from_path function
    images = convert_from_path(pdf_path, poppler_path=r'C:\\poppler-0.68.0\bin')

    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('Files\\IMG\\'+pdf_path[:-4]+'-'+str(i)+'.jpg','JPEG')




def ocr_text_extraction(img_path):

    img = Image.open(img_path)
    pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    res = pytesseract.image_to_string(img)              # for english
    #res = pytesseract.image_to_string(img, lang="hin") # for hindi

    with Path('Files\\TEXT\\'+img_path[:-4]+'.txt').open('w', encoding = 'utf-8') as op_file:
            op_file.write(res)



def pdf2img2txt(pdf_path):

    full_text = ""

    images = convert_from_path(pdf_path, poppler_path=r'C:\\poppler-0.68.0\bin')
    pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    for i in range(len(images)):

        # Save pages as images in the pdf
        images[i].save('Files\\IMG\\'+pdf_path[9:-4]+'-'+str(i)+'.jpg','JPEG')

        img = Image.open('Files\\IMG\\'+pdf_path[9:-4]+'-'+str(i)+'.jpg')

        full_text += "\n"
        res = pytesseract.image_to_string(img)              # for english
        full_text += res

        #res = pytesseract.image_to_string(img, lang="hin") # for hindi

        with Path('Files\\TEXT\\'+pdf_path[9:-4]+'-'+str(i)+'.txt').open('w', encoding = 'utf-8') as op_file:
            op_file.write(res)

    with Path('Files\\TEXT\\'+pdf_path[9:-4]+'.txt').open('w', encoding = 'utf-8') as op_file:
        op_file.write(full_text)
    return full_text


# pdf2img2txt("BRS_PPT_1.pdf")
# pdf2img("Receipt.pdf")
# ocr_text_extraction("Receipt-0.jpg")
