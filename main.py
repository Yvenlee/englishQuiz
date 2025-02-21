import streamlit as st
import json
import random

# Charger le fichier JSON
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

categories = list(data.keys())

for key in ["category", "word", "correct_answer", "choices", "user_answer", "quiz_ready", "validated", "score"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "score" else 0

def generate_question(category):
    words = list(data[category].keys())
    word = random.choice(words)
    correct_answer = data[category][word]

    # Générer 2 mauvaises réponses aléatoires
    all_answers = list(data[category].values())
    all_answers.remove(correct_answer)
    wrong_answers = random.sample(all_answers, min(2, len(all_answers)))

    choices = wrong_answers + [correct_answer]
    random.shuffle(choices)

    st.session_state.update({
        "category": category,
        "word": word,
        "correct_answer": correct_answer,
        "choices": choices,
        "user_answer": None,
        "quiz_ready": True,
        "validated": False
    })

st.markdown("<h1 style='text-align: center;'>📝 Apprentissage de l'anglais</h1>", unsafe_allow_html=True)

category = st.selectbox("📚 Choisissez une catégorie :", categories)

if st.button("🔄 Nouvelle question", use_container_width=True, key="new_question_main") or not st.session_state.quiz_ready:
    generate_question(category)

if st.session_state.quiz_ready:
    st.subheader(f"🔤 Quelle est la traduction de **'{st.session_state.word}'** en français ?")

    user_choice = st.radio(
        "Sélectionnez votre réponse:", 
        st.session_state.choices, 
        index=None, 
        horizontal=True
    )

    validate_button = st.button("✅ Valider", use_container_width=True, key="validate_button", disabled=user_choice is None)

    if validate_button and user_choice:
        st.session_state.user_answer = user_choice
        st.session_state.validated = True

        if user_choice == st.session_state.correct_answer:
            st.session_state.score += 1
            st.success("✅ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. La bonne réponse était : **{st.session_state.correct_answer}**.")

    st.markdown(f"<h3 style='text-align: center;'>🌟 Score : {st.session_state.score}</h3>", unsafe_allow_html=True)
