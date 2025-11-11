import streamlit as st
import random

st.set_page_config(page_title="Imposter ohne Wort", page_icon="🕵️‍♂️")

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
if "names" not in st.session_state:
    st.session_state.names = {}
if "current_name" not in st.session_state:
    st.session_state.current_name = 1
if "reveal" not in st.session_state:
    st.session_state.reveal = ""

# --- WORTLISTE ---
word_categories = {
    "Allgemein": ["Apfel", "Schule", "Auto", "Katze", "Pizza", "Zug", "Haus"],
    "Tiere": ["Hund", "Katze", "Elefant", "Pferd", "Vogel", "Affe", "Fisch"],
    "Orte": ["Strand", "Wald", "Stadt", "Berge", "Zoo", "Schule", "Kino"],
    "Gegenstände": ["Buch", "Tisch", "Computer", "Ball", "Lampe", "Rucksack", "Stuhl"]
}

# --- SETUP PHASE ---
if st.session_state.phase == "setup":
    st.title("🕵️‍♂️ Imposter ohne Wort")
    st.write("Gib die Anzahl der Spieler ein und starte das Spiel.")

    num = st.number_input("👥 Anzahl der Spieler:", min_value=3, max_value=10, step=1)
    category = st.selectbox(
        "📚 Wähle eine Kategorie:",
        list(word_categories.keys()) + ["Eigenes Wort eingeben"]
    )

    # --- Eigenes Wort mit Komma-Unterstützung ---
    if category == "Eigenes Wort eingeben":
        custom_input = st.text_input(
            "✏️ Gib eigene Wörter ein (mit Komma getrennt):",
            placeholder="z. B. Apfel, Banane, Kiwi"
        )
        if custom_input:
            custom_words = [w.strip() for w in custom_input.split(",") if w.strip()]
            custom_word = random.choice(custom_words) if custom_words else None
        else:
            custom_word = None
    else:
        custom_word = None

    if st.button("🎮 Spiel starten"):
        st.session_state.num_players = num
        st.session_state.imposter = random.randint(1, num)
        st.session_state.word = custom_word if custom_word else random.choice(word_categories[category])
        st.session_state.phase = "name_input"
        st.session_state.current_name = 1
        st.session_state.names = {}
        st.rerun()

# --- NAME INPUT PHASE ---
elif st.session_state.phase == "name_input":
    st.title("🧾 Spielernamen eingeben")

    current = st.session_state.current_name
    name = st.text_input(f"Wie heißt Spieler {current}?", key=f"name_input_{current}")

    if st.button("✅ Namen speichern"):
        if name.strip() != "":
            st.session_state.names[current] = name.strip()
            if current < st.session_state.num_players:
                st.session_state.current_name += 1
                st.rerun()
            else:
                st.session_state.phase = "show_word"
                st.session_state.current_player = 1
                st.rerun()
        else:
            st.warning("Bitte gib einen Namen ein.")

# --- SHOW WORD PHASE ---
elif st.session_state.phase == "show_word":
    st.title("📜 Wortanzeige")
    current_player = st.session_state.current_player
    player_name = st.session_state.names.get(current_player, f"Spieler {current_player}")

    st.write(f"👉 Jetzt ist **{player_name}** dran!")

    if st.button(f"Ich bin {player_name}"):
        if current_player == st.session_state.imposter:
            st.session_state.reveal = "😈 Du bist der Imposter!"
        else:
            st.session_state.reveal = f"🔤 Dein Wort ist: **{st.session_state.word}**"
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
        st.rerun()

# --- DISCUSSION PHASE ---
elif st.session_state.phase == "discussion":
    st.title("💬 Diskussionsrunde")
    st.write("Jeder Spieler sagt **ein Wort**, das zu dem Thema passt (aber nicht zu eindeutig sein darf).")
    st.info("Tipp: Der Imposter kennt das Wort nicht – also gut bluffen 😏")

    if st.button("➡️ Zur Abstimmung"):
        st.session_state.phase = "voting"
        st.session_state.votes = {i: 0 for i in range(1, st.session_state.num_players + 1)}
        st.session_state.current_voter = 1
        st.rerun()

# --- VOTING PHASE ---
elif st.session_state.phase == "voting":
    st.title("🗳️ Abstimmung")

    voter = st.session_state.current_voter
    voter_name = st.session_state.names.get(voter, f"Spieler {voter}")
    st.write(f"👉 Jetzt stimmt **{voter_name}** ab!")

    voted = st.selectbox(
        "Wähle den verdächtigen Spieler:",
        [st.session_state.names[i] for i in range(1, st.session_state.num_players + 1)],
        key=f"vote_{voter}"
    )

    if st.button("✅ Stimme abgeben"):
        # Spielername in Nummer umwandeln
        voted_num = [k for k, v in st.session_state.names.items() if v == voted][0]
        st.session_state.votes[voted_num] += 1

        if voter < st.session_state.num_players:
            st.session_state.current_voter += 1
            st.rerun()
        else:
            st.session_state.phase = "result"
            st.rerun()

# --- RESULT PHASE ---
elif st.session_state.phase == "result":
    st.title("🏁 Ergebnis")

    max_votes = max(st.session_state.votes.values())
    most_voted = [p for p, v in st.session_state.votes.items() if v == max_votes]

    imposter_num = st.session_state.imposter
    imposter_name = st.session_state.names.get(imposter_num, f"Spieler {imposter_num}")

    if imposter_num in most_voted:
        st.success(f"🎉 Die Gruppe gewinnt! Der Imposter war **{imposter_name}**!")
    else:
        st.error(f"😈 Der Imposter ({imposter_name}) gewinnt! Niemand hat ihn erkannt!")

    st.write(f"Das Wort war: **{st.session_state.word}**")

    # --- TEXT EXPORT ---
    if st.button("📄 Ergebnis speichern (Textdatei)"):
        result_text = f"""
🕵️‍♂️ Imposter ohne Wort - Spielergebnis
---------------------------------------
Anzahl Spieler: {st.session_state.num_players}
Imposter: {imposter_name}
Wort: {st.session_state.word}

Abstimmungsergebnisse:
"""
        for i, v in st.session_state.votes.items():
            name = st.session_state.names.get(i, f"Spieler {i}")
            result_text += f"\n{name}: {v} Stimmen"

        st.download_button(
            "📥 Download Ergebnis als TXT",
            data=result_text.encode("utf-8"),
            file_name="imposter_ergebnis.txt"
        )

    if st.button("🔁 Neues Spiel starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
