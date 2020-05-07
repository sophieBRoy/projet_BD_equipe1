import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tomato",
    database="library"
)

mycursor = mydb.cursor(buffered=True)


def research(query, book, magazine):
    result = []

    if (book == 0 and magazine == 0) or (book == 1 and magazine == 1):
        mycursor.callproc('getMagsAndBooks', (query,))

        for test in mycursor.stored_results():
            result += (test.fetchall())
    elif book == 1:
        mycursor.callproc('getBooks', (query,))

        for test in mycursor.stored_results():
            result += (test.fetchall())
    else:
        mycursor.callproc('getMagazines', (query,))

        for test in mycursor.stored_results():
            result += (test.fetchall())

    return result


def advancedResearch(title, author, typeList):
    result = []
    types = ["Fantaisie", "Science-fiction", "Polar", "Classique", "Horreur", "BD", "Overrated"]
    command = "SELECT b.id, b.name, b.genre, b.image_id FROM books b WHERE b.name like '%" + title + "%' AND b.author_name like '%" + author + "%'"
    command += "AND b.genre IN ('"

    for x in range(0, 7):
        if typeList[x] == True:
            command += types[x] + "','"
    # si aucune donnée a été sélectionnée on prend tous
    if command[-2:] != ",'":
        for x in range(0, 7):
            command += types[x] + "','"
    command = command[:-2]
    command += ")"
    print(command)
    mycursor.execute(command)
    result = mycursor.fetchall()

    return result


def getBook(id):
    result = []
    mycursor.callproc('getBook', (id,))

    for test in mycursor.stored_results():
        result += (test.fetchall())
    return result


def getMagazine(id):
    result = []
    mycursor.callproc('getMagazine', (id,))

    for test in mycursor.stored_results():
        result += (test.fetchall())
    return result

def getAuthor(authorName):
    result = []
    mycursor.callproc('getAuthor', (authorName,))

    for test in mycursor.stored_results():
        result += (test.fetchall())
    return result


def getBooksFromAuthor(authorName):
    result = []
    mycursor.callproc('getBooksFromAuthor', (authorName,))

    for test in mycursor.stored_results():
        result += (test.fetchall())
    return result

def GetEmail(mail):

    command = ("SELECT u.id FROM Users u WHERE u.email like'%" + mail + "%'")
    mycursor.execute(command)
    result = mycursor.fetchone()
    if result is None:
        result ="Le courriel saisie n'éxiste pas"
        return False, result
    return result
#ne doit pas afficher un message
def GetPassWord(passWord):
    command = ("SELECT u.id FROM Users u WHERE u.password like '%" + passWord + "%'")
    mycursor.execute(command, passWord)
    result = mycursor.fetchone()
    if result is None:
        return False
    return result

def GetUser(mail, passWord):
    result=[]
    # si la saisie est VIDE retourner false /testé
    if mail.isspace() and passWord.isspace():
        return False
    #sinon traiter la saisie
    else:
        #recupérer les donnée des fonctions GetEmail et GetPassWord/TESTÉ
        resultatmail = GetEmail(mail)
        resultatpassword=GetPassWord(passWord)
        #si les deux fonctions retourne False (c est a dire que la saisie ne concorde pas avec une des entrées de la table users) alors on retourne False/TESTÉ
        if not resultatmail[0] or not resultatpassword:
            result = False
        #tester si les deux ID concorde/TESTÉ
        elif resultatpassword[0] != resultatmail[0]:
            result = False
        else:
            #cas ou les deux entrées concorde et récupérer le ID
            command = "SELECT u.id FROM Users u WHERE u.email like %s AND u.password like %s"
            mycursor.execute(command, (mail, passWord))
            result = mycursor.fetchone()
            print(result)

    return result

def getmail(numero, rue, code):
    result5 = []
    mycursor.callproc('SetNewAdresses', (numero, rue, code))
    for test in mycursor.stored_results():
        result5 += (test.fetchall())
        mydb.commit()
    command = ("SELECT u.id FROM Users u WHERE u.email like'%" + mail + "%'")
    mycursor.execute(command)
    result = mycursor.fetchone()
    if result is None:
        result ="Le courriel saisie n'existe pas"
        return False, result
    return result

