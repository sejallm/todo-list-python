import streamlit as st
import json
import os
from datetime import date

st.set_page_config(page_title="To-Do App", page_icon="📝", layout="centered")

FILE = "tasks.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

data = load_data()
today = str(date.today())

if today not in data:
    data[today] = []

st.markdown("<h1 style='text-align: center;'>📝 My To-Do List</h1>", unsafe_allow_html=True)

task = st.text_input("✨ Add a new task")

if st.button("➕ Add Task"):
    if task:
        data[today].append({"task": task, "done": False})
        save_data(data)
        st.rerun()

st.divider()
st.subheader("📅 Today's Tasks")

for i, item in enumerate(data[today]):
    col1, col2, col3 = st.columns([6,1,1])

    item["done"] = col1.checkbox(item["task"], value=item["done"], key=f"done_{i}")

    if col2.button("✏️", key=f"edit_{i}"):
        new_task = st.text_input("Edit task", value=item["task"], key=f"edit_input_{i}")
        if st.button("Save", key=f"save_{i}"):
            data[today][i]["task"] = new_task
            save_data(data)
            st.rerun()

    if col3.button("❌", key=f"del_{i}"):
        data[today].pop(i)
        save_data(data)
        st.rerun()

save_data(data)

st.sidebar.title("📂 Previous Days")

for day in data:
    if day != today:
        st.sidebar.subheader(day)
        for item in data[day]:
            status = "✅" if item["done"] else "⬜"
            st.sidebar.write(f"{status} {item['task']}")