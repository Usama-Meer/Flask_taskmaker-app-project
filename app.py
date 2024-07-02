from flask import Flask,redirect,render_template,app,request,url_for
from traitlets import default
from wtforms import Form
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#initailize app
app=Flask(__name__)

#location of db
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'

#initilaize db
db=SQLAlchemy(app)

#creating a class for the table of the database
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    content=db.Column(db.String(200))
    completed=db.Column(db.Integer,default=0)

    # date_created=db.Column(db.DateTime,default=datetime.now(utc))
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %>'%self.id
    
#pages
    
@app.route('/',methods=['POST','GET'])
def index():
    #check whether request is post or get
    if request.method=='POST':
        #get data from the form into task_content variable
        task_content=request.form['content']
        
        #value is added to content attribute of Todo
        new_content=Todo(content=task_content)

      

        try:
            #value is added to the database
            db.session.add(new_content)
            #database is updated
            db.session.commit()
            #redirect to the page
            return redirect('/')
        except:
            return "There was an error while adding your task"
        

        
    else:
          #query is made in database to print all data 
        task=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=task)
    






@app.route("/delete/<int:id>")
def delete(id):

    task_to_delete=Todo.query.get_or_404(id)
    
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "There was an error while deleting your task"
    
 


@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    #get content
    task=Todo.query.get_or_404(id)
    if request.method=="POST":

        
        
        #add content to the task
        task.content=request.form['content']

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "there was an error updating your task"

    else:

        return render_template("update.html",task=task)
    


if  __name__=='__main__':
    app.run(debug=True)