import streamlit as st
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# --- PAGE CONFIG ---
st.set_page_config(page_title="Imposter ohne Wort", page_icon="🕵️‍♂️")

# --- DESIGN THEME ---
mode = st.radio("🌗 Wähle Design:", ["Hell", "Dunkel"], horizontal=True)

if mode == "Dunkel":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: #f5f5f5;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #fafafa;
            color: #111111;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- SESSION STATE SETUP ---
if "phase" not in st.session_state:
    st.session_state.phase = "setup"
if "num_players" not in st.session_state:
    st.session_state.num_players = 0
if "current_player" not in st.session_state:
    st.session_state.current_player = 1
if "imposter" not in st.session_state:
    st.session_state.imposter = None
if "word" not in st.session_state:
    st.session_state.word = ""
if "votes" not in st.session_state:
    st.session_state.votes = {}
if "winner" not in st.session_state:
    st.session_state.winner = None

# --- WORTKATEGORIEN ---
word_categories = {
    "Essen 🍕": ["Pizza", "Apfel", "Brot", "Nudel", "Käse"],
    "Tiere 🐶": ["Hund", "Katze", "Pferd", "Elefant", "Vogel"],
    "Orte 🌍": ["Schule", "Zahnarzt", "Bahnhof", "Park", "Haus"],
    "Gegenstände 🪑": ["Tisch", "Stuhl", "Lampe", "Computer", "Buch"]
}

# --- SETUP PHASE ---
if st.session_state.phase == "setup":
    st.title("🕵️‍♂️ Imposter ohne Wort")
    st.write("Willkommen! Gib die Anzahl der Spieler ein und wähle ein Thema oder ein eigenes Wort.")

    num = st.number_input("👥 Anzahl der Spieler:", min_value=3, max_value=10, step=1)

    category = st.selectbox(
        "📚 Wähle eine Kategorie:",
        list(word_categories.keys()) + ["Eigenes Wort eingeben"]
    )

    if category == "Eigenes Wort eingeben":
        custom_word = st.text_input("✏️ Gib dein eigenes Wort ein:")
    else:
        custom_word = None

    if st.button("🎮 Spiel starten"):
        st.session_state.num_players = num
        st.session_state.imposter = random.randint(1, num)
        if custom_word:
            st.session_state.word = custom_word
        else:
            st.session_state.word = random.choice(word_categories[category])
        st.session_state.phase = "show_word"
        st.session_state.current_player = 1
        st.rerun()

# --- SHOW WORD PHASE ---
elif st.session_state.phase == "show_word":
    st.title("🎭 Spieler-Runde")
    st.write(f"👉 Spieler {st.session_state.current_player} ist dran.")

    if st.button(f"Ich bin Spieler {st.session_state.current_player}"):
        if st.session_state.current_player == st.session_state.imposter:
            st.session_state.reveal = "Du bist der Imposter 😈"
        else:
            st.session_state.reveal = f"Dein Wort ist: **{st.session_state.word}**"
        st.session_state.phase = "reveal"
        st.rerun()

# --- REVEAL PHASE ---
elif st.session_state.phase == "reveal":
    st.subheader(st.session_state.reveal)
    if st.button("Weiter"):
        if st.session_state.current_player < st.session_state.num_players:
            st.session_state.current_player += 1
            st.session_state.phase = "show_word"
        else:
            st.session_state.phase = "voting"
            st.session_state.votes = {i: 0 for i in range(1, st.session_state.num_players + 1)}
        st.rerun()

# --- VOTING PHASE ---
elif st.session_state.phase == "voting":
    st.title("🗳️ Abstimmung")
    st.write("Jetzt stimmt jeder ab, wer der Imposter ist!")

    voted = st.number_input(
        "Gib die Nummer des verdächtigen Spielers ein:",
        min_value=1, max_value=st.session_state.num_players, step=1
    )

    if st.button("Stimme abgeben"):
        st.session_state.votes[voted] += 1
        total_votes = sum(st.session_state.votes.values())
        if total_votes >= st.session_state.num_players:
            st.session_state.phase = "result"
        st.rerun()

# --- RESULT PHASE ---
elif st.session_state.phase == "result":
    st.title("🏁 Ergebnis")

    max_votes = max(st.session_state.votes.values())
    most_voted = [p for p, v in st.session_state.votes.items() if v == max_votes]

    if st.session_state.imposter in most_voted:
        st.success("🎉 Die Gruppe gewinnt! Der Imposter wurde enttarnt!")
    else:
        st.error("😈 Der Imposter gewinnt! Niemand hat ihn erkannt!")

    st.write(f"Der Imposter war: **Spieler {st.session_state.imposter}**")
    st.write(f"Das Wort war: **{st.session_state.word}**")

if st.button("📄 Ergebnis speichern (Textdatei)"):
    result_text = f"""
    🕵️‍♂️ Imposter ohne Wort - Spielergebnis
    ---------------------------------------
    Anzahl Spieler: {st.session_state.num_players}
    Imposter: Spieler {st.session_state.imposter}
    Wort: {st.session_state.word}

    Abstimmungsergebnisse:
    """
    for p, v in st.session_state.votes.items():
        result_text += f"\nSpieler {p}: {v} Stimmen"

    st.download_button("📥 Download Ergebnis als TXT",
                       data=result_text.encode("utf-8"),
                       file_name="imposter_ergebnis.txt")


    if st.button("🔁 Noch ein Spiel"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