def SetUtilisateur( nom, prenom, age, numero, rue, code,  email, password):
    commande = " INSERT INTO Adresses(number, street, postal_code) VALUES (%s, %s, %s)"
    mycursor.execute(commande, (numero, rue, code))
    adress_id = mycursor.lastrowid
    mydb.commit()
    commande2 = "INSERT INTO Users(first_name,last_name, age, adress_id, email, password, admin) VALUES (%s, %s, %s,%s,%s,%s,%s)"
    mycursor.execute(commande2, (prenom, nom, age, adress_id, email, password, 0))
    mydb.commit()
    return True

def GetInfoUtilisateur(id):
    result = []
    command = ("SELECT u.id, u.first_name, u.last_name, u.age, u.email, u.admin FROM Users u WHERE u.id like '%" + str(id) + "%'")
    mycursor.execute(command)
    result += mycursor.fetchone()
    return result

def ajoutUtilisateur(nom, prenom, age, mail, password):
    result6 = []
    resultat = []
    command=("SELECT MAX(a.id) FROM Adresses a")
    mycursor.execute(command)
    resultat +=mycursor.fetchone()
    print(resultat)
    mycursor.callproc('SetNewUser', (nom, prenom, age,  mail, password, 0))
    for test in mycursor.stored_results():
        result6 += (test.fetchall())
        mydb.commit()

def addMagToPurchases(userId, magId):
    try:
        mycursor.callproc('addPurchase', (userId, magId))
        mydb.commit()
    except mydb.Error as ex:
        return ex
    return 0

def addBookToLocations(userId, bookId):
    result = []
    mycursor.callproc('selectCopy', (bookId, ))

    for test in mycursor.stored_results():
        result += (test.fetchall())
    copieId= result[0][0]
    if copieId:
        mycursor.callproc('addLocation', (userId, copieId))
        mydb.commit()
    else:
        return "il ne reste plus d'exemplaires de ce livre"

def getUserLocations(userId):
    result=[]
    mycursor.callproc('getUserLocations', (userId,))

    for test in mycursor.stored_results():
        result += (test.fetchall())
    return result

