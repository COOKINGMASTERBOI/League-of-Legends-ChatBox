from flask_login import LoginManager
from config import Config
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

app = Flask(__name__)
# 添加配置信息

login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)

# 建立数据库关系
db = SQLAlchemy(app)
# 绑定app和数据库，以便进行操作
migrate = Migrate(app, db)

from app import routes