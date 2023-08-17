from setuptools import setup, find_packages

setup(
    name='spotify_share_project',  # パッケージ名
    version='0.1',              # バージョン
    packages=find_packages(),    # サブディレクトリ内のパッケージを自動的に探索
    install_requires=[
        'alembic==1.11.1',
        'blinker==1.6.2',
        'certifi==2023.7.22',
        'charset-normalizer==3.2.0',
        'click==8.1.6',
        'colorama==0.4.6',
        'dnspython==2.4.1',
        'email-validator==2.0.0.post2',
        'Flask==2.3.2',
        'Flask-Login==0.6.2',
        'Flask-Mail==0.9.1',
        'Flask-Migrate==4.0.4',
        'flask-paginate==2022.1.8',
        'Flask-SQLAlchemy==3.0.5',
        'Flask-WTF==1.1.1',
        'greenlet==2.0.2',
        'gunicorn==21.2.0',
        'hello-app==0.1',
        'heroku==0.1.4',
        'idna==3.4',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.2',
        'Mako==1.2.4',
        'MarkupSafe==2.1.3',
        'packaging==23.1',
        'python-dateutil==1.5',
        'python-dotenv==1.0.0',
        'redis==4.6.0',
        'requests==2.31.0',
        'six==1.16.0',
        'spotify-share==0.1',
        'spotipy==2.23.0',
        'SQLAlchemy==2.0.19',
        'typing_extensions==4.7.1',
        'urllib3==2.0.4',
        'waitress==2.1.2',
        'Werkzeug==2.3.6',
        'WTForms==3.0.1',
    ],
    author='karaage0000',  # 作者
    author_email='karaagekun0451@gmail.com',  # 作者のメールアドレス
    description='to share spotify playlist',  # パッケージの説明
    url='https://github.com/karaage0000/flask_app.git',  # パッケージのURL
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
