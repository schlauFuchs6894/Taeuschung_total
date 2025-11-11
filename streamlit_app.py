import streamlit as st
import random

# Initialisierung
if "spieler_anzahl" not in st.session_state:
    st.session_state.spieler_anzahl = None
if "aktueller_spieler" not in st.session_state:
    st.session_state.aktueller_spieler = 1
if "begriffe" not in st.session_state:
    st.session_state.begriffe = ["Apfel", "Banane", "Kirsche", "Birne"]
if "impersonator" not in st.session_state:
    st.session_state.impersonator = None
if "spiel_start" not in st.session_state:
    st.session_state.spiel_start = False
if "abstimmung" not in st.session_state:
    st.session_state.abstimmung = None
if "stimmen" not in st.session_state:
    st.session_state.stimmen = None
if "abstimmender_spieler" not in st.session_state:
    st.session_state.abstimmender_spieler = 1

# Schritt 1: Anzahl der Spieler wählen
if st.session_state.spieler_anzahl is None:
    st.title("🕵️ Imposter-Spiel")
    st.session_state.spieler_anzahl = st.number_input("Wie viele Spieler machen mit?", min_value=2, max_value=10, step=1)
    if st.button("Spiel starten"):
        st.session_state.impersonator = random.randint(1, st.session_state.spieler_anzahl)
        st.session_state.spiel_start = True
        st.experimental_rerun()

# Schritt 2: Spieler sind dran
elif st.session_state.spiel_start and st.session_state.aktueller_spieler <= st.session_state.spieler_anzahl:
    st.title(f"Spieler {st.session_state.aktueller_spieler} ist dran")
    if st.button(f"Ich bin Spieler {st.session_state.aktueller_spieler}"):
        if st.session_state.aktueller_spieler == st.session_state.impersonator:
            st.write("Du bist der Imposter! Versuche, dich nicht zu verraten 😈")
        else:
            begriff = random.choice(st.session_state.begriffe)
            st.write(f"Dein Begriff ist: **{begriff}**")
        if st.button("Weiter"):
            st.session_state.aktueller_spieler += 1
            st.experimental_rerun()

# Schritt 3: Abstimmung vorbereiten
elif st.session_state.aktueller_spieler > st.session_state.spieler_anzahl and st.session_state.abstimmung is None:
    st.title("🗳️ Abstimmung: Wer ist der Imposter?")
    st.session_state.abstimmung = [None] * st.session_state.spieler_anzahl
    st.session_state.stimmen = [0] * st.session_state.spieler_anzahl
    st.experimental_rerun()

# Schritt 4: Jeder Spieler stimmt ab
elif None in st.session_state.abstimmung:
    spieler = st.session_state.abstimmender_spieler
    st.title(f"Spieler {spieler} stimmt ab")
    auswahl = st.selectbox(f"Spieler {spieler}, wer ist der Imposter?", [f"Spieler {i}" for i in range(1, st.session_state.spieler_anzahl + 1)])
    if st.button("Abstimmen"):
        gewählte_nummer = int(auswahl.split()[-1])
        st.session_state.abstimmung[spieler - 1] = gewählte_nummer
        st.session_state.stimmen[gewählte_nummer - 1] += 1
        st.session_state.abstimmender_spieler += 1
        st.experimental_rerun()

# Schritt 5: Ergebnis anzeigen
else:
    st.title("📢 Ergebnis der Abstimmung")
    max_stimmen = max(st.session_state.stimmen)
    meistgewählt = [i + 1 for i, s in enumerate(st.session_state.stimmen) if s == max_stimmen]

    st.write("Die Spieler haben abgestimmt:")
    for i, stimme in enumerate(st.session_state.abstimmung, start=1):
        st.write(f"Spieler {i} hat für Spieler {stimme} gestimmt.")

    if st.session_state.impersonator in meistgewählt:
        st.success(f"🎉 Der Imposter (Spieler {st.session_state.impersonator}) wurde enttarnt! Die Gruppe gewinnt!")
    else:
        st.error(f"😈 Der Imposter (Spieler {st.session_state.impersonator}) wurde nicht erkannt. Der Imposter gewinnt!")

    if st.button("Neues Spiel starten"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
