import re
import requests
from flask import Flask, redirect, request

app = Flask(__name__)

@app.route("/")
def home():
    video_id = request.args.get("video", "x7wjrui")
    embed_url = f"https://dailymotion.com{video_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": "https://dailymotion.com"
    }
    
    try:
        response = requests.get(embed_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"Erro: {response.status_code}", response.status_code
            
        html_text = response.text
        match = re.search(r'"(https?:\\/\\/[^"]+?\.m3u8[^"]*?)"', html_text)
        
        if match:
            m3u8_url = match.group(1).replace(r"\/", "/")
            return redirect(m3u8_url, code=302)
            
        return "Link nao encontrado.", 404
        
    except Exception as e:
        return f"Erro interno: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
