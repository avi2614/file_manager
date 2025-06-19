import streamlit as st
import os
import psutil

st.set_page_config(page_title="File Manager", layout="centered")
st.title("📁 Streamlit File Manager")

path = st.text_input("Enter Directory Path", value="workspace")
os.makedirs(path, exist_ok=True)

def files(): return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
def dirs(): return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def get_dir_size(p):
    total = 0
    for dirpath, _, filenames in os.walk(p):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total

opt = st.selectbox("Choose Option", (
    "1️⃣ List Files", "2️⃣ Delete File", "3️⃣ Rename File",
    "4️⃣ Create Directory", "5️⃣ Exit", "📤 Upload File", "📥 Download File",
    "📊 Path Size & RAM Usage"
))

if opt == "1️⃣ List Files":
    d_list = dirs()
    f_list = files()
    if d_list:
        st.subheader("📂 Folders:")
        for d in d_list:
            st.markdown(f"- {d}/")
    if f_list:
        st.subheader("📄 Files:")
        for f in f_list:
            st.markdown(f"- {f}")
    if not d_list and not f_list:
        st.info("No files or folders in this path.")

elif opt == "2️⃣ Delete File":
    f = files()
    if f:
        fdel = st.selectbox("Select File", f)
        if st.button("Delete"): os.remove(os.path.join(path, fdel)); st.success(f"Deleted {fdel}")
    else:
        st.warning("No files to delete.")

elif opt == "3️⃣ Rename File":
    f = files()
    if f:
        old = st.selectbox("Old Name", f)
        new = st.text_input("New Name")
        if st.button("Rename") and new:
            os.rename(os.path.join(path, old), os.path.join(path, new))
            st.success(f"Renamed to {new}")
    else:
        st.warning("No files to rename.")

elif opt == "4️⃣ Create Directory":
    ndir = st.text_input("Directory Name")
    if st.button("Create") and ndir:
        p = os.path.join(path, ndir)
        if not os.path.exists(p): os.makedirs(p); st.success("Created")
        else: st.warning("Already exists.")
    elif st.button("Create"):
        st.error("Enter a valid name.")

elif opt == "5️⃣ Exit":
    st.warning("Session ended. You may close or select another option.")

elif opt == "📤 Upload File":
    up = st.file_uploader("Upload")
    if up:
        with open(os.path.join(path, up.name), "wb") as f:
            f.write(up.read())
        st.success(f"Uploaded {up.name}")

elif opt == "📥 Download File":
    f = files()
    if f:
        fdl = st.selectbox("Download File", f)
        with open(os.path.join(path, fdl), "rb") as file:
            st.download_button("Download", file, file_name=fdl)
    else:
        st.warning("No files available to download.")

elif opt == "📊 Path Size & RAM Usage":
    size = get_dir_size(path)
    ram = psutil.virtual_memory()
    st.subheader("📊 Stats")
    st.write(f"📁 Total Size of `{path}`: **{round(size / (1024**2), 2)} MB**")
    st.write(f"🧠 RAM Used: **{round(ram.used / (1024**3), 2)} GB** / {round(ram.total / (1024**3), 2)} GB")
    st.progress(ram.percent / 100)
