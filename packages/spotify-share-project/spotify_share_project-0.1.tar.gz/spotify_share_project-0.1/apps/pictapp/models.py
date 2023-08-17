from datetime import datetime
# app.pyのdbオブジェクト
from apps.app import db

class UserPicture(db.Model):
    """picturesテーブルのモデルクラス
    db.Modelを継承

    """
    # テーブル名を「pictures」にする
    __tablename__ = "pictures"
    
    # 連番を振るフィールド、プライマリーキー
    id = db.Column(
		db.Integer,         # Integer型
        primary_key=True,   # プライマリーキーに設定
        autoincrement=True) # 自動連番を振る
    
    # user_idはusersテーブルのidカラムを外部キーとして設定
    user_id = db.Column(
        db.String,          # String型
        db.ForeignKey('users.id'))
    
    # ユーザー名用のフィールド
    username = db.Column(
        db.String,         # String型
        index=True)        # インデックス

    # タイトル用のフィールド
    title = db.Column(
        db.String)          # String型
    
    # 本文用のフィールド
    contents = db.Column(
        db.Text)            # Text型
    
    url = db.Column(
        db.Text
    )
    
    # 作成日時のフィールド
    create_at = db.Column(
        db.DateTime,          # DatTime型
        default=datetime.now) # アップロード時の日時を取得
    
