import streamlit as st
from graph import app

st.set_page_config(page_title="Handwritten Study Notes", layout="centered")
st.title("Handwritten Study Notes — Multi-Agent System")

prompt = st.text_area("Enter the topic or prompt for the study notes:", height=120)
run = st.button("Generate Notes")

if run and prompt.strip():
    with st.spinner("Running agents..."):
        initial_state = {
            "messages": [{"content": prompt}],
            "summary_notes": "",
            "html_content": "",
            "image_path": "",
            "iterations": 0,
            "is_approved": False
        }

        outputs = []
        for out in app.stream(initial_state):
            outputs.append(out)

        # display last known state
        final_state = {}
        for o in outputs:
            for k, v in o.items():
                final_state.update(v)

        st.subheader("Generated Notes")
        st.markdown(final_state.get("summary_notes", "_No notes generated._"))

        if final_state.get("image_path"):
            st.image(final_state.get("image_path"), caption="Handwritten Notes Preview")
        else:
            st.info("Screenshot not generated — Playwright may be missing.")

        st.success("Done")
