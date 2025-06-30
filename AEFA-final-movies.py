
import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])

# Add this debug print statement (excluding private_key)
#debug_key_dict = key_dict.copy()
#if "private_key" in debug_key_dict:
#    debug_key_dict["private_key"] = "---PRIVATE KEY REDACTED---"
#st.sidebar.write("Loaded key_dict (excluding private_key):", debug_key_dict)


creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="final-movies")

# It is recommended to handle authentication securely,
# for example, by using environment variables for service account paths.
# For this example, we'll use the provided path.
# Ensure that 'aefa-firebase2-firebase-adminsdk-fbsvc-e2fd0946c7.json' is accessible.

dbNames = db.collection("names")

st.header("Nuevo Registro:")

company = st.text_input("Company")
director = st.text_input("Director")
genre = st.text_input("Genre")
name = st.text_input("Name")

submit = st.button("Crear nuevo registro")

#ONCE THE NAME HAS SUBMITTED, UPLOAD IT TO THE BASE
if company and director and genre and name and submit:
  doc_ref = db.collection("names").document(name)
  doc_ref.set({
      "company": company,
      "director": director,
      "genre": genre, # Added a comma here
      "name": name
  })

  st.sidebar.write("Registro insertado correctamente!") # Added closing parenthesis


#############ESTO MUESTRA Y ACTUALIZA LOS REGISTROS EN EL SIDEBAR
  names_ref = list(db.collection(u'names').stream())
  names_dict = list(map(lambda x: x.to_dict(), names_ref))
  names_dataframe = pd.DataFrame(names_dict)
  st.dataframe(names_dataframe)
#############

###########BUSQUEDA POR NOMBRE###########################
def loadByName(name):
  names_ref = dbNames.where(u'name', u'==', name).limit(1) # Limit to one result since names should be unique
  currentName = None
  for myName in names_ref.stream():
    currentName = myName.to_dict()
  return currentName

st.sidebar.subheader("Buscar nombre")
nameSearch = st.sidebar.text_input("nombre")
btnFiltrar = st.sidebar.button("Buscar")

if btnFiltrar:
  doc = loadByName(nameSearch)
  if doc is None:
    st.sidebar.write("Nombre no existe")
  else:
    st.sidebar.write(doc)
#########################################################

###################eliminar#############################
st.sidebar.markdown("""___""")
btnEliminar = st.sidebar.button("Eliminar")

if btnEliminar:
  deletename = loadByName(nameSearch)
  if deletename is None:
   st.sidebar.write(f"{nameSearch} no existe")
  else:
    # To delete a document, you need the document reference, not just the dictionary
    doc_ref_to_delete = dbNames.document(deletename.get('name')) # Assuming 'name' is the document ID
    doc_ref_to_delete.delete()
    st.sidebar.write(f"{nameSearch} ha sido eliminado")
########################################################

#######################ACTULIZAR##########################
#
#st.sidebar.markdown("""___""")
#newname = st.sidebar.text_input("Actualizar nombre")
#btnActualizar = st.sidebar.button("Actualizar")

#if btnActualizar:
#  updatename = loadByName(nameSearch)
#  if updatename is None:
#    st.sidebar.write(f"{nameSearch} no existe")
#  else:
#    # To update a document, you need the document reference, not just the dictionary
#    doc_ref_to_update = dbNames.document(updatename.get('name')) # Assuming 'name' is the document ID
#    doc_ref_to_update.update(
#        {
#            "name": newname
#        }
#    )
#
############################################################
