
import streamlit as st
import pandas as pd
from google.cloud import firestore

db = firestore.Client.from_service_account_json("aefa-999-final-firebase-adminsdk-fbsvc-5e42f45ac9.json.json")
dbNames = db.collection("name")

names_ref = list(db.collection(u'name').stream())
names_dict =list(map(lambda x: x.to_dict(), names_ref))
names_dataframe = pd.DataFrame(names_dict)
st.dataframe(names_dataframe)

######BUSQUEDA#############################
def loadByName(name):
  names_ref = dbNames.where(u'name', u'==', name)
  currentName = None
  for myname in names_ref.stream():
    currentName = myname
    return currentName

st.sidebar.subheader("Buscar nombre")
nameSearch  = st.sidebar.text_input("nombre")
btnFiltrar = st.sidebar.button("Buscar")

if btnFiltrar:
  doc = loadByName(nameSearch)
  if doc is None:
    st.sidebar.write("Nombre no existe")
  else:
    st.sidebar.write(doc.to_dict())

###########ELIMNA##########################
st.sidebar.markdown("""---""")
btnEliminar = st.sidebar.button("Eliminar")

if btnEliminar:
  deletename = loadByName(nameSearch)
  if deletename is None:
    st.sidebar.write(f"{nameSearch} no existe")
  else:
    dbNames.document(deletename.id).delete()
    st.sidebar.write(f"{nameSearch} eliminado")


###########ACTUALIZAR##########################
#st.sidebar.markdown("""---""")
#newname = st.sidebar.text_input("Actualizar nombre")
#btnActualizar = st.sidebar.button("Actualizar")
#if btnActualizar:
# updatename = loadByName(nameSearch)
# if updatename is None:
#   st.write(f"{nameSearch} no existe")
# else:
#   myupdatename = dbNames.document(updatename.id)
#   myupdatename.update(
# {
#"name": newname
# }
# )

st.sidebar.subheader("Inserte la informacion que desea agregar")
# Input fields for data
company = st.sidebar.text_input("Company")
director = st.sidebar.text_input("Director")
genre = st.sidebar.text_input("Genre")
name = st.sidebar.text_input("Name")


if st.sidebar.button("Insert into Firebase"):
    if company and director and genre and name:
        # Reference to the Firestore collection
        doc_ref = db.collection("name").document()  # You can specify a document ID or let Firestore auto-generate one
        doc_ref.set({
            "company": company,
            "director": director,
            "genre": genre,
            "name": name
        })
        st.success("Informacion insertada correctamente!")
    else:
        st.error("Porfavor llene todos los campos!")
