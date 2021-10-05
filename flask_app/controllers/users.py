from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User

@app.route('/')
def login():
    return render_template('login.html')