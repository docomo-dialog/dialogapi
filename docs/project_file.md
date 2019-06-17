# プロジェクト構成ファイル

dialogapi の利用にあたり、はじめにプロジェクトの構成を記述した **プロジェクト構成ファイル** を作成します。

このチュートリアルでは、二つのボット "hellobot", "qbot" から構成されるプロジェクト「DA」を dialogapi を使ってデプロイし、テストまで行う方法を示します。

ボットと対応するリソースのディレクトリ構成は次の通りとします。
なお、このディレクトリは本リポジトリの `dialogapi/sample` 以下に格納されています。

```sh
da
├── hellobot  # hellobot ボットのリソースを含むディレクトリ
│   ├── hello.aiml  # AIML
│   ├── hello.config  # ボットコンフィグファイル
│   ├── hello.map  # MAPファイル
│   ├── hello.property  # ボットプロパティファイル
│   ├── hello.set  # SETファイル
│   └── hello_test.yml  # テストファイル
└── qbot  # qbot ボットのリソースを含むディレクトリ
    ├── qbot.aiml  # AIML ファイル
    └── qbot_test.yml  # テストファイル
```

テストファイルについては後ほど説明しますので、まずは xAIML の各リソースファイルおよびテストファイルを用意するという点を確認してください。

## プロジェクト構成ファイルの書き方

このプロジェクト構成に従って YAML 形式のプロジェクト構成ファイルを作成します。

```yaml
version: "1"

servers:
- name: TestServer
  config:
    host: ${HOST}
    port: 10443
    protocol: https
    ssl_verify: true
    user: ${USER}
    password: ${PASSWORD}
    endpoint:
      management:
        prefix: /management/v2.7
        header:
          content-type: application/json;charset=utf-8
      registration:
        prefix: /UserRegistrationServer/users/applications
        header:
          content-type: application/json;charset=utf-8
      dialogue:
        prefix: /SpontaneousDialogueServer/dialogue
        header:
          content-type: application/json;charset=utf-8

projects:
- name: TestProject
  config:
    project_name: DA
  bots:
  - name: QBot
    config:
      bot_id: DA_QBot
    aimls:
    - qbot/qbot.aiml
    tests:
    - qbot/qbot_test.yml
  - name: HelloBot
    config:
      bot_id: DA_HelloBot
      sraix: global
    configs:
      - hellobot/hello.config
    properties:
      - hellobot/hello.property
    aimls:
      - hellobot/hello.aiml
    maps:
      - hellobot/hello.map
    sets:
      - hellobot/hello.set
    tests:
      - hellobot/hello_test.yml
```

設定ファイルは大きく

- `version` セクション
- `servers` セクション
- `projects` セクション

の 3 つから成り立っています。

### version セクション

`version` セクションでは、設定ファイルのバージョンを指定します。指定が必須となっていますので、 `1` を指定してください。

### servers セクション

`servers` セクションでは、 自然対話サーバの設定をリストで記述します。
各設定には次の項目を記述します。

| キー  | 必須 | 説明 |
| ---  | --- | --- |
| name | o | サーバの名前をつけます。この名前は dialogapi の実行時にサーバを指定する際に使います。 |
| config | o | サーバの設定をこの下で設定します。 |

`config` では、次の内容を設定します。

| キー  | 必須 | 説明 |
| ---  | --- | --- |
| host | o | サーバのホスト名を指定します。 |
| port | o | サーバのポートを指定します。 |
| protocol | o | サーバに接続するプロトコルを http か https のどちらかで指定します。 |
| ssl_verify | x | プロトコルが https の場合、 SSL 検証を行うかどうか指定します。指定しない場合は true となります。 |
| user | x | 自然対話エンジンのユーザ名を指定します。 Management API を利用する場合は指定してください。 |
| password | x | 自然対話エンジンのパスワードを指定します。 Management API を利用する場合は指定してください。 |
| endpoint | x | `management`, `registration`, `dialogue` で、このサーバの Management API, Registration API, Dialogue API のエンドポイントの prefix およびリクエストヘッダ情報を記述します。 |

### projects セクション

`projects` では、プロジェクトの設定をリストで記述します。
各設定には次の項目を記述します。

| キー  | 必須 | 説明 |
| ---  | --- | --- |
| name | o | プロジェクトの名前を指定します。この名前は dialogapi の実行時にプロジェクトを指定する際に使います。 |
| config | o | `project_name` でプロジェクト名を指定します。この値は `name` と異なり、自然対話サーバに存在する実際のプロジェックト名でなければなりません。 |
| bots | o | このプロジェクトに属するボットの設定を行います。 |

`bots` では、ボットの設定をリストで記述します。
各設定には次の項目を記述します。

| キー  | 必須 | 説明 |
| ---  | --- | --- |
| name   | o | ボットの名前をつけます。この名前は dialogapi の実行時にボットを指定する際に使います。 |
| config | o | 必須パラメータである `bot_id` で自然対話サーバにデプロイする際のボットIDを指定します。またオプションの `sraix` で sraix の設定を行います。 |
| aimls  | x | アップロードする AIML ファイルのパスをリストで指定します。 |
| sets   | x | アップロードする SET ファイルのパスをリストで指定します。 |
| maps   | x | アップロードする MAP ファイルのパスをリストで指定します。 |
| configs| x | アップロードするボットコンフィグファイルのパスをリストで指定します。 |
| properties | x |  アップロードするボットプロパティファイルのパスをリストで指定します。 |
| tests  | x | テストファイルをリストで指定します。 |

なお、パスワードのような 設定ファイル中に記載するべきではない値や、コマンド実行時に変更したい値は環境変数を使って設定ファイルに記述します。
環境変数を設定ファイルで参照するには `${環境変数名}` のように記述してください。
