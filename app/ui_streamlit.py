import os, io, tempfile, pandas as pd, streamlit as st
from dotenv import load_dotenv
from graph.langgraph_pipeline import build_graph
from tts_asr.asr_whisper import transcribe
from tts_asr.tts_client import synthesize

load_dotenv()
st.set_page_config(page_title="🎙️ Agentic Voice Product Finder", layout="centered")
st.title("🎙️ Agentic Voice-to-Voice Product Discovery")

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

st.caption("Hold to record a short request, then click **Transcribe & Search**.")
audio_bytes = st.audio_input("Record your voice")

manual = st.text_input("Or type your request (fallback)", value="Recommend an eco-friendly stainless steel cleaner under $15.")
use_manual = st.toggle("Use typed request instead of ASR", value=True)

if st.button("Transcribe & Search"):
    if not use_manual and not audio_bytes:
        st.error("Please record audio or enable typed request."); st.stop()

    transcript = manual
    if not use_manual:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes.getvalue())
            audio_path = tmp.name
        transcript = transcribe(audio_path, os.getenv("ASR_MODEL","small"))
        st.success("ASR complete.")
        st.write("**Transcript:**", transcript)
    else:
        st.write("**Transcript:**", transcript)

    state = {
        "audio_path": None, "transcript": transcript,
        "intent": None, "plan": None, "evidence": None,
        "answer": None, "citations": None, "safety_flags": None,
        "tts_path": None, "log": []
    }
    final = st.session_state.graph.invoke(state)

    st.subheader("Agent Steps")
    for step in final["log"]:
        st.json(step, expanded=False)

    st.subheader("Answer")
    st.write(final["answer"])

    rag = (final.get("evidence") or {}).get("rag", [])
    if rag:
        df = pd.DataFrame(rag)[["title","brand","price","rating","ingredients"]].head(5)
        st.dataframe(df, use_container_width=True)

    st.subheader("Citations")
    st.write(final.get("citations", []))

    if st.button("🔊 Play TTS"):
        out_path = synthesize(final["answer"])
        audio = open(out_path, "rb").read()
        st.audio(io.BytesIO(audio), format="audio/wav")
