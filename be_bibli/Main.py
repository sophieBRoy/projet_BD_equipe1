import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tomato",
    database="library"
)

mycursor = mydb.cursor()


def research(query, book, magazine):
    result = []
    if book == 1:
        command = "SELECT b.id, b.name, b.genre, b.image_id FROM books b WHERE b.name like '%" + query + "%'"
        mycursor.execute(command)
        result += mycursor.fetchall()
    if magazine == 1:
        command = "SELECT m.id, m.name, m.genre, m.image_id FROM magazines m WHERE m.name like '%" + query + "%'"
        mycursor.execute(command)
        result += mycursor.fetchall()
    return result

def getBook(id):
    command = "SELECT * FROM Books b WHERE b.id ='" + str(id) + "'"
    mycursor.execute(command)
    result = mycursor.fetchall()
    return result

def getMagazine(id):
    command = "SELECT * FROM Magazines m WHERE m.id ='" + str(id) + "'"
    mycursor.execute(command)
    result = mycursor.fetchall()
    return result


if __name__ == '__main__':
    # INITIALISATION OF TABLES (FIRST METHOD)
    # after running this code for the first time, uncomment this line:
    mycursor.execute("DROP DATABASE Library")

    # create the database
    mycursor.execute("CREATE DATABASE Library")
    print("created Database Library!")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tomato",
        database="library"
    )

    mycursor = mydb.cursor()

    # create the table for the adresses
    mycursor.execute('''CREATE TABLE Adresses (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     number VARCHAR(4),
                     street VARCHAR(255),
                     postal_code CHAR(6) NOT NULL)''')
    print("created table Adresses")
    # missing email and password in the datas
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
                     name VARCHAR(50) PRIMARY KEY,
                     image_id CHAR(3) UNIQUE,
                     birth DATE NOT NULL,
                     death DATE,
                     nationality VARCHAR(255) NOT NULL)''')
    print("created table Authors")

    mycursor.execute('''CREATE TABLE Books (
                     id VARCHAR(10) PRIMARY KEY,
                     publishing_date DATE NOT NULL,
                     author_name VARCHAR(50) NOT NULL,
                     name VARCHAR(255) NOT NULL,
                     image_id VARCHAR(255),
                     genre VARCHAR(50) NOT NULL,
                     FOREIGN KEY(author_name) REFERENCES Authors(name)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE)''')
    print("created table Books")

    mycursor.execute('''CREATE TABLE Copies (
                     id INTEGER AUTO_INCREMENT PRIMARY KEY,
                     b_id VARCHAR(10) NOT NULL,
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

    mycursor.execute('''CREATE TABLE Magazines (
                     id VARCHAR(10) PRIMARY KEY,
                     name VARCHAR(255) NOT NULL,
                     image_id VARCHAR(255),
                     genre VARCHAR(50) NOT NULL,
                     number INTEGER NOT NULL,
                     month VARCHAR(10) NOT NULL,
                     year INTEGER NOT NULL,
                     quantity INTEGER NOT NULL)''')
    print("created table Magazines")
    # TRIGGERS (SECOND METHOD)
    # someone needs to be at least 10 to rent a book and cant be older than 117 years old
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

    # FILLING DATABASE (THIRD METHOD)

    # fills adresses
    # use this method to read a file that has columns delimited by ; and rows delimited by a new line
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/adresses.txt" INTO TABLE adresses
        COLUMNS TERMINATED BY ";"
       LINES TERMINATED BY "\r\n" ''')
    print("Filled Adresses")

    # fills users
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/users.txt" INTO TABLE users
        COLUMNS TERMINATED BY ";"
       LINES TERMINATED BY "\r\n" ''')
    print("Filled Users")

    # fills authors
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/authors.txt" INTO TABLE authors
            COLUMNS TERMINATED BY ";"
           LINES TERMINATED BY "\r\n" ''')
    print("Filled Authors")

    # fills books
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/books.txt" INTO TABLE books
            COLUMNS TERMINATED BY ";"
           LINES TERMINATED BY "\r\n" ''')
    print("Filled Books")

    #fill magazines
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/magazines.txt" INTO TABLE magazines
            COLUMNS TERMINATED BY ";"
           LINES TERMINATED BY "\r\n" ''')
    print("Filled Magazines")

    mydb.commit()
    mycursor.close()
    mydb.close()
