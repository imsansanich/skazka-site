import streamlit as st
import google.generativeai as genai
import urllib.parse

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(
    page_title="Magic Story Generator",
    page_icon="✨",
    layout="centered"
)

# --- ПЕРЕВОДЫ (RU, EN, UKR) ---
TRANSLATIONS = {
    "Русский 🇷🇺": {
        "title": "✨ Генератор сказок",
        "desc": "Введи имя и тему, а ИИ придумает сказку и нарисует картинку!",
        "name_label": "Как зовут ребенка?",
        "topic_label": "О чем будет сказка?",
        "topic_placeholder": "Например: про космос",
        "button": "🚀 Придумать сказку!",
        "loading": "🧙‍♂️ Сказочник сочиняет историю...",
        "image_loading": "🎨 Художник рисует иллюстрацию...",
        "success": "Сказка готова!",
        "error_key": "Укажите API ключ в настройках слева!"
    },
    "English 🇺🇸": {
        "title": "✨ Magic Story Generator",
        "desc": "Enter a name and topic, AI will create a story and a picture!",
        "name_label": "Child's name?",
        "topic_label": "What is the story about?",
        "topic_placeholder": "E.g. space adventure",
        "button": "🚀 Generate Story!",
        "loading": "🧙‍♂️ The Storyteller is writing...",
        "image_loading": "🎨 Drawing the illustration...",
        "success": "Story is ready!",
        "error_key": "Please enter API Key in settings!"
    },
    "Українська 🇺🇦": {
        "title": "✨ Генератор казок",
        "desc": "Введи ім'я та тему, а ШІ вигадає казку та намалює малюнок!",
        "name_label": "Як звати дитину?",
        "topic_label": "Про що буде казка?",
        "topic_placeholder": "Наприклад: про космос",
        "button": "🚀 Придумати казку!",
        "loading": "🧙‍♂️ Казкар складає історію...",
        "image_loading": "🎨 Художник малює ілюстрацію...",
        "success": "Казка готова!",
        "error_key": "Вкажіть API ключ у налаштуваннях зліва!"
    }
}

# --- ФУНКЦИИ ---

def generate_story(api_key, child_name, topic, language_name):
    """Генерирует текст сказки через Google Gemini."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Промпт для ИИ
        prompt = f"""
        Role: Kind children's storyteller.
        Task: Write a short, magical story.
        
        INPUTS:
        Child's name: {child_name if child_name else "Hero"}
        Topic: {topic if topic else "Magic adventure"}
        LANGUAGE: Write the story strictly in {language_name}.
        
        INSTRUCTIONS:
        1. Kind, safe, no scary moments.
        2. Use the child's name.
        3. Length: 4-5 paragraphs.
        
        IMPORTANT ENDING:
        At the very end, strictly on a new line, write: '---IMAGE_PROMPT---'
        Then write a short visual description for the story in ENGLISH (for the image generator).
        Example: "Cute fluffy cat in space suit, cartoon style."
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return None

def get_image_url(prompt_text):
    """Генерирует ссылку на картинку."""
    encoded_prompt = urllib.parse.quote(prompt_text)
    # Добавляем стиль
    style = " children book illustration, cute style, soft colors, masterpiece, 4k"
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}{style}"

# --- ИНТЕРФЕЙС ---

# 1. Сайдбар (Выбор языка и Ключ)
with st.sidebar:
    st.header("Settings / Настройки")
    selected_lang = st.selectbox("Language / Язык", list(TRANSLATIONS.keys()))
    
    st.divider()

# 2. Основная часть
t = TRANSLATIONS[selected_lang] # Берем переводы для выбранного языка

st.title(t["title"])
st.write(t["desc"])

col1, col2 = st.columns(2)
with col1:
    name = st.text_input(t["name_label"])
with col2:
    topic = st.text_input(t["topic_label"], placeholder=t["topic_placeholder"])

if st.button(t["button"], type="primary", use_container_width=True):
    if not api_key:
        st.error(t["error_key"])
    else:
        # ГЕНЕРАЦИЯ ТЕКСТА
        with st.spinner(t["loading"]):
            # Передаем название языка (например "Українська 🇺🇦") в функцию
            full_text = generate_story(api_key, name, topic, selected_lang)
        
        if full_text:
            # Разбираем ответ на текст и промпт картинки
            parts = full_text.split('---IMAGE_PROMPT---')
            story = parts[0].strip()
            img_prompt = parts[1].strip() if len(parts) > 1 else ""

            # Вывод сказки
            st.success(t["success"])
            st.markdown(f"### 📖 {name}")
            st.write(story)

            # ГЕНЕРАЦИЯ КАРТИНКИ
            if img_prompt:
                with st.spinner(t["image_loading"]):
                    img_url = get_image_url(img_prompt)
                    st.image(img_url, use_column_width=True)
        else:

            st.error("Error/Ошибка: Проверьте API Key или VPN.")


