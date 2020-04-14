import mysql.connector

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tomato"
    )

    mycursor = mydb.cursor()

    #after running this code for the first time, uncomment this line:
    #mycursor.execute("DROP DATABASE Library")

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
                     number VARCHAR(4),
                     street VARCHAR(255),
                     postalCode CHAR(6) NOT NULL,
                     PRIMARY KEY (number, street))''')
    print("created table Adresses")

    mycursor.execute('''CREATE TABLE Users (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     firstName VARCHAR(255) NOT NULL,
                     lastName VARCHAR(255) NOT NULL,
                     age INTEGER NOT NULL,
                     number CHAR(6) NOT NULL,
                     street VARCHAR(250) NOT NULL,
                     FOREIGN KEY(number, street) REFERENCES Adresses(number, street)
                     ON UPDATE CASCADE
                     ON DELETE RESTRICT)''')
    print("created table Users")

    mycursor.execute('''CREATE TABLE Authors (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     firstName VARCHAR(255) NOT NULL,
                     lastName VARCHAR(255) NOT NULL,
                     imageId VARCHAR(255),
                     nationality VARCHAR(255) NOT NULL,
                     birth DATE NOT NULL,
                     death DATE)''')
    print("created table Authors")

    mycursor.execute('''CREATE TABLE Texts (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(255) NOT NULL,
                     imageId VARCHAR(255),
                     description VARCHAR(500),
                     type VARCHAR(50) NOT NULL)''')
    print("created table Texts")

    mycursor.execute('''CREATE TABLE Books (
                     id INTEGER PRIMARY KEY,
                     publishingDate DATE NOT NULL,
                     aId INTEGER NOT NULL,
                     FOREIGN KEY(aId) REFERENCES Authors(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE,
                     FOREIGN KEY(id) REFERENCES Texts(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE)''')
    print("created table Books")

    mycursor.execute('''CREATE TABLE Copies (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     bId INTEGER NOT NULL,
                     status BOOL NOT NULL,
                     FOREIGN KEY(bId) REFERENCES Books(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE)''')
    print("created table Copies")

    mycursor.execute('''CREATE TABLE Locations (
                     uId INTEGER NOT NULL,
                     cId INTEGER NOT NULL,
                     FOREIGN KEY(uId) REFERENCES Users(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE,
                     FOREIGN KEY(cId) REFERENCES Copies(id)
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


