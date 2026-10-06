import asyncio
import streamlit as st
import edge_tts

# Pagina configuratie
st.set_page_config(page_title="Gratis Text-to-Speech", page_icon="🎙️")
st.title("🎙️ Gratis AI Text-to-Speech Converter")
st.write("Converteer tekst naar spraak met natuurlijke stemmen, zonder API-sleutels.")

# Tekst invoer met jouw originele tekst als standaard
default_text = (
    "In life... we remember moments. Not days. Not years. Moments. "
    "And for thirty years... you gave us moments that became memories. "
    "Memories... that became traditions. Traditions... that became a family. "
    "Tonight... we celebrate every person who walked through these doors. "
    "Every friend who returned. Every laugh. Every embrace. Every dance. "
    "You gave this place its soul. You turned music into something bigger than sound. "
    "You turned strangers into friends. And friends... into family. "
    "From the bottom of our hearts... thank you for thirty extraordinary years. "
    "This is not an ending. This is a legacy. And that legacy... is you."
)

text_input = st.text_area("Voer je tekst in:", value=default_text, height=250)

# Instellingen voor de stem
col1, col2 = st.columns(2)
with col1:
    # en-US-GuyNeural is de stem uit je originele Azure-bestand
    voice_option = st.selectbox(
        "Kies een stem:",
        ["en-US-GuyNeural", "en-US-AriaNeural", "nl-NL-MaartenNeural", "nl-NL-ColetteNeural"]
    )
with col2:
    speed = st.slider("Spraaksnelheid (Rate):", min_value=-50, max_value=50, value=-20, step=5)

# Toonhoogte aanpassing (Pitch)
pitch = st.slider("Toonhoogte (Pitch):", min_value=-50, max_value=50, value=-12, step=5)

output_filename = "output_free.mp3"

# Asynchrone functie om de audio te genereren via edge-tts
async def generate_audio(text, voice, rate_val, pitch_val, output_file):
    # Formateer de parameters zoals edge-tts dat verwacht (bijv. "-20%" of "+0%")
    rate_str = f"{rate_val:+d}%" if rate_val != 0 else "+0%"
    pitch_str = f"{pitch_val:+d}%" if pitch_val != 0 else "+0%"
    
    communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
    await communicate.save(output_file)

if st.button("Genereer en Beluister Audio", type="primary"):
    if not text_input.strip():
        st.warning("Voer eerst wat tekst in.")
    else:
        with st.spinner("Bezig met het genereren van de audio..."):
            try:
                # Start het asynchrone proces
                asyncio.run(generate_audio(text_input, voice_option, speed, pitch, output_filename))
                
                st.success("🎉 Audio succesvol gegenereerd!")
                
                # Lees het gegenereerde MP3-bestand in
                with open(output_filename, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                
                # Toon de audioplayer en downloadknop
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(
                    label="Download MP3-bestand",
                    data=audio_bytes,
                    file_name=output_filename,
                    mime="audio/mp3"
                )
            except Exception as e:
                st.error(f"Er is een fout opgetreden: {e}")
