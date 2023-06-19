import os
from datetime import datetime
import sqlite3 as sql

# class - contains various methods for interaction with data within database

# creating database.py class DB() object


class DB:
    # constructor
    def __init__(self, **kwargs):
        # creating or connecting to DB
        self.conn = sql.connect("PyFloraPosude.db")
        # creating cursor for DML operation queries
        self.cur = self.conn.cursor()
        # calling function
        self.create_database_structure()

    def create_database_structure(self):
        # create table if it does not exist
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            first_name TEXT,
                            last_name TEXT,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL)"""
        )
        # check if there is user that already exists
        self.cur.execute("SELECT * FROM Users")
        # if not
        if not self.cur.fetchall():
            # add admin user
            self.cur.execute(
                "INSERT INTO Users VALUES (Null, '', '', 'admin', 'admin')"
            )
            # commit database
            self.conn.commit()
        # create table PyFloraPosuda which will hold all the PyFloraPosuda data
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS PyFloraPosude (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_date DATE NOT NULL, 
                    PyFloraPosuda_Name TEXT NOT NULL,
                    plant_planted TEXT NOT NULL,
                    plant_name TEXT,
                    watering TEXT,
                    place TEXT,
                    moisture_soil_sensor TEXT,
                    ph_sensor TEXT,
                    light_sensor TEXT,
                    photo TEXT)"""
        )
        # check if PyFloraPosuda already exist
        self.cur.execute("SELECT * FROM PyFloraPosude")
        # if not
        if not self.cur.fetchall():
            # get current date
            date = datetime.now()
            # change format of date
            date = date.strftime(f"%d-%m-%Y %H:%M:%S")
            # image
            path = os.getcwd() + "/plant_image/rose.jpeg"

            self.cur.execute(
                "INSERT INTO PyFloraPosude VALUES (Null, ?, 'Bedroom', 'Yes', 'Rose',"
                " 'day', 'lighter & colder', 'Active', 'Active', 'Active', ? )",
                (date, path),
            )

            # commit database
            self.conn.commit()
        print("Database Connected...")

    # fetch user by giving the username
    def get_user(self, username):
        # select query
        self.cur.execute("SELECT * FROM Users WHERE username=?", (username,))
        # get result
        res = self.cur.fetchall()

        if res:
            # return result if there is any
            return res[0]
        else:
            # else return none
            return None

    # get Pypot info function
    def get_Pypot(self):
        # select query
        self.cur.execute("SELECT * FROM PyFloraPosude")
        # get data from DB
        res = self.cur.fetchall()
        # return result
        return res

    # dml queries like insert/update/delete
    def dml_queries(self, operation, details, id):
        try:
            # if updating
            if operation == "update":
                # update query
                self.cur.execute(
                    "UPDATE PyFloraPosude SET PyFloraPosuda_Name=?, plant_planted =?, plant_name=?,"
                    " watering=?, place=?, moisture_soil_sensor=?, ph_sensor=?, light_sensor=?,"
                    " photo=? where id=?",
                    (
                        details[1],
                        details[2],
                        details[3],
                        details[4],
                        details[5],
                        details[6],
                        details[7],
                        details[8],
                        details[9],
                        id,
                    ),
                )
                msg = "Data Updated successfully"
                # if deleting
            elif operation == "delete":
                # delete query
                self.cur.execute("DELETE FROM PyFloraPosude WHERE id=?", (id,))
                msg = "Data Deleted successfully"
            else:
                # if inserting insert query
                self.cur.execute(
                    "INSERT INTO PyFloraPosude VALUES (Null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        details[0],
                        details[1],
                        details[2],
                        details[3],
                        details[4],
                        details[5],
                        details[6],
                        details[7],
                        details[8],
                        details[9],
                    ),
                )
                msg = "Data Inserted successfully"
            # save DB
            self.conn.commit()
            return msg
        except Exception as e:
            return str(e)

    # update profile function
    def update_profile(self, data):
        try:
            # update query
            self.cur.execute(
                "UPDATE Users SET first_name=?, last_name=?, username=?, password=? where id=?",
                (data[0], data[1], data[2], data[3], data[4]),
            )
            # save DB
            self.conn.commit()
            msg = "Profile Updated successfully"
        except Exception as e:
            msg = str(e)
        return msg

    def insert_profile(self, data):
        try:
            # update query
            self.cur.execute(
                "INSERT INTO Users VALUES ( Null, ?, ?, ?, ?)",
                (data[0], data[1], data[2], data[3]),
            )
            # save DB
            self.conn.commit()
            msg = "User Register successfully"
        except Exception as e:
            msg = str(e)
        return msg
