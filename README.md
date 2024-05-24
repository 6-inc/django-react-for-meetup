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
Djangoを入れて、Djangoのコマンドでプロジェクトを作成
```
pip install django
django-admin startproject myapp
```