import streamlit as st
import random

# Initialisiere Session State
if "step" not in st.session_state:
    st.session_state.step = "setup"
    st.session_state.players = []
    st.session_state.words = []
    st.session_state.imposter = None
    st.session_state.current_player = 0
    st.session_state.confirmed = False
    st.session_state.votes = {}

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
        st.session_state.confirmed = False

# Schritt 2: Spieler sehen ihr Wort
elif st.session_state.step == "play":
    player = st.session_state.players[st.session_state.current_player]
    st.header(f"{player} ist dran")

    if not st.session_state.confirmed:
        if st.button(f"Ich bin {player}"):
            word = st.session_state.words[st.session_state.current_player]
            st.write(f"Dein Wort: **{word}**")
            st.session_state.confirmed = True
    else:
        if st.button("Weiter"):
            st.session_state.current_player += 1
            st.session_state.confirmed = False
            if st.session_state.current_player >= len(st.session_state.players):
                st.session_state.step = "vote"

# Schritt 3: Abstimmung
elif st.session_state.step == "vote":
    st.title("🗳️ Abstimmung: Wer ist der Imposter?")
    for player in st.session_state.players:
        vote = st.radio(f"Stimme von {player}", st.session_state.players, key=player)
        st.session_state.votes[player] = vote

    if st.button("Auswertung"):
        # Stimmen auszählen
        tally = {}
        for vote in st.session_state.votes.values():
            tally[vote] = tally.get(vote, 0) + 1
        voted_out = max(tally, key=tally.get)

        # Wer war der Imposter?
        imposter_index = st.session_state.words.index("Du bist der Imposter!")
        imposter_name = st.session_state.players[imposter_index]

        st.write(f"Die Gruppe hat **{voted_out}** gewählt.")
        if voted_out == imposter_name:
            st.success("🎉 Die Gruppe hat gewonnen! Der Imposter wurde enttarnt.")
        else:
            st.error(f"😈 Der Imposter **{imposter_name}** hat gewonnen!")

        # Neustart-Button
        if st.button("Neues Spiel starten"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
