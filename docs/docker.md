# Docker での利用方法

dialogapi を Docker コンテナとして実行する方法を解説します。

dialogapi を clone してそのディレクトリ以下に移動します。

```sh
$ cd dialogapi
```

イメージをビルドします。

```sh
$ docker image build -t dialogapi .
```

コマンドの実行について、 Docker を使用しない場合に `VARKEY1=VARVAL1 VARKEY2=VARVAL2 python -u -m dialogapi.main` としていた部分を
`docker container run -v $(pwd):/workspace:ro -it --rm dialogapi -e VARKEY1=VARVAL1 -e VARKEY1=VARVAL2` のように置き換えて実行します。

例えば、次のようなコマンドは

```sh
$ USER=YOUR_USER_NAME PASSWORD=YOUR_PASSWORD HOST=host.example.jp python -u -m dialogapi.main project list --config config.yml --server TestServer
```

Docker を使用する場合は次のコマンドを実行することになります。


```sh
$ docker container run -v $(pwd):/workspace:ro -it --rm dialogapi -e USER=YOUR_USER_NAME -e PASSWORD=YOUR_PASSWORD -e HOST=host.example.jp project list --config config.yml --server TestServer
```
