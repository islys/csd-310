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

    # Grab and print Studio Records
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    studio = cursor.fetchall()
    print("-- DISPLAYING Studio RECORDS --")
    for i in studio:
        print("Studio ID: {}\nStudio Name: {}\n".format(i[0], i[1]))
    print("\n")
    # Grab and print Genre Records
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    studio = cursor.fetchall()
    print("-- DISPLAYING Genre RECORDS --")
    for i in studio:
        print("Genre ID: {}\nGenre Name: {}\n".format(i[0], i[1]))
    print("\n")

    # Grab and print Short Film Records, WHERE the runtime is < 120 min
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    studio = cursor.fetchall()
    print("-- DISPLAYING Short Film RECORDS --")
    for i in studio:
        print("Film Name: {}\nRuntime: {}\n".format(i[0], i[1]))
    print("\n")

    # Grab and print Director Records, ordering by film_director
    cursor.execute("SELECT film_director, film_name AS films FROM film ORDER BY film_director")
    # This would be kind of a neat way to put the movies on the same line and sort them in ascending order      
    # cursor.execute("SELECT film_director, GROUP_CONCAT(film_name ORDER BY film_name ASC) AS films FROM film GROUP BY film_director")
    studio = cursor.fetchall()
    print("-- DISPLAYING Director RECORDS in Order --")
    for i in studio:
        print("Film Name: {}\nDirector: {}\n".format(i[0], i[1]))
    print("\n")

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

    