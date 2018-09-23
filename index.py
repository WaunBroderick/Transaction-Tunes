from flask import Flask
from flask import Flask, render_template

app = Flask(__name__, template_folder='template')

@app.route("/")
def home():
    return render_template('./home.html')

def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            pass # do something
        elif request.form['submit_button'] == 'Do Something Else':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)