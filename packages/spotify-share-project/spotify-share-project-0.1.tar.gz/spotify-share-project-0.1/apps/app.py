"""
初期化処理
"""
from flask import Flask

# Flaskのインスタンスを生成
app = Flask(__name__)
# 設定ファイルを読み込む
app.config.from_pyfile('settings.py')

"""SQLAlchemyの登録
"""
# SQLAlchemyのインスタンスを生成
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# SQLAlchemyオブジェクトにFlaskオブジェクトを登録する
db.init_app(app)

"""Migrateの登録
"""
# Migrateオブジェクトを生成して
# FlaskオブジェクトとSQLAlchemydbを登録する
from flask_migrate import Migrate
Migrate(app, db)

"""LoginManagerの登録
"""
from flask_login import LoginManager

# LoginManagerのインスタンスを生成
login_manager = LoginManager()
# 未ログイン時にリダイレクトするエンドポイントを設定
login_manager.login_view = 'index'
# ログインしたときのメッセージを設定
login_manager.login_message = ''
# LoginManagerをアプリに登録する
login_manager.init_app(app)

"""トップページのルーティング
"""
from flask import render_template, url_for, redirect, flash
from apps import models # apps/models.pyをインポート
from apps import forms  # apps/forms.pyをインポート


@app.route('/', methods=['GET', 'POST'])
def index():
    # SignupFormをインスタンス化
    form = forms.SignupForm()
    # サインアップフォームのsubmitボタンが押されたときの処理
    if form.validate_on_submit():
        # モデルクラスUserのインスタンスを生成
        user = models.User(
            # Userのusernameフィールドに格納
            username=form.username.data,
            # Userのemailフィールドに格納
            email=form.email.data,
            # フォームのpasswordに入力されたデータを取得して
            # Userのpasswordプロパティに格納に格納
            password=form.password.data,
        )
        # メールアドレスの重複チェック
        if user.is_duplicate_email():
            # メールアドレスが既に登録済みの場合は
            # メッセージを表示してエンドポイントindexにリダイレクト
            flash("登録済みのメールアドレスです")
            return redirect(url_for('index'))

        # Userオブジェクトをレコードのデータとして
        # データベースのテーブル(uesr)に追加
        db.session.add(user)
        # データベースを更新
        db.session.commit()
        # 処理完了後、エンドポイントindexにリダイレクト
        return redirect(url_for('index'))
    
    # トップページへのアクセスは、index.htmlをレンダリングして
    # SignupFormのインスタンスformを引き渡す
    return render_template('index.html', form=form)

"""ブループリントauthappの登録
"""
# authappのモジュールviews.pyからBlueprint「authapp」ををインポート
from apps.authapp.views import authapp

# Flaskオブジェクトにブループリント「authapp」を登録
# URLのプレフィクスを/authにする
app.register_blueprint(authapp, url_prefix='/auth')

"""ブループリントpictappの登録
"""
# pictappのモジュールviews.pyからBlueprint「pictapp」ををインポート
from apps.pictapp.views import pictapp

# FlaskオブジェクトにBlueprint「pictapp」を登録
# URLのプレフィクスを/pictureにする
app.register_blueprint(pictapp, url_prefix='/picture')
