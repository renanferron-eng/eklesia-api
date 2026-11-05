from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright
import time

app = Flask(__name__)

@app.route('/gerar-relatorio', methods=['POST'])
def gerar_relatorio():
    dados = request.get_json() or {}
    tipo_filtro = dados.get('filtro', 'INSCRIÇÕES VIAGEM MISSIONÁRIA')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            page.goto("https://gestaoweb.eklesiaonline.com.br/login", wait_until="networkidle")
            page.fill("input[name='login']", "renanferron@gmail.com")
            page.fill("input[name='senha']", "Lu1z4.B34tr1z")
            page.click("button[type='submit']")
            page.wait_for_timeout(3000)

            url_gerador = f"https://gestaoweb.eklesiaonline.com.br/relatorios/index/Eventos/Gerador/relatorio?filtro={tipo_filtro}"
            page.goto(url_gerador, wait_until="networkidle")
            page.wait_for_timeout(4000)

            browser.close()
            return jsonify({
                "sucesso": True,
                "mensagem": "Sessão e dados renderizados com sucesso no Render!"
            })

        except Exception as e:
            browser.close()
            return jsonify({"sucesso": False, "erro": str(e)}), 500

if __name__ == '__main__':
    app.run()
