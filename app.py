from flask import Flask, render_template, jsonify, request
import budg_model as model
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form
        return render_template('result.html', form_data=form_data)
    else:
        return render_template('index.html')

@app.route('/user/<name>')
def hello(name=None):
    return render_template('hello.html', name='Alex')

@app.route('/yabdga/', methods=['GET', 'POST'])
def yabdga():
    head, results = model.get_all()
    categories = model.get_categories()
    accounts = model.get_accounts()
    body = results
    if request.method == 'POST':
        form_data = request.form.to_dict()
        model.tr_save(int(time.time()), form_data['account_from'], form_data['account_to'],
                    form_data['category'], form_data['amount'], form_data['comment'])
        head, results = model.get_all()
        body = results
        return render_template('yabdga.html', head=head, body=body, categories=categories, accounts=accounts, formdata=form_data)
    else:
        return render_template('yabdga.html', head=head, body=body, categories=categories, accounts=accounts)

@app.route('/delete_transaction', methods=['POST'])
def delete_transaction():
    data = request.json
    button_id = data.get('button_id')
    result = model.tr_delete_by_id(button_id)
    response = {"status": result}
    return jsonify(response)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404