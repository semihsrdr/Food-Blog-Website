from flask import Flask,render_template,request,flash
import requests,datetime,os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from database import db,FoodPost,User,Comment
from forms import PostForm,CommentForm
from functions import send_mail
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_gravatar import Gravatar


year=datetime.datetime.now().year

app=Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///posts.db")
login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User,user_id)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def main_page():
    return render_template("index.html",year=year)

@app.route("/recipe/<int:index>",methods=["POST","GET"])
def go_post(index):

    requested_data=db.session.execute(db.select(FoodPost).where(FoodPost.id==index)).scalar()
    users=db.session.execute(db.select(User)).scalar()
    comments=db.session.execute(db.select(Comment).where(Comment.post_id==index)).scalars()
    id=requested_data.author_id
    form=CommentForm()
    if form.validate_on_submit():
        comment=Comment(author_id=current_user.id,
                        post_id=index,
                        text=str(form.comment.data))
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('go_post',index=index))
    return render_template("food-detail.html",food=requested_data,
                           year=year,id=id,
                           users=users,form=form,
                           comments=comments)

@app.route("/recipes")
def blog_page():
    result=db.session.execute(db.select(FoodPost).order_by(FoodPost.title))
    food_data=result.scalars().all()
    return render_template("blog.html",food_data=food_data,year=year)

@app.route("/add_post",methods=["POST","GET"])
def add_post():
    date=datetime.date.today()
    form=PostForm()
    if form.validate_on_submit():
        new_post=FoodPost(title=form.title.data,
                          subtitle=form.subtitle.data,
                          body=form.body.data,
                          date=str(date),
                          img_url=str(form.img_url.data),
                          author_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog_page'))
    return render_template("add_page.html",form=form,date=date)

@app.route("/edit_post/<int:index>",methods=["POST","GET"])
@login_required
def edit_post(index):
    post=db.get_or_404(FoodPost,index)
    date=datetime.date.today()
    form=PostForm(title=post.title,
                  subtitle=post.subtitle,
                  img_url=post.img_url,
                  author=post.author,
                  body=post.body
                 )
    if form.validate_on_submit():
        post.title=form.title.data
        post.subtitle=form.subtitle.data
        post.body=form.body.data
        post.date=str(date)
        post.img_url=str(form.img_url.data)
        post.author=post.author
        db.session.commit()
        return redirect(url_for('blog_page'))
    return render_template("add_page.html",form=form,date=date)

@app.route("/delete/<int:index>")
@login_required
def delete_post(index):
    deleted_post=db.session.execute(db.select(FoodPost).where(FoodPost.id==index)).scalar()
    db.session.delete(deleted_post)
    db.session.commit()
    return redirect(url_for("blog_page"))

@app.route("/contact",methods=["POST","GET"])
def contact_page():
    if request.method=='POST':
        user_address=request.form["email"]
        msg=request.form["comments"]
        name=request.form["firstName"]
        surname=request.form["lastName"]
        send_mail(user_address,msg,name,surname)

        return render_template("contact.html",year=year)
    return render_template("contact.html",year=year)

@app.route("/faqs")
def faqs():
    return render_template("faqs.html",year=year)

@app.route("/about")
def about_page():
    return render_template("about.html",year=year)

@app.route("/sign_in",methods=["POST","GET"])
def sign_in():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        result=db.session.execute(db.select(User).where(User.email==email)).scalar()
        if result:
            if check_password_hash(result.password,password):
                login_user(result)
                return redirect(url_for('blog_page'))
            else:
                flash("Email or Password is Wrong. Please Try Again!")
        else:
            flash("Email or Password is Wrong. Please Try Again!")
            return redirect(url_for('sign_in'))
    return render_template("login.html",year=year)

@app.route("/sign_up",methods=["POST","GET"])
def sign_up():
    if request.method == 'POST':
        password=request.form["password"]
        name=request.form["name"]
        mail=request.form["email"]
        result=db.session.execute(db.select(User).where(User.email==mail)).scalar()
        if request.form["password"] == request.form["password2"]:
            if not result:
                hashed_password=generate_password_hash(password,method="scrypt",salt_length=16)
                new_user=User(
                    name=name.title(),
                    email=mail,
                    password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('blog_page'))
            else:
                flash("This email already exist. Please try to login!")
        else:
            flash("Passwords are not matching. Please try again!")
            return redirect(url_for('sign_up'))
    return render_template("sign-up.html",year=year)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_page"))
if __name__=="__main__":
    app.run(debug=False)



