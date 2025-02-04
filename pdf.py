import streamlit as st
import PyPDF2
from PyPDF2 import PdfFileMerger, PdfFileReader
import os
import emoji as emo
import io
output_pdf = "documents/pdf.pdf"

st.set_page_config(page_title="Editor de PDFs", page_icon="📄", layout="centered")
# Título de la app
st.title("📄 Editor de PDFs")
st.subheader("Elige una función para modificar tu PDF:")
# Menú de selección
opcion = st.selectbox("Selecciona una opción:", ["Unir PDFs", "Reordenar páginas", "Eliminar páginas", "Rotar páginas"])




def unir_pdfs(output_path, documents):
    pdf_final = PyPDF2.PdfMerger()
    for document in documents:
        pdf_final.append(io.BytesIO(document.getvalue()))  # Leer desde memoria en BytesIO
    with open(output_path, "wb") as output_file:
        pdf_final.write(output_file)
    
st.header("Unir archivos pdf",divider="rainbow" )
st.image("img/pdf_img.png")
st.subheader("Adjuntar archivos para unir")

pdf_adjuntos = st.file_uploader(label="",accept_multiple_files=True, type='pdf')

unir = st.button(label="Unir PDF's", icon="\U0001F60D")

if unir:
    if len(pdf_adjuntos) <=1:
        st.warning("Debes adjuntar mas de un archivo PDF")
    else:
        unir_pdfs(output_pdf, pdf_adjuntos)
        st.success("Desde aqui puede descargar el PDF unido", )
        with open(output_pdf, 'rb') as file:
            pdf_data = file.read()
        st.download_button(label=":sunglasses: Descragar el archivo PDF :sunglasses:", data=pdf_data, file_name="pdf_final.pdf") 
        
