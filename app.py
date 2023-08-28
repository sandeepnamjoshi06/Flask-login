from flask import Flask,render_template,redirect,request,session
import mysql.connector
import os
app=Flask(__name__)
app.secret_key=os.urandom(24)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="customer"
)
mycursor = mydb.cursor()
@app.route("/", methods=["GET","POST"])
def home():
    email=request.form.get("email")
    password=request.form.get("password")
    sql = "SELECT * FROM cus_info where email like %s and passwordHash like %s"
    data=(email,password)
    mycursor.execute(sql,data)
    user=mycursor.fetchall()
    if len(user)>0:
        session["user_id"]=user[0][0]

        return redirect('/dashbord')
    else:
        flash("invalid")
        return render_template("Home.html")
   
@app.route("/Register",methods=["GET","POST"])
def Register():
    user_name=request.form.get("user_name")
    email=request.form.get("uemail")
    password=request.form.get("upassword")
    sql = "INSERT INTO cus_info(id,user_name,email,passwordHash) VALUES(Null,%s,%s,%s)"
    data=(user_name,email,password)
    mycursor.execute(sql,data)
    mydb.commit()
    return render_template("Register.html")

@app.route("/dashbord")
def deshbord():
    if "user_id" in session:
        return render_template("dash.html")
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session.pop("user_id")
    return redirect("/")



if __name__=="__main__":
    app.run(debug=True)


