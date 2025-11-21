import os, httpx

def synthesize(text, out_path="out.wav"):
    prov = os.getenv("TTS_PROVIDER","openai")
    if prov != "openai":
        raise NotImplementedError("Only OpenAI TTS wired in demo")
    key = os.getenv("OPENAI_API_KEY")
    voice = os.getenv("TTS_VOICE","alloy")
    with httpx.Client(timeout=60) as c:
        r = c.post(
          "https://api.openai.com/v1/audio/speech",
          headers={"Authorization": f"Bearer {key}"},
          json={"model":"gpt-4o-mini-tts","voice":voice,"input":text}
        )
        r.raise_for_status()
        with open(out_path,"wb") as f: f.write(r.content)
    return out_path