def getUserPurchases(userId):
    result=[]
    mycursor.callproc('getUserPurchases', (userId,))

    for test in mycursor.stored_results():
        result += (test.fetchall())
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
                     postal_code CHAR(7) NOT NULL)''')
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
                     image_id CHAR(3),
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

    mycursor.execute('''CREATE TABLE Purchases (
                    u_id INTEGER NOT NULL,
                    m_id VARCHAR(10) NOT NULL,
                    FOREIGN KEY(u_id) REFERENCES Users(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE,
                     FOREIGN KEY(m_id) REFERENCES Magazines(id)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE)''')
    print("created table Purchases")

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

    mycursor.execute('''CREATE TRIGGER noMoreMagazines
                    BEFORE UPDATE ON Magazines
                    FOR EACH ROW
                        BEGIN
                            IF NEW.quantity < 0
                            THEN
                                SIGNAL SQLSTATE '45000'
                                SET MESSAGE_TEXT = "Il ne reste plus d'exemplaires de ce magazine";
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

    # fills users
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/copies.txt" INTO TABLE copies
        COLUMNS TERMINATED BY ";"
       LINES TERMINATED BY "\r\n" ''')
    print("Filled Users")

    # fill magazines
    mycursor.execute('''LOAD DATA LOCAL INFILE "data/magazines.txt" INTO TABLE magazines
            COLUMNS TERMINATED BY ";"
           LINES TERMINATED BY "\r\n" ''')
    print("Filled Magazines")

    # create getBook function
    mycursor.execute('''CREATE PROCEDURE getMagazines(IN query varchar(64))
            BEGIN
            SELECT m.id, m.name, m.genre, m.image_id FROM Magazines m WHERE m.name like(CONCAT('%', query, '%'));
            END''')

    print("Created getMagazines")

    mycursor.execute('''CREATE PROCEDURE getMagazine(id varchar(64))
                        BEGIN
                        SELECT * FROM Magazines m WHERE m.id = id;
                        END''')
    print("Created getMagazine")

    mycursor.execute('''CREATE PROCEDURE getBooks(query varchar(64))
            BEGIN
            SELECT b.id, b.name, b.genre, b.image_id FROM Books b WHERE b.name like(CONCAT('%', query, '%'));
            END''')

    print("Created getBooks")

    mycursor.execute('''CREATE PROCEDURE getBook(id varchar(64))
                    BEGIN
                    SELECT * FROM Books b WHERE b.id = id;
                    END''')
    print("Created getBook")

    mycursor.execute('''CREATE PROCEDURE getMagsAndBooks(query varchar(64))
                BEGIN
                CALL getBooks(query);
                CALL getMagazines(query);
                END''')

    print("Created getMagsAndBooks")

    mycursor.execute('''CREATE PROCEDURE getUser(email varchar(64), pass varchar(64))
                BEGIN
                SELECT * FROM Users u WHERE u.password = pass AND u.email = email;
                END''')

    print("Created getUser")

    mycursor.execute('''CREATE PROCEDURE getAuthor(authorName varchar(64))
                    BEGIN
                    SELECT a.name, a.birth, a.death, a.nationality, a.image_id FROM Authors a WHERE a.name = authorName;
                    END''')

    print("Created getAuthor")

    mycursor.execute('''CREATE PROCEDURE getBooksFromAuthor(authorName varchar(64))
                        BEGIN
                        SELECT b.id, b.name, b.image_id FROM Books b WHERE b.author_name = authorName;
                        END''')

    print("Created getBooksFromAuthor")

    mycursor.execute('''CREATE PROCEDURE advancedSearch(title varchar(64), author varchar(64), types varchar(64))
                          BEGIN
                          SELECT b.id, b.name, b.genre, b.image_id FROM books b WHERE b.name like 
                          (CONCAT('%', title, '%')) AND b.author_name like (CONCAT('%', author, '%')) AND b.genre IN (types);
                          END''')

    print("Created advancedSearch")

    mycursor.execute('''CREATE PROCEDURE updateQuantity(magId varchar(10), difference integer)
                    BEGIN
                        UPDATE Magazines
                        SET quantity = quantity + difference
                        WHERE id = magId;
                        END''')
    print("Created updateQuantity")

    mycursor.execute('''CREATE PROCEDURE addPurchase(userId integer, magId varchar(10))
                    BEGIN
                    CALL updateQuantity(magId, -1);
                    INSERT INTO Purchases(u_id, m_id)
                    VALUES(userId, magId);
                    END''')
    print("Created addPurchase")

    mycursor.execute('''CREATE PROCEDURE setStatusLocation(bookId varchar(10))
                        BEGIN
                        UPDATE Copies
                        SET status = 0
                        WHERE b_id = bookId AND status = 1
                        LIMIT 1;
                        END''')
    print("Created setStatusLocation")

    mycursor.execute('''CREATE PROCEDURE selectCopy(bookId varchar(10))
                            BEGIN
                            SELECT c.id FROM Copies c
                            WHERE c.b_id = bookId AND status = 1
                            LIMIT 1;
                            CALL setStatusLocation(bookId);
                            END''')
    print("Created selectCopy")

    mycursor.execute('''CREATE PROCEDURE addLocation(userId integer, copieId integer)
                    BEGIN
                    INSERT INTO Locations(u_id, c_id)
                    VALUES(userId, copieId);
                    END''')
    print("Created addLocation")

    mycursor.execute('''CREATE PROCEDURE getUserLocations(userId integer)
                        BEGIN
                        SELECT b.name, c.id FROM Books b, Copies c, Locations l
                        WHERE l.u_id = userId AND l.c_id = c.id AND b.id = c.b_id;
                        END''')
    print("Created getUserLocations")

    mycursor.execute('''CREATE PROCEDURE getUserPurchases(userId integer)
                        BEGIN
                        SELECT m.name FROM Magazines m, Purchases p
                        WHERE p.u_id = userId AND p.m_id = m.id; 
                        END''')
    print("Created getUserPurchases")

    mycursor.execute('''CREATE PROCEDURE SetNewAdresses(nid INTEGER, Nnumber VARCHAR(4), Sstreet VARCHAR(255), Ppostal_code CHAR(6))
                        BEGIN
                        INSERT INTO Adresses (id, number, street, postal_code)
                        VALUES (nid, Nnumber, Sstreet, Ppostal_code);
                        END''')

    mycursor.execute('''CREATE PROCEDURE SetNewUser(Ufirst_name VARCHAR(255),Ulast_name VARCHAR(255),Uage INTEGER , Uemail VARCHAR(255), Upassword VARCHAR(20) ,Uadmin BOOL)
                BEGIN
                INSERT INTO Adresses (first_name,last_name, age, adress_id,email, admin)
                        VALUES (Ufirst_name ,Ulast_name,Uage ,(SELECT MAX(id) FROM Adresses), Uemail , Upassword,Uadmin );
                END''')









    mydb.commit()
    mycursor.close()
    mydb.close()
