# DjangoとReactでアプリケーションを構築する。
## 例：Todo管理アプリケーションの構築
今回は題材としてTodo管理アプリケーションを構築する。  

### 構成
![構成図](/out/PlantUML-images/application-composition/application-composition.png)

## 手順
下記の手順で構築していきます。

### Anacondaを使って構築する
まずはpythonのパッケージ管理アプリケーションのAnacondaを入れていきます。  
Anacondaを使うことでPython環境の切り分けができます。

ここからインストール→[Anaconda公式サイト](https://docs.anaconda.com/)  

下記のコマンドで環境を作ります。（meetupって名前の環境を作りました）   
※アプリケーションごとに作ったらよいです
```
conda create -n meetup
```

meetup環境を使います。ついでにpythonを入れます。
```
conda activate meetup
conda install python=3.12
```

これでこのアプリケーション用にpythonパッケージをインストールすることができます。

### Django環境を作っていく
Djangoを入れて、Djangoのコマンドでプロジェクトを作成（backendフォルダ内にプロジェクトが構築されます。さらにその中にbackendアプリケーションが作成されています）
```
pip install django
django-admin startproject backend
```
Djangoを起動してみます。（止める場合は「Ctrl + C」）
```
cd backend
python manage.py runserver
```
[http://localhost:8000/](http://localhost:8000/)にアクセスし、こんな画面が出れば正しく起動しています。
![構成図](/images/django-start-screen.png)

管理画面に入りたいので、特権ユーザーを作成します。
そのために、データベース（ここではsqlite）にテーブル等を作成します。
```
python manage.py migrate
python manage.py createsuperuser
```

[http://localhost:8000/admin/](http://localhost:8000/admin/)にアクセスします。
作成したユーザーでログインできます。

### フォルダ構成を整理する
backend/backendをbackend/configに変更する。
それに伴い、manage.pyやsettings.pyに記述のパスを変更する。

### 設定ファイルを書き換える
設定ファイルを本番環境と手元のローカル環境と切り分けます。  

|     |     |
| --- | --- | 
| 本番環境 | config/production.py |
| ローカル | config/development.py |

### DjangoをAPIに対応する
必要なAPI対応のパッケージをインストール。
```
pip install django-cors-headers
pip install djangorestframework
pip install djangorestframework-simplejwt
```

設定ファイルに書いていきます。
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders", # 追加
    "rest_framework", # 追加
]
```
url.pyも修正
```
from django.contrib import admin
from django.urls import include, path # includeを追加
from rest_framework import routers # 追加

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)), #追加
    path("admin/", admin.site.urls),
]
```