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
    st.header("Unir archivos pdf",divider="rainbow" )
    st.image("img/pdf_img.png")
    st.subheader("Adjuntar archivos para unir")
    pdf_final = PyPDF2.PdfMerger()
    for document in documents:
        pdf_final.append(io.BytesIO(document.getvalue()))  # Leer desde memoria en BytesIO
    with open(output_path, "wb") as output_file:
        pdf_final.write(output_file)  


# Función para reordenar páginas
def reordenar_pdf(archivo, nuevo_orden):
    pdf_reader = PyPDF2.PdfReader(archivo)
    pdf_writer = PyPDF2.PdfWriter()
    
    for i in nuevo_orden:
        pdf_writer.add_page(pdf_reader.pages[i])
    
    output_path = "pdf_reordenado.pdf"
    with open(output_path, "wb") as output_file:
        pdf_writer.write(output_file)
    
    return output_path

# Función para eliminar páginas
def eliminar_paginas(archivo, paginas_a_eliminar):
    pdf_reader = PyPDF2.PdfReader(archivo)
    pdf_writer = PyPDF2.PdfWriter()
    
    for i in range(len(pdf_reader.pages)):
        if i not in paginas_a_eliminar:
            pdf_writer.add_page(pdf_reader.pages[i])
    
    output_path = "pdf_editado.pdf"
    with open(output_path, "wb") as output_file:
        pdf_writer.write(output_file)
    
    return output_path

# Función para rotar páginas
def rotar_paginas(archivo, paginas_a_rotar, angulo):
    pdf_reader = PyPDF2.PdfReader(archivo)
    pdf_writer = PyPDF2.PdfWriter()
    
    for i in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[i]
        if i in paginas_a_rotar:
            page.rotate(angulo)
        pdf_writer.add_page(page)
    
    output_path = "pdf_rotado.pdf"
    with open(output_path, "wb") as output_file:
        pdf_writer.write(output_file)
    return output_path

# Sección según la opción elegida
if opcion == "Unir PDFs":
#    st.subheader("🔗 Unir PDFs")
#    archivos = st.file_uploader("Selecciona varios archivos PDF", accept_multiple_files=True, type="pdf")
#    if st.button("Unir PDFs"):
#        if archivos and len(archivos) > 1:
#            pdf_path = unir_pdfs(archivos)
 #           with open(pdf_path, "rb") as file:
 #               st.download_button("📥 Descargar PDF Unido", data=file, file_name="pdf_unido.pdf")
 #       else:
 #           st.warning("Debes subir al menos 2 archivos.")
    pdf_adjuntos = st.file_uploader(label="",accept_multiple_files=True, type='pdf')
    unir = st.button(label="Unir PDF's", icon="\U0001F60D")
    if unir: 
        if len(pdf_adjuntos) <=1:
            st.warning("Debes adjuntar mas de un archivo PDF")
        else:
            unir_pdfs(output_pdf, pdf_adjuntos)
            st.success("Desde aqui puede descargar el PDF unido")
            with open(output_pdf, 'rb') as file:
                pdf_data = file.read()
                st.download_button(label=":sunglasses: Descragar el archivo PDF :sunglasses:", data=pdf_data, file_name="pdf_final.pdf") 

elif opcion == "Reordenar páginas":
    st.subheader("🔄 Reordenar Páginas")
    archivo = st.file_uploader("Sube un archivo PDF", type="pdf")
    nuevo_orden = st.text_input("Introduce el nuevo orden de páginas (Ejemplo: 2,0,1 para cambiar el orden)")
    if st.button("Reordenar"):
        if archivo and nuevo_orden:
            orden = list(map(int, nuevo_orden.split(",")))
            pdf_path = reordenar_pdf(archivo, orden)
            with open(pdf_path, "rb") as file:
                st.download_button("📥 Descargar PDF Reordenado", data=file, file_name="pdf_reordenado.pdf")

elif opcion == "Eliminar páginas":
    st.subheader("❌ Eliminar Páginas")
    archivo = st.file_uploader("Sube un archivo PDF", type="pdf")
    paginas = st.text_input("Introduce los números de páginas a eliminar (Ejemplo: 0,2 para eliminar pág 1 y 3)")
    if st.button("Eliminar"):
        if archivo and paginas:
            paginas_a_eliminar = list(map(int, paginas.split(",")))
            pdf_path = eliminar_paginas(archivo, paginas_a_eliminar)
            with open(pdf_path, "rb") as file:
                st.download_button("📥 Descargar PDF Editado", data=file, file_name="pdf_editado.pdf")

elif opcion == "Rotar páginas":
    st.subheader("🔄 Rotar Páginas")
    archivo = st.file_uploader("Sube un archivo PDF", type="pdf")
    paginas = st.text_input("Introduce los números de páginas a rotar (Ejemplo: 0,1 para rotar pág 1 y 2)")
    angulo = st.selectbox("Selecciona el ángulo de rotación", [90, 180, 270])
    if st.button("Rotar"):
        if archivo and paginas:
            paginas_a_rotar = list(map(int, paginas.split(",")))
            pdf_path = rotar_paginas(archivo, paginas_a_rotar, angulo)
            with open(pdf_path, "rb") as file:
                st.download_button("📥 Descargar PDF Rotado", data=file, file_name="pdf_rotado.pdf")
        
