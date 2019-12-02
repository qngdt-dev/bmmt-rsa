from rsa import RSA, modInverse
from flask import Flask, render_template, request, json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/postService', methods=['POST'])
def postService():
    if(request.form['serviceName'] == 'init'):
        p = int(request.form['p'])
        q = int(request.form['q'])
        rsa_ins = RSA(p, q)
        k_list = rsa_ins.generate_ed()
        print(k_list)
        return json.dumps({'status': 'OK', 'n': rsa_ins.n, 'r': rsa_ins.r, 'k': k_list})
    if(request.form['serviceName'] == 'checkKey'):
        p = int(request.form['p'])
        q = int(request.form['q'])
        rsa_ins = RSA(p, q)
        e = int(request.form['e'])
        d = modInverse(e, rsa_ins.r)
        rsa_ins.check_valid_key(e, d)
        return json.dumps({'status': 'OK', 'd': d, 'check': rsa_ins.check_valid_key(e, d)})
    if(request.form['serviceName'] == 'encrypt'):
        p = int(request.form['p'])
        q = int(request.form['q'])
        rsa_ins = RSA(p, q)
        e = int(request.form['e'])
        d = int(request.form['d'])
        message = request.form['msg']
        encoded_message = rsa_ins.encode_message(message)
        encrypted_message = rsa_ins.encrypt_message(encoded_message, e)
        return json.dumps({'status': 'OK', 'encrypted_message': encrypted_message})
    if(request.form['serviceName'] == 'decrypt'):
        data = request.get_json()
        print(data)
        p = int(request.form['p'])
        q = int(request.form['q'])
        rsa_ins = RSA(p, q)
        e = int(request.form['e'])
        d = int(request.form['d'])
        print(request.form)
        encrypted_msg = request.form.getlist('encrypted_array[]')
        for i in range(0, len(encrypted_msg)):
            encrypted_msg[i] = int(encrypted_msg[i])
        print(encrypted_msg)
        decrypted_message = rsa_ins.decrypt_message(encrypted_msg, d)
        return json.dumps({'status': 'OK', 'decrypted_message': decrypted_message})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')
