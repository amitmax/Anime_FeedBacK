from flask import Flask,render_template,request
from sqlalchemy import create_engine,text


class DB:
    connection_string = "mysql+mysqlconnector://elt5vab00kzesv73gevl:pscale_pw_bn70vyZSsbfzzKmdP80SrxUc9rtAyvPtdJJrE1eBOjY@aws.connect.psdb.cloud:3306/ani_feedback"
    engine = create_engine(connection_string,)

    connection = engine.connect()

    #connection.execute(text("CREATE TABLE Feedback ( id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(30),age int,gender varchar(7), fav_anime varchar (50),fav_anime_genre varchar (20),feedback varchar (100))"))
    #connection.commit()
    #connection.execute(text("alter table Feedback add email varchar(50)"))

    @classmethod
    def Inse(cls,U_Name,U_Age,U_Gender,U_Fav_Ani,U_Fav_Gen,U_Feedback,U_Email):
        sql_inst = text("Insert into Feedback(name,age,gender,fav_anime,fav_anime_genre,feedback,email) values ('%s', %s,'%s','%s','%s','%s','%s')" %(U_Name,int(U_Age),U_Gender,U_Fav_Ani,U_Fav_Gen,U_Feedback,U_Email))
        cls.connection.execute(sql_inst)
        cls.connection.commit()    
        print("done")
 
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/Input', methods=['POST'] )
def Input():
    if request.method == 'POST':
       
        U_Name = request.form['name']
        U_Email = str(request.form['email'])
        U_Age = request.form['age']
        U_Gender = request.form['gender']
        U_Fav_Ani = request.form['anime']
        U_Fav_Gen = request.form['genre']
        U_Feedback = request.form['feedback']

    # Check if U_Fav_Ani and U_Fav_Gen are blank
    if not U_Fav_Ani.strip() or not U_Fav_Gen.strip() or not U_Name.strip():
        return render_template('index.html', message="Please fill in your favorite anime and genre. and name")
    
    # The fields are not blank, proceed with database insertion
    if DB.Inse(U_Name, U_Age, U_Gender, U_Fav_Ani, U_Fav_Gen, U_Feedback, U_Email):
        return render_template('index.html', message="Please fill details correctly")
    else:
        return render_template('thanks.html')

@app.errorhandler(400)
def bad_request(error):
    return render_template('index.html', message="Please fill details correctly")


if __name__ == "__main__":
    app.run(port=3884)
