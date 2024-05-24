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

### バックエンドのtodoモデルを作成
backend/todoを作成（__init__.pyも）し、その中にmodels、serializers、viewsを作成。  
URLを定義するurls.pyも作成


config/settigns.pyにtodoを追加
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    "rest_framework",
    "todo",
]
```

config/urls.pyにtodoのurlsを追加
```
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/", include("todo.urls")), # 追加
]
```
下記のファイル（フォルダ）を作成
- todo/modesls/Todo.py
- todo/serializers/TodoSerializer.py
- todo/views/TodoView.py
- todo/urls.py
- todo/migrations/

todo/modesls/Todo.pyの実装
```
from django.db import models

class ToDo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

todo/serializers/TodoSerializer.pyの実装
```
from rest_framework import serializers
from backend.todo.models.Todo import ToDo

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'
```
todo/views/TodoView.pyの実装
```
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from backend.todo.models.Todo import ToDo
from todo.serializers import ToDoSerializer

class ToDoListCreate(APIView):
    def get(self, request):
        todos = ToDo.objects.all()
        serializer = ToDoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ToDoDetail(APIView):
    def get_object(self, pk):
        try:
            return ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        todo = self.get_object(pk)
        serializer = ToDoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = self.get_object(pk)
        serializer = ToDoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

todo/urls.pyの実装
```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.views.TodoView import ToDoListCreate, ToDoDetail

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path('todo/', ToDoListCreate.as_view(), name='todo-list-create'),
    path('todo/<int:pk>/', ToDoDetail.as_view(), name='todo-detail'),
]
```

todo/migrationsはフォルダと内容の__init__.pyを作成


### フロントエンドをcreate-react-appで実装する
```
npx create-react-app frontend --template typescript
cd frontend
npm start
```
