from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    """ログイン画面のフォームクラス

    Attributes:
        email: メールアドレス
        password: パスワード
        submit: 送信ボタン
    """
    email = StringField(
        "メールアドレス",
        validators=[DataRequired(message="メールアドレスの入力が必要です。"),
                    Email(message="メールアドレスの形式で入力してください。"),]
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired(message="パスワードの入力が必要です。"),]
    )
    # フォームのsubmitボタン
    submit = SubmitField(("ログイン"))
