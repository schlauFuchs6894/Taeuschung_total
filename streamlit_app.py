import streamlit as st
import random

# Session-State initialisieren
for key, default in {
    "step": "setup",
    "players": [],
    "words": [],
    "imposter": None,
    "current_player": 0,
    "votes": {},
    "revealed": False,
    "has_seen_word": False,
    "show_word": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Schritt 1: Setup
if st.session_state.step == "setup":
    st.title("🕵️ Imposter-Spiel")
    num_players = st.number_input("Wie viele Spieler machen mit?", min_value=3, max_value=10, step=1)
    if st.button("Spiel starten"):
        st.session_state.players = [f"Spieler {i+1}" for i in range(num_players)]
        st.session_state.words = ["Apfel"] * (num_players - 1) + ["Du bist der Imposter!"]
        random.shuffle(st.session_state.words)
        st.session_state.step = "play"
        st.session_state.current_player = 0
        st.session_state.votes = {}
        st.session_state.revealed = False
        st.session_state.has_seen_word = False
        st.session_state.show_word = False

# Schritt 2: Spieler sehen ihr Wort
elif st.session_state.step == "play":
    player = st.session_state.players[st.session_state.current_player]
    st.header(f"{player} ist dran")

    if not st.session_state.has_seen_word:
        if st.button(f"Ich bin {player}"):
            st.session_state.has_seen_word = True
            st.session_state.show_word = True

    if st.session_state.show_word:
        word = st.session_state.words[st.session_state.current_player]
        st.write(f"Dein Wort: **{word}**")
        if st.button("Weiter"):
            st.session_state.current_player += 1
            st.session_state.has_seen_word = False
            st.session_state.show_word = False
            if st.session_state.current_player >= len(st.session_state.players):
                st.session_state.step = "vote"

# Schritt 3: Abstimmung
elif st.session_state.step == "vote":
    st.title("🗳️ Abstimmung: Wer ist der Imposter?")

    for player in st.session_state.players:
        with st.expander(f"{player} stimmt ab"):
            if player not in st.session_state.votes:
                vote = st.radio("Wähle den Imposter:", st.session_state.players, key=f"vote_{player}")
                if st.button("Abstimmen", key=f"submit_{player}"):
                    st.session_state.votes[player] = vote
                    st.success(f"{player} hat abgestimmt.")
            else:
                st.info(f"{player} hat bereits abgestimmt.")

    if len(st.session_state.votes) == len(st.session_state.players) and not st.session_state.revealed:
        st.subheader("📊 Auswertung")
        tally = {}
        for vote in st.session_state.votes.values():
            tally[vote] = tally.get(vote, 0) + 1
        voted_out = max(tally, key=tally.get)

        imposter_index = st.session_state.words.index("Du bist der Imposter!")
        imposter_name = st.session_state.players[imposter_index]

        st.write(f"Die Gruppe hat **{voted_out}** gewählt.")
        st.write(f"🔍 Der Imposter war: **{imposter_name}**")

        if voted_out == imposter_name:
            st.success("🎉 Die Gruppe hat gewonnen! Der Imposter wurde enttarnt.")
        else:
            st.error(f"😈 Der Imposter **{imposter_name}** hat gewonnen!")

        st.session_state.revealed = True

    if st.session_state.revealed:
        if st.button("🔁 Neues Spiel starten"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
