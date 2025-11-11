import streamlit as st
import random

st.set_page_config(page_title="Imposter ohne Wort", page_icon="🕵️‍♂️")

# --- SESSION STATE SETUP ---
if "phase" not in st.session_state:
    st.session_state.phase = "setup"
if "num_players" not in st.session_state:
    st.session_state.num_players = 0
if "player_names" not in st.session_state:
    st.session_state.player_names = []
if "current_name" not in st.session_state:
    st.session_state.current_name = 1
if "current_player" not in st.session_state:
    st.session_state.current_player = 1
if "imposter" not in st.session_state:
    st.session_state.imposter = None
if "word" not in st.session_state:
    st.session_state.word = ""
if "votes" not in st.session_state:
    st.session_state.votes = {}
if "voting_player" not in st.session_state:
    st.session_state.voting_player = 1
if "winner" not in st.session_state:
    st.session_state.winner = None

# --- WORTLISTE ---
word_list = [
    "Apfel", "Schule", "Auto", "Katze", "Pizza", "Fernsehen", "Zug",
    "Zahnarzt", "Tisch", "Computer", "Hund", "Meer", "Buch", "Ball", "Haus"
]

# --- SETUP PHASE ---
if st.session_state.phase == "setup":
    st.title("🕵️‍♂️ Imposter ohne Wort")
    st.write("Gib die Anzahl der Spieler ein und starte das Spiel.")

    num = st.number_input("Anzahl der Spieler:", min_value=3, max_value=10, step=1)
    if st.button("Weiter"):
        st.session_state.num_players = num
        st.session_state.phase = "names"
        st.session_state.player_names = []
        st.session_state.current_name = 1
        st.rerun()

# --- NAMEN EINGEBEN PHASE ---
elif st.session_state.phase == "names":
    st.title("👥 Spielernamen eingeben")
    st.write(f"Wie heißt Spieler {st.session_state.current_name}?")

    # einzigartiger Key, damit Streamlit den Input pro Spieler trennt
    input_key = f"name_input_{st.session_state.current_name}"
    name = st.text_input("Name eingeben:", key=input_key)

    if st.button("Speichern"):
        if name.strip() != "":
            st.session_state.player_names.append(name.strip())

            # Wichtig: Kein direkter Zugriff auf session_state[input_key] mehr!
            # Dadurch kein StreamlitAPIException-Fehler.

            # Wenn noch Spieler fehlen → nächster Name
            if len(st.session_state.player_names) < st.session_state.num_players:
                st.session_state.current_name += 1
            else:
                st.session_state.phase = "name_review"
            st.rerun()
        else:
            st.warning("Bitte einen gültigen Namen eingeben.")


# --- NAMENSÜBERSICHT PHASE ---
elif st.session_state.phase == "name_review":
    st.title("✅ Teilnehmerübersicht")
    st.write("Alle Spieler wurden erfolgreich eingetragen:")

    for i, name in enumerate(st.session_state.player_names, start=1):
        st.write(f"**Spieler {i}:** {name}")

    if st.button("Spiel starten 🚀"):
        st.session_state.imposter = random.randint(1, st.session_state.num_players)
        st.session_state.word = random.choice(word_list)
        st.session_state.phase = "show_word"
        st.session_state.current_player = 1
        st.rerun()

# --- SHOW WORD PHASE ---
elif st.session_state.phase == "show_word":
    st.title("Spieler-Runde")
    name = st.session_state.player_names[st.session_state.current_player - 1]
    st.write(f"👉 {name} ist dran.")

    if st.button(f"Ich bin {name}"):
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
            st.session_state.phase = "discussion"

# --- DISCUSSION PHASE ---
elif st.session_state.phase == "discussion":
    st.title("💬 Diskussionsrunde")
    st.write("Jetzt sagt **jeder Spieler ein Wort** zu dem Thema oder beschreibt es kurz, "
             "ohne das Wort direkt zu nennen. Der Imposter muss versuchen mitzuhalten!")

    st.info("Wenn ihr fertig seid mit der Runde, klickt auf **Weiter zur Abstimmung**.")

    if st.button("Weiter zur Abstimmung 🗳️"):
        st.session_state.phase = "voting"
        st.session_state.votes = {name: 0 for name in st.session_state.player_names}
        st.session_state.voting_player = 1
        st.rerun()


# --- VOTING PHASE ---
elif st.session_state.phase == "voting":
    st.title("🗳️ Abstimmung")
    current_voter_name = st.session_state.player_names[st.session_state.voting_player - 1]
    st.subheader(f"Jetzt stimmt ab: {current_voter_name}")

    # Nur Spieler auswählen, nicht sich selbst
    options = [
        name for name in st.session_state.player_names
        if name != current_voter_name
    ]
    choice = st.selectbox("Wähle den verdächtigen Spieler:", options)

    if st.button("Stimme abgeben"):
        st.session_state.votes[choice] += 1

        # Nächster Spieler oder Ergebnis
        if st.session_state.voting_player < st.session_state.num_players:
            st.session_state.voting_player += 1
        else:
            st.session_state.phase = "result"
        st.rerun()

# --- RESULT PHASE ---
elif st.session_state.phase == "result":
    st.title("🏁 Ergebnis")

    max_votes = max(st.session_state.votes.values())
    most_voted = [p for p, v in st.session_state.votes.items() if v == max_votes]

    imposter_name = st.session_state.player_names[st.session_state.imposter - 1]

    if imposter_name in most_voted:
        st.success("🎉 Die Gruppe gewinnt! Der Imposter wurde enttarnt!")
    else:
        st.error("😈 Der Imposter gewinnt! Niemand hat ihn erkannt!")

    st.write(f"Der Imposter war: **{imposter_name}**")
    st.write(f"Das Wort war: **{st.session_state.word}**")

    st.write("### 📊 Stimmenübersicht:")
    for player, votes in st.session_state.votes.items():
        st.write(f"{player}: {votes} Stimmen")

    if st.button("🔁 Noch ein Spiel"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
