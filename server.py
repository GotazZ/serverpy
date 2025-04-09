from flask import Flask, request, render_template_string
import socket
import threading

app = Flask(__name__)

HOST = '192.168.1.28'
PORT = 8000

html_form = """
<!doctype html>
<title>Envoyer un message</title>
<h2>Envoyer un message via socket</h2>
<form method=post>
  <label for="first">Premier message :</label>
  <select name="first" required>
    <option value="nouveau">nouveau</option>
    <option value="delete">delete</option>
  </select><br><br>
  <label for="second">Deuxième message :</label>
  <input type="text" name="second" required><br><br>
  <input type="submit" value="Envoyer">
</form>
{% if success %}
<p style="color: green;">Message envoyé avec succès à {{ addr }}</p>
{% endif %}
"""

# Fonction de socket dans un thread
def socket_server(first_message, second_message, result):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"En écoute sur {HOST}:{PORT}...")
        conn, addr = s.accept()
        with conn:
            print('Connecté par', addr)
            conn.sendall(first_message.encode('utf-8'))
            conn.sendall(second_message.encode('utf-8'))
            result['addr'] = addr

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        first_message = request.form['first'].strip().lower()
        second_message = request.form['second']
        server_thread = threading.Thread(target=socket_server, args=(first_message, second_message, result))
        server_thread.start()
        server_thread.join()
        return render_template_string(html_form, success=True, addr=result.get('addr'))
    return render_template_string(html_form, success=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
