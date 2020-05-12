from flask import Flask ,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/kenan/OneDrive/Masaüstü/Todo_App/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    # veritabanı classımıızı (Todo) buraya User in yerine yazıyoruz.
    todos = Todo.query.all()
    #veritabında almış olduğumuz verileri todos adı altında bir sözlük içerisnde toplayıp sonra bunu da index.html e göndermemiz gerekir.
    return render_template("index.html" , todos = todos) 

@app.route("/addURL" , methods=["POST"])
def addURL():
    title = request.form.get("title")
    newtodo = Todo(title=title , complete=False)
    db.session.add(newtodo)
    db.session.commit()
    return redirect(url_for("index"))
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/complete/<string:id>")
def complete(id):
    
    todo_objects = Todo.query.filter_by(id = id).first()

    #Aşağıdaki kod satırıyle aynı görevi yapıyor sadece çok kısa olması tercih edilinilir kılıyor.
    todo_objects.complete = not todo_objects.complete
    #Bu kod satırı yukardaki ile aynı görevi yapıyor if else bölümü.
    """
    if todo_objects.complete == True:
        todo_objects.complete = False
    else:
        todo_objects.complete = True
    """ 
    
    db.session.commit()
    return redirect(url_for("index"))
    
@app.route("/delete/<string:id>")
def delete(id):
    todo_objects = Todo.query.filter_by(id = id).first()
    db.session.delete(todo_objects)
    db.session.commit()
    return redirect(url_for("index"))
    
if __name__== '__main__':
    #Burdaki tüm classlarımı veritabanına bir tablo olarak eklemek için kullanıyoruz.Önceden Oluşturmuş olduğu tabloları tekrardan yine oluşturmaz..
    db.create_all()
    app.run(debug=True)

