import streamlit as st
import pandas as pd
import os 
from io import BytesIO

st.set_page_config(page_title= "Data Sweeper",layout='centered')

#custom css
st.markdown(
    """
    <style>
    .stApp{
    background-color : white;
    color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#title and subtitle
st.title("🧹 Datasweeper By Khizar Raza")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning & visualization")
  
  #file uploader
uploaded_files =st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_files: 
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df =pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unspported file type: {file_ext}")
            continue

        #files Details
        st.write("🔍 Preview the head of thr Datafame")
        st.dataframe(df.head())
        
        # Data cleaning options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

                    with col2:
                        if st.button(f"fill missing values ofr {file.name}"):
                            numeric_cols = df.select_dtypes(include=["number"]).columns
                            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                            st.write("✅ Missing values filled!")

                st.subheader("🎯 Select Columns to keep")
                columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
                df = df[columns]


                #Data Visualization
                st.subheader("📊 Data Visualization")            
                if st.checkbox(f"Show visualization for {file.name}"):
                    st.bar_chart(df.select_dtypes(includes="number").ilot[:, :2])

                #Conversion Options

                st.subheader("♻️ Conversion Options")
                conversion_type =st.radio(f"Convert {file.name} to:",  {"CSV", "Excel"}, key=file.name)
                if st.button(f"Convert{file.name}"):
                    buffer = BytesIO()
                    if conversion_type == "CSV":
                        df.to.csv(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".csv")
                        mime_type = "text/csv"

                    elif conversion_type == "Excel":
                           df.to_excel(buffer, index=False)    
                        file_name = file.name.replace(file_ext, ".xlsx")
                        mime_type = "application/vnd.opemxmlformats-officedocument.spreadsheetml.sheet"
                        buffer.seek(0)

                    st.download_button(
                        label=f"Download {file.name} as {conversion_type}",
                        data=buffer,
                        file_name=file_name,
                        mime=mime_type
                    )
                    st.success("🎉 processed successfully!")
