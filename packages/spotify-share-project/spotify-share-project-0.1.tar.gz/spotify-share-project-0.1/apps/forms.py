from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, length

class SignupForm(FlaskForm):
    """サインアップ画面のフォームクラス

    Attributes:
        username: ユーザー名
        email: メールアドレス
        password: パスワード
        submit: 送信ボタン
    """
    username = StringField(
        "ユーザー名",
        validators=[DataRequired(message="入力が必要です。"),
                    length(max=30, message="30文字以内で入力してください。"),]
    )
    email = StringField(
        "メールアドレス",
        validators=[DataRequired(message="入力が必要です。"),
                    Email(message="メールアドレスの形式で入力してください。"),]
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired(message="入力が必要です。"),
                    length(min=6, message="6文字以上で入力してください。"),]
    )
    # フォームのsubmitボタン
    submit = SubmitField("新規登録")
