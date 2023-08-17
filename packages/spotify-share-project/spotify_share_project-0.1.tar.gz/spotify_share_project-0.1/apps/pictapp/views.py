
""" 識別名をpictappにしてBlueprintオブジェクトを生成
    ・テンプレートフォルダーは同じディレクトリの'templates_pict'
    ・staticフォルダーは同じディレクトリの'static_pict'
"""
from flask import Blueprint, request

pictapp = Blueprint(
    'pictapp',
    __name__,
    template_folder='templates_pict',
    static_folder='static_pict',
    )

"""pictappのトップページのルーティングとビューの定義
"""
from flask import render_template
from flask_login import login_required # login_required
from sqlalchemy import select # sqlalchemy.select()
from flask import request # flask.request
from flask_paginate import Pagination, get_page_parameter

# ログイン必須にする
@pictapp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # 投稿記事のレコードをidの降順で全件取得するクエリ
    stmt = select(
        modelpict.UserPicture).order_by(modelpict.UserPicture.create_at.desc())
    # データベースにクエリを発行
    entries = db.session.execute(stmt).scalars().all()

    # 現在のページ番号を取得
    page = request.args.get(
        get_page_parameter(), type=int, default=1)
    # entriesから現在のページに表示するレコードを抽出
    res = entries[(page - 1)*6: page*6]
    # Paginationオブジェクトを生成
    pagination = Pagination(
        page=page,          # 現在のページ
        total=len(entries), # 全レコード数を取得
        per_page=6)         # 1ページあたりのレコード数

    # top.htmlをレンダリングする際に
    # user_pictsでレコードデータres
    # paginationでPaginationオブジェクトを引き渡す
    return render_template('top.html', user_picts=res, pagination=pagination)

"""imagesフォルダー内の画像ファイルのパスを返す機能
"""
from flask import send_from_directory # send_from_directory

"""ログアウトのルーティングとビューの定義
"""
from flask_login import logout_user
from flask import render_template, url_for, redirect

@pictapp.route('/logout')
@login_required
def logout():
    # flask_loginのlogout_user()関数でログイン中のユーザーを
    # ログアウトさせる
    logout_user()
    # ログイン画面のindexビューにリダイレクト
    return redirect(url_for('authapp.index'))

"""画像アップロードページのルーティングとビューの定義
"""
import uuid # uuid
from pathlib import Path # pathlibのPath
from flask_login import current_user # current_user
from flask import current_app # current_app

from apps.app import db # apps.pyのSQLAlchemyインスタンスapp
from apps.pictapp import forms # pictapp.formsモジュール
from apps.pictapp import models as modelpict # pictapp.modelsモジュール

@pictapp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # UploadImageFormをインスタンス化
    form = forms.UploadImageForm()
    # アップロードフォームのsubmitボタンが押されたときの処理
    if form.validate_on_submit():
        # UserPictureをインスタンス化してフォームのデータを格納
        upload_data = modelpict.UserPicture(
            # user_idに現在ログイン中のユーザーのidを格納
            user_id=current_user.id,
            # usernameに現在ログイン中のユーザー名を格納
            username = current_user.username,
            # titleにフォームのtitleの入力データを格納
            title=form.title.data,
            # contentsにフォームのmessageの入力データを格納
            contents=form.message.data,
            #urlの情報を入力
            url=form.url.data,
        )
        # UserPictureオブジェクトをレコードのデータとして
        # データベースのテーブルに追加
        db.session.add(upload_data)
        # データベースを更新
        db.session.commit()
        # 処理完了後、pictapp.indexにリダイレクト
        return redirect(url_for('pictapp.index'))
    
    # トップページへのアクセスは、
    # SignupFormのインスタンスformを引き渡す
    return render_template('upload.html', form=form)

"""詳細ページ
"""
@pictapp.route('/detail/<int:id>')
@login_required
def show_detail(id):
    #apps.modelsモジュールmodelpictのUserPictureモデルで
    #データベースから<int:id>で取得したidのレコードを抽出
    detail = db.session.get(modelpict.UserPicture, id)
    playlist_url = None

    if request.method == 'POST':
        playlist_url = request.detail.url
        if playlist_url:
            playlist_id = playlist_url.split('/')[-1]
            playlist_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"

    

    return render_template('detail.html', detail=detail)

@pictapp.route('/user-list/<int:user_id>')
@login_required
def user_list(user_id):
    stmt = select(
        modelpict.UserPicture).filter_by(user_id=user_id).order_by(
            modelpict.UserPicture.create_at.desc())
    #データベースにクエリを発行
    userlist = db.session.execute(stmt).scalars().all()

    return render_template('userlist.html', userlist=userlist)

"""マイページのルーティングとビューの定義
"""
@pictapp.route('/mypage/<int:user_id>')
@login_required
def mypage(user_id):
    stmt = select(
        modelpict.UserPicture).filter_by(user_id=user_id).order_by(
            modelpict.UserPicture.create_at.desc())
    #データベースにクエリを発行
    mylist = db.session.execute(stmt).scalars().all()

    #抽出したレコードをmylist=mylistに格納して
    #mypage.htmlをレンダリングする
    return render_template('mypage.html', mylist=mylist)

"""テーブルからレコードを削除する機能のルーティングとビューの定義
"""
@pictapp.route('/delete/<int:id>')
@login_required
def delete(id):
    entry = db.session.get(modelpict.UserPicture, id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('pictapp.index'))

# 修正：同じ名前の関数名を避けるために関数名を変更
@pictapp.route('/playlist', methods=['GET', 'POST'])
def show_embedded_playlist():
    form = forms.UploadImageForm()

    playlist_url = None  # プレイリストの埋め込みURLを初期化

    if form.validate_on_submit():
        url = form.url.data
        playlist_id = url.split('/')[-1]
        playlist_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
    
    return render_template('index.html', form=form, playlist_url=playlist_url)