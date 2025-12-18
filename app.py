from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import imagehash
import os
import json # 1. Імпортуємо модуль JSON
import time

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

DB_FILE = 'database.json'

# --- ФУНКЦІЇ ДЛЯ РОБОТИ З JSON ---
def load_db():
    if not os.path.exists(DB_FILE):
        return [] # Якщо файлу немає, повертаємо пустий список
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4) # indent=4 робить файл красивим для читання

# --- ОСНОВНИЙ КОД ---

@app.route('/')
def root():
    return send_from_directory('.', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = file.filename # Зберігаємо назву файлу
    
    try:
        img = Image.open(file.stream)
        p_hash = str(imagehash.phash(img))
        
        # 2. Завантажуємо актуальну базу з файлу
        known_hashes = load_db()
        
        threshold = 5
        current_hash_obj = imagehash.hex_to_hash(p_hash)
        
        # Перевірка на плагіат
        for entry in known_hashes:
            existing_p_hash = entry['pHash'] # Тепер ми беремо хеш з об'єкта
            existing_obj = imagehash.hex_to_hash(existing_p_hash)
            
            if current_hash_obj - existing_obj < threshold:
                return jsonify({
                    "success": False,
                    "message": f"PLAGIARISM DETECTED! Similar to '{entry['filename']}'",
                    "pHash": p_hash
                })

        # 3. Якщо унікальний - додаємо запис у JSON
        new_record = {
            "pHash": p_hash,
            "filename": filename,
            "timestamp": time.time()
        }
        known_hashes.append(new_record)
        save_db(known_hashes) # Зберігаємо на диск
        
        return jsonify({
            "success": True,
            "message": "Content is unique. Saved to DB & Ready for Blockchain.",
            "pHash": p_hash
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🌍 DApp with JSON DB is running on http://127.0.0.1:5000")
    app.run(debug=True)