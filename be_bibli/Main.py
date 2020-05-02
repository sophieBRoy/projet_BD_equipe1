import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tomato",
    database="library"
)

mycursor = mydb.cursor()

def research(query):
    command="SELECT t.name, t.type, t.image_id FROM texts t WHERE t.name like '%" + query + "%'"
    mycursor.execute(command)
    result = mycursor.fetchall()
    return result


if __name__ == '__main__':

    #INITIALISATION OF TABLES (FIRST METHOD)
    #after running this code for the first time, uncomment this line:
    mycursor.execute("DROP DATABASE Library")

    #create the database
    mycursor.execute("CREATE DATABASE Library")
    print("created Database Library!")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tomato",
        database="library"
    )

    mycursor = mydb.cursor()

    #create the table for the adresses
    mycursor.execute('''CREATE TABLE Adresses (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     number VARCHAR(4),
                     street VARCHAR(255),
                     postal_code CHAR(6) NOT NULL)''')
    print("created table Adresses")
#missing email and password in the datas
    mycursor.execute('''CREATE TABLE Users (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     first_name VARCHAR(255) NOT NULL,
                     last_name VARCHAR(255) NOT NULL,
                     age INTEGER NOT NULL,
                     adress_id INTEGER NOT NULL,
                     email VARCHAR(255) NOT NULL, 
                     password VARCHAR(20) NOT NULL,
                     admin BOOL NOT NULL,
                     FOREIGN KEY(adress_id) REFERENCES Adresses(id)
                     ON UPDATE CASCADE
                     ON DELETE RESTRICT)''')
    print("created table Users")

    mycursor.execute('''CREATE TABLE Authors (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     first_name VARCHAR(255) NOT NULL,
                     last_name VARCHAR(255) NOT NULL,
                     image_id CHAR(3) UNIQUE,
                     birth DATE NOT NULL,
                     death DATE,
                     nationality VARCHAR(255) NOT NULL)''')
    print("created table Authors")

    mycursor.execute('''CREATE TABLE Texts (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(255) NOT NULL,
                     image_id VARCHAR(255),
                     type VARCHAR(50) NOT NULL)''')
    print("created table Texts")

    mycursor.execute('''CREATE TABLE Books (
                     id INTEGER PRIMARY KEY,
                     publishing_date DATE NOT NULL,
                     a_id INTEGER NOT NULL,
                     FOREIGN KEY(a_id) REFERENCES Authors(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE,
                     FOREIGN KEY(id) REFERENCES Texts(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE)''')
    print("created table Books")

    mycursor.execute('''CREATE TABLE Copies (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     b_id INTEGER NOT NULL,
                     status BOOL NOT NULL,
                     FOREIGN KEY(b_id) REFERENCES Books(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE)''')
    print("created table Copies")

    mycursor.execute('''CREATE TABLE Locations (
                     u_id INTEGER NOT NULL,
                     c_id INTEGER NOT NULL,
                     FOREIGN KEY(u_id) REFERENCES Users(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE,
                     FOREIGN KEY(c_id) REFERENCES Copies(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE)
                     ''')
    print("created table Locations")

    mycursor.execute('''CREATE TABLE Magasines (
                     id INTEGER PRIMARY KEY,
                     number INTEGER NOT NULL,
                     month VARCHAR(10) NOT NULL,
                     year INTEGER NOT NULL,
                     quantity INTEGER NOT NULL,
                     FOREIGN KEY(id) REFERENCES Texts(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE)''')
    print("created table Magasines")
    #TRIGGERS (SECOND METHOD)
    #someone needs to be at least 10 to rent a book and cant be older than 117 years old
    mycursor.execute('''CREATE TRIGGER ageLimits
                        BEFORE INSERT ON Users
                        FOR EACH ROW
                        BEGIN
                            IF (NEW.age) < 10
                            THEN
                                SIGNAL SQLSTATE '45000'
                                SET MESSAGE_TEXT = NEW.age;
                            ELSEIF (NEW.age) > 117000
                            THEN
                                SIGNAL SQLSTATE '45000'
                                SET MESSAGE_TEXT = 'Vous êtes trop vieux pour utiliser nos services';
                           END IF;
                        END''')

    mycursor.execute('''CREATE TRIGGER maxLivre
                    BEFORE INSERT ON Locations
                    FOR EACH ROW
                        BEGIN
                            IF (SELECT COUNT(*)
                                FROM Locations
                                WHERE u_id = NEW.u_id) = 8
                            THEN
                                SIGNAL SQLSTATE '45000'
                                SET MESSAGE_TEXT = 'Vous ne pouvez pas emprunter plus de 8 livres';
                       END IF;
                    END''')


    #FILLING DATABASE (THIRD METHOD)

    #fills adresses
    #use this method to read a file that has columns delimited by ; and rows delimited by a new line
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/adresses.txt" INTO TABLE adresses
        COLUMNS TERMINATED BY ";"
       LINES TERMINATED BY "\r\n" ''')
    print("Filled Adresses")

    #fills users
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/users.txt" INTO TABLE users
        COLUMNS TERMINATED BY ";"
       LINES TERMINATED BY "\r\n" ''')
    print("Filled Users")

    # fills authors
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/authors.txt" INTO TABLE authors
            COLUMNS TERMINATED BY ";"
           LINES TERMINATED BY "\r\n" ''')
    print("Filled Authors")

    # fills texts
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/texts.txt" INTO TABLE texts
            COLUMNS TERMINATED BY ";"
           LINES TERMINATED BY "\r\n" ''')
    print("Filled Texts")

    mydb.commit()
    mycursor.close()
    mydb.close()
