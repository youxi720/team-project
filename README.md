<h1>Chick-teck # hackathon8</h1>
<section>
<h2>エンジニア交流サイト</h2>
<p>｢新人エンジニアはなかなか先輩エンジニアと繋がれない｣</p>
<p>｢海外のエンジニアとも交流したいけど繋がれない｣</p>
<p>そうした課題を解決するアプリケーションです。</p>
</section>

<section>
<h2>主な機能</h2>
<p>こちらはハッカソンの即席チームにて作成しました</p>
<ul>
    <li>ログイン/ログアウト機能</li>
    <li>ユーザー検索機能</li>
    <li>個人チャット機能</li>
    <li>コミュニティ機能</li>
    <li>プロフィール機能</li>
</ul>
</section>

<section>
<h2>使用技術</h2>
<ul>
    <li>HTML(bootstrap)/CSS</li>
    <li>Python(Django)</li>
    <li>Docker</li>
    <li>MySQL</li>
    <li>AWS EC2</li>
</ul>
</section>

<section>
<h2>環境構築<h2>
dockerの立ち上げ
```
docker-compose build
docker-compose up
```

backendコンテナ内での操作(例)
```
docker exec -it backend bash
# migration(modelの変更をDBに反映)
python manage.py makemigrations
python manage.py migrate

# django立ち上げ
python manage.py runserver 0.0.0.0:8000
# http://localhost:8000/home でブラウザに表示される

# 管理ユーザーの作成
python manage.py createsuperuser
```
</section>

<section>
mysqlの操作
```
# コンテナ内へ
docker exec -it mysql bash
% mysql へログイン(パスワードは`django`)
mysql -u django -p

# mysql ログイン後の操作

mysql> SHOW DATABASES;

mysql> USE django;

mysql> SHOW tables;
</section>