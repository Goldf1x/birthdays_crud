import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session


DB_NAME = "birthdays.db"

# Конфигурация приложения
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    # Избавляемся от кеширования 
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Подключаем бд
        db = sqlite3.connect(DB_NAME)
        db.row_factory = sqlite3.Row # Чтобы данные возвращались в виде словарей

        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", (name, int(month),  int(day)))
        db.commit()
        db.close()

        return redirect("/")

    else:
        return render_template("index.html")
        

@app.route("/api/bdays", methods=["GET"])
def get_bdays_data():

    # Подключаем бд
    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row # Чтобы данные возвращались в виде словарей

    # Возвращает объект sqlite3.Row который нужно потом преобразовать в словарь потому что jsonify сам не может
    rows =  db.execute("SELECT * FROM birthdays").fetchall() 
    bdays_data = [dict(row) for row in rows]
    db.close()

    return jsonify(bdays_data)
