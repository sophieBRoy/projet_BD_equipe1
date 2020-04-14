import mysql.connector

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tomato"
    )

    mycursor = mydb.cursor()

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
                     number VARCHAR(4),
                     street VARCHAR(255),
                     postal_code CHAR(6) NOT NULL,
                     PRIMARY KEY (number, street))''')
    print("created table Adresses")

    mycursor.execute('''CREATE TABLE Users (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     first_name VARCHAR(255) NOT NULL,
                     last_name VARCHAR(255) NOT NULL,
                     age INTEGER NOT NULL,
                     number CHAR(6) NOT NULL,
                     street VARCHAR(250) NOT NULL,
                     FOREIGN KEY(number, street) REFERENCES Adresses(number, street)
                     ON UPDATE CASCADE
                     ON DELETE RESTRICT)''')
    print("created table Users")

    mycursor.execute('''CREATE TABLE Authors (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     first_name VARCHAR(255) NOT NULL,
                     last_name VARCHAR(255) NOT NULL,
                     image_id VARCHAR(255) UNIQUE,
                     nationality VARCHAR(255) NOT NULL,
                     birth DATE NOT NULL,
                     death DATE)''')
    print("created table Authors")

    mycursor.execute('''CREATE TABLE Texts (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(255) NOT NULL,
                     image_id VARCHAR(255) UNIQUE,
                     description VARCHAR(500),
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

    #someone needs to be at least 10 to rent a book
    mycursor.execute('''CREATE TRIGGER ageLimits
                        BEFORE INSERT ON Users
                        FOR EACH ROW
                        BEGIN
                            IF (NEW.age) < 10
                            THEN
                                SIGNAL SQLSTATE '45000'
                                SET MESSAGE_TEXT = 'Vous êtes trop jeune pour utiliser nos services';
                            ELSEIF (NEW.age) > 117
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


