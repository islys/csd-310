# Ryan Monnier
# CSD310 
# Module 7 Assignment
# 16-Feb-2025

""" import statements """
# Added import os so I can have my .env file in a root directory and access it now and for future assignments
import os
import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values

# Function to display Film and its info in accordance with instructions
def show_films(cursor, title):
    cursor.execute("select film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name' from film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id")
    films = cursor.fetchall()
    print("\n  -- {}  --".format(title))
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}".format(film[0], film[1], film[2],film[3]))
        print("")



# .env is in csd-310 folder; this gets absolute path to .env
parent_dir = "\\".join(os.path.realpath(__file__).split("\\")[:-2])

#using our .env file
secrets = dotenv_values(parent_dir + "\\.env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

try:
    """ try/catch block for handling potential MySQL database errors """ 

    movies = mysql.connector.connect(**config) # connect to the movies database 
    cursor = movies.cursor()

    # output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"])+"\n")

    # Show the original list of films
    show_films(cursor, "DISPLAYING FILMS")

    # Add my own movie into the database (Shaun of the Dead)
    cursor.execute("INSERT INTO film (film_id, film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) VALUES (4, 'Shaun of the Dead', '2004', 99, 'Edgar Wright', 3, 1)")

    # Display films after I added my own
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # Update the Genre on Alien
    cursor.execute("UPDATE film SET genre_id = 1 WHERE film_name='Alien'")    

    # Display films after I updated Alien to Horror
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")

    # Delete Gladiator
    cursor.execute("DELETE FROM film where film_name = 'Gladiator'")    

    # Display films after Delete Gladiator
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")


    input("\n\n  Press any key, as long as that key is <ENTER> to continue...")

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """

    movies.close()

    