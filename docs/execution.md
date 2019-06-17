# 実行方法

プロジェクト構成ファイルとテストファイルを作成したら、 次の手順でプロジェクトをデプロイ、テストします。

1. プロジェクトを自然対話サーバに **手動で** 作成する
2. dialogapi でプロジェクトをデプロイする
3. dialogapi でプロジェクトをテストし、適切にデプロイが完了したか確認する

はじめに、対象の自然対話サーバに空のプロジェクトを作成します。今回の例では `DA` というプロジェクトを作成してください。

プロジェクトを作成し終えたら、dialogapi でプロジェクトをデプロイします。
まずはプロジェクトのディレクトリに移動します。
このサンプルは本リポジトリの `sample/da` 以下にありますので、次のように対象ディレクトリに移動します。

```sh
$ cd dialogapi/sample/da
```

はじめに、プロジェクト一覧を表示して対象サーバに接続できるかテストしてみましょう。
これには、dialogapi の `project list` コマンドを使います。

```sh
$ USER=YOUR_USER_NAME PASSWORD=YOUR_PASSWORD HOST=host.example.jp python -u -m dialogapi.main project list --config config.yml --server TestServer
id   name
754  DA
```

このコマンドでは、 `USER=YOUR_USER_NAME PASSWORD=YOUR_PASSWORD HOST=host.example.jp` のようにして設定ファイル中の環境変数に値を渡しています。
この値は各自の環境に合わせて変更してください。

正常に接続できる場合は、プロジェクトの ID と名前が表示されます。

次にプロジェクトをデプロイします。
デプロイには `project setup` コマンドを使います。

```sh
$ USER=YOUR_USER_NAME PASSWORD=YOUR_PASSWORD HOST=host.example.jp python -u -m dialogapi.main project setup --config config.yml --server TestServer --project TestProject
Adding bot DA_QBot ... done
Uploading AIML qbot/qbot.aiml ... done
Compiling bot DA_QBot ... done
Transfering: bot DA_QBot ... done
Adding bot DA_HelloBot ... done
Uploading AIML hellobot/hello.aiml ... done
Uploading Set hellobot/hello.set ... done
Uploading Map hellobot/hello.map ... done
Uploading Config hellobot/hello.config ... done
Uploading Property hellobot/hello.property ... done
Compiling bot DA_HelloBot ... done
Transfering: bot DA_HelloBot ... done
```

このようにエラーが発生せずに終了すればデプロイは完了です。

最後に、デプロイが正常に完了したか確認するためにテストを実行します。
テストには `project test` コマンドを使います。

```sh
$ USER=YOUR_USER_NAME PASSWORD=YOUR_PASSWORD HOST=host.example.jp python -u -m dialogapi.main project test --config config.yml --server TestServer --project TestProject
Testing bot DA_QBot
- 「こんにちは」に対する名前・年齢質問テスト ... ok.
- 「こんにちは」に対する名前・年齢質問テスト ... ok.
- 「こんにちは」に対する名前・年齢質問テスト ... ok.
- 「こんにちは」に対する名前・年齢質問テスト ... ok.
- 「こんにちは」に対する名前・年齢質問テスト ... ok.
- 「こんにちは」に対する名前・年齢質問テスト ... ok.
- 「こんにちは」に対する名前・年齢質問テスト ... ok.
- 「こんにちは」に対する名前・年齢質問テスト ... ok.
Testing bot DA_HelloBot
- 挨拶テスト ... ok.
- NoMatchテスト ... ok.
```

このコマンドで、 `test` 以下に記述した全てのテストを実行し期待通りの動作をしていることを確かめます。

以上でプロジェクトのデプロイは完了です。
プロジェクトを使わなくなったら、 `project reset` コマンドでプロジェクト中のボットを全て削除し、空のプロジェクト作成直後の状態に戻すことができます。

```sh
$ USER=YOUR_USER_NAME PASSWORD=YOUR_PASSWORD HOST=host.example.jp python -u -m dialogapi.main project reset --config config.yml --server TestServer --project TestProject
Removing bot DA_QBot ... done
Removing bot DA_HelloBot ... done
```