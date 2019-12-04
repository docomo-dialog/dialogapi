# dialogapi - 自然対話サーバのプロジェクト構成管理ツール

dialogapi は、構成ファイルに従ってプロジェクトを自然対話サーバにデプロイ、テストするコマンドラインインターフェースツールです。
dialogapi によりプロジェクトをコードで一括管理しデプロイとテストを自動化することで、ボットの開発体制を改善します。

dialogapi は次のようなデプロイとテストを自動化する一連のコマンドを提供します。これにより、開発者はボット開発に集中できるようになります。

```sh
# プロジェクトのデプロイ
$ python -u -m dialogapi.main project setup --config config.yml --server TestServer --project TestProject
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

# プロジェクトのテスト
$ python -u -m dialogapi.main project test --config config.yml --server TestServer --project TestProject
Testing bot DA_QBot
- 「こんにちは」に対する名前・年齢質問テスト ... ok.
Testing bot DA_HelloBot
- 挨拶テスト ... ok.
- NoMatchテスト ... ok.
```

## インストール

バージョン 3.6 以上の Python をインストールしたのち、pip で dialogapi をインストールしてください。

```sh
$ pip install git+https://github.com/docomo-dialog/dialogapi
```

## 使い方

次のチュートリアルにしたがって、使い方を理解してください。

1. [プロジェクト構成ファイルを作成する](docs/project_file.md)
2. [テストファイルを作成する](docs/test_file.md)
3. [プロジェクトをデプロイ・テストする](docs/execution.md)

dialogapi が提供する全てのコマンドは [コマンド一覧](docs/commands.md) を確認してください。

本ツールを Docker コンテナとして利用したい場合は [Dockerでの利用](docs/docker.md) を確認してください。

## License

New BSD License
