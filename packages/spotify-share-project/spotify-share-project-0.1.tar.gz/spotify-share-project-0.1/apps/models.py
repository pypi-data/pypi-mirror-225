from datetime import datetime
# werkzeug.securityからパスワード関連の関数をインポート
from werkzeug.security import generate_password_hash, check_password_hash
# flask_loginからUserMixinクラスをインポート
from flask_login import UserMixin
# app.pyのdbオブジェクト、login_managerオブジェクト
from apps.app import db, login_manager

class User(db.Model, UserMixin):
    """モデルクラス
    db.ModelとUserMixinを継承

    """
    # テーブル名を「users」にする
    __tablename__ = "users"

    # 自動的に連番を振るフィールド、プライマリーキー
    id = db.Column(
		db.Integer,         
        primary_key=True,   # プライマリーキーに設定
        autoincrement=True) # 自動連番を振る
    
    # ユーザー名用のフィールド
    username = db.Column(
        db.String(30),     # String型(最大文字数30)
        index=True,        # インデックス
        nullable=False)    # 登録を必須にする
    
    # メールアドレス用のフィールド
    email = db.Column(
        db.String,         # String型
        index=True,        # インデックス
        unique=True,       # ユニークキー
        nullable=False)    # 登録を必須にする
    
    # パスワード用のフィールド
    password_hash = db.Column(
        db.String,         # String型
        nullable=False)    # 登録を必須にする
    
    # 投稿日のフィールド
    create_at = db.Column(
        db.DateTime,          # DatTime型
        default=datetime.now) # 登録時の日時を取得
    
    @property
    def password(self):
        """passwordプロパティの定義

        Raises:
            AttributeError: 読み取り不可
        """
        # プロパティが直接参照された場合はAttributeErrorを発生させる
        raise AttributeError('password is not a readable')
    
    @password.setter
    def password(self, password):
        """passwordプロパティのセッター
        
        トップページのビューにおいてフォームに入力されたパスワードを
        passwordプロパティにセットするときに呼ばれる
        """
        # ハッシュ化したパスワードをpassword_hashフィールドに格納
        self.password_hash = generate_password_hash(password)
    
    def is_duplicate_email(self):
        """ユーザー登録時におけるメールアドレスの重複チェックを行う
        """
        # データベースのemailカラムからサインアップフォームで入力された
        # メールアドレスのレコードを取得
        # 該当するレコードが取得された場合はTrueを返し、
        # 取得できない場合はFalseを返す
        return User.query.filter_by(
            email=self.email).first() is not None

    def verify_password(self, password):
        """パスワードの照合を行う

        indexビューでログインチェックする際に呼ばれる

        Args:
            password (str): ログイン画面で入力されたパスワード

        Returns:
            bool: パスワードが一致した場合はTrueを返す
        """
        # パラメーターpasswordの値をハッシュ化して
        # 現在のインスタンスのpassword_hashと照合した結果を返す
        return check_password_hash(self.password_hash, password)

# user_loaderはセッションに保存されているユーザーID 
# からユーザーオブジェクトを再読み込みする際に呼ばれる
# コールバックを設定する
@login_manager.user_loader
def load_user(user_id):
    """ユーザーオブジェクトを再読み込みする際にコールバックされる

    Args:
        user_id (str): ユーザーid

    Returns:
        object: 対象のユーザーのレコード
    """
    # usersテーブルから指定されたuser_idのレコードを抽出
    return db.session.get(User, user_id)