from flask import Blueprint

""" 識別名をauthappにしてBlueprintオブジェクトを生成

    テンプレートフォルダーは'templates_auth'
    staticフォルダーは'static_auth'
"""
authapp = Blueprint(
    'authapp',
    __name__,
    template_folder='templates_auth',
    static_folder='static_auth',
    )

"""authappのログインページのルーティングとビューの定義

    ユーザー認証を行う
"""
from flask import render_template, url_for, redirect, flash
from flask_login import login_user
from sqlalchemy import select
from apps.authapp import forms # authapp/forms.py
from apps import models # apps/models.py
from apps.app import db # apps/blogapp.pyからdbをインポート

@authapp.route('/', methods=['GET', 'POST'])
def index():
    # LoginFormをインスタンス化
    form = forms.LoginForm()
    # ログインフォームのsubmitボタンが押されたときの処理
    if form.validate_on_submit():
        # データベースのusersテーブルからemailカラムで
        # form.email.dataと一致するレコードを取得(1件)する
        stmt = (
            select(models.User).filter_by(email=form.email.data).limit(1)
        )
        # データベースにクエリを発行して結果を取得する
        user = db.session.execute(stmt).scalars().first()

        # ユーザーが存在し、パスワードが一致する場合はログインを許可
        # パスワードの照合はUserクラスのverify_password()で行う
        if user is not None and user.verify_password(form.password.data):
            # ユーザー情報をセッションに格納
            login_user(user)
            # pictappのトップページにリダイレクト
            return redirect(url_for('pictapp.index'))
        # ログインチェックがfaseの場合はメッセージを表示
        flash("認証に失敗しました")
    # ログイン画面へのアクセスはlogin.htmlをレンダリングして
    # LoginFormのインスタンスformを引き渡す
    return render_template('login.html', form=form)

