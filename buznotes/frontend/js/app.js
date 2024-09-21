// Функция для перевода текста через API
async function translateText() {
    const userId = document.querySelector('#user_id').value;
    const text = document.querySelector('#text_input').value;

    const response = await fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, text: text })
    });

    const data = await response.json();
    document.querySelector('#translated_text').innerText = data.translated_text;
}

// Сохранение заметки
async function saveNote() {
    const userId = document.querySelector('#user_id').value;
    const text = document.querySelector('#text_input').value;

    const response = await fetch('/save_note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, text: text })
    });

    if (response.ok) {
        alert('Заметка сохранена!');
    }
}
