from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify APIのクライアント情報
SPOTIPY_CLIENT_ID = '9798d4c934df4405bbdf3d5353eb4660'
SPOTIPY_CLIENT_SECRET = '2d2e7805ff004422a2a72c5670561977'

# Spotipyクライアントのセットアップ
sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))


class UploadImageForm(FlaskForm):
    """
    Attributes:
        title: タイトル
        message: メッセージ
        url: spotifyのurl
        submit: 送信ボタン
    """
    title = StringField(
        "タイトル",
        validators=[DataRequired(message="入力が必要です。"),
                    length(max=200, message="200文字以内で入力してください。"),]
    )

    message = TextAreaField(
        "メッセージ",
        validators=[DataRequired(message="入力が必要です。"),])
    
    url = StringField(
        "URL",
        validators=[DataRequired(message="プレイリストのURLを記入してください。"),])
    
    
    # フォームのsubmitボタン
    submit = SubmitField('投稿する')





