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

# Woordenboeken met uitgebreide stemmen per taal
voices_en = {
    "Guy (Man - Serieus/Origineel)": "en-US-GuyNeural",
    "Andrew (Man - Nieuws/Formeel)": "en-US-AndrewNeural",
    "Brian (Man - Brits accent)": "en-GB-BrianNeural",
    "Aria (Vrouw - Vriendelijk)": "en-US-AriaNeural",
    "Jenny (Vrouw - Natuurlijk/Gesprek)": "en-US-JennyNeural",
    "Emma (Vrouw - Brits accent)": "en-GB-EmmaNeural"
}

voices_nl = {
    "Maarten (Man - Nederlands Standaard)": "nl-NL-MaartenNeural",
    "Fenna (Vrouw - Nederlands Standaard)": "nl-NL-FennaNeural",
    "Colette (Vrouw - Vlaams/Belgisch)": "nl-BE-ColetteNeural",
    "Arnaud (Man - Vlaams/Belgisch)": "nl-BE-ArnaudNeural"
}

# Instellingen voor de stem
col1, col2, col3 = st.columns(3)

with col1:
    # Kies eerst de taal
    language_option = st.selectbox("Kies taal:", ["Engels (US/GB)", "Nederlands / Vlaams"])

with col2:
    # Laad de stemmen op basis van de gekozen taal
    if language_option == "Engels (US/GB)":
        selected_voice_label = st.selectbox("Kies een stem:", list(voices_en.keys()))
        voice_id = voices_en[selected_voice_label]
    else:
        selected_voice_label = st.selectbox("Kies een stem:", list(voices_nl.keys()))
        voice_id = voices_nl[selected_voice_label]

with col3:
    speed = st.slider("Spraaksnelheid (Rate):", min_value=-50, max_value=50, value=-20, step=5)

# Toonhoogte aanpassing (Pitch)
pitch = st.slider("Toonhoogte (Pitch):", min_value=-50, max_value=50, value=-12, step=5)

output_filename = "output_free.mp3"

# Asynchrone functie om de audio te genereren via edge-tts
async def generate_audio(text, voice, rate_val, pitch_val, output_file):
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
                # Start het asynchrone proces met de geselecteerde voice_id
                asyncio.run(generate_audio(text_input, voice_id, speed, pitch, output_filename))
                
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
