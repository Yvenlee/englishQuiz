import streamlit as st
import json
import random

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

categories = list(data.keys())

# Initialisation des variables de session
for key, default in {"category": None, "word": None, "correct_answer": None, "choices": None, 
                      "user_answer": None, "quiz_ready": False, "validated": False, "score": 0, "question_count": 0, "answered_correctly": {}}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def generate_question(category):
    if st.session_state.question_count >= 10:
        return
    
    words = [word for word in data[category].keys() if word not in st.session_state.answered_correctly]
    
    if not words:
        st.session_state.answered_correctly = {}
        words = list(data[category].keys())
    
    word = random.choice(words)
    correct_answer = data[category][word]

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

def reset_quiz():
    st.session_state.update({
        "score": 0,
        "question_count": 0,
        "quiz_ready": False,
        "validated": False,
    })
    generate_question(st.session_state.category)

st.markdown("<h1 style='text-align: center; font-size: 24px;'>📝 Améliorer le vocabulaire</h1>", unsafe_allow_html=True)

new_category = st.selectbox("📚 Choisissez une catégorie :", categories, index=categories.index(st.session_state.category) if st.session_state.category in categories else 0)

if new_category != st.session_state.category:
    st.session_state.category = new_category
    reset_quiz()

if st.button("🔄 Nouvelle question", use_container_width=True, key="new_question_main") or not st.session_state.quiz_ready:
    generate_question(st.session_state.category)

if st.session_state.quiz_ready and st.session_state.question_count < 10:
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
        st.session_state.question_count += 1

        if user_choice == st.session_state.correct_answer:
            st.session_state.score += 1
            st.session_state.answered_correctly[st.session_state.word] = True
            st.success("✅ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. La bonne réponse était : **{st.session_state.correct_answer}**.")

    st.markdown(f"<h3 style='text-align: center; font-size: 18px;'>🌟 Score : {st.session_state.score} / 10 | Questions : {st.session_state.question_count} / 10</h3>", unsafe_allow_html=True)

if st.session_state.question_count >= 10:
    st.warning("📌 Vous avez atteint la limite de 10 questions.")
    if st.button("🔁 Recommencer", use_container_width=True, key="restart_button"):
        reset_quiz()
