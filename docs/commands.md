# コマンド一覧

dialogapi が提供するコマンド一覧です。
**冪等性** は、コマンドを2回以上繰り返しても、1回目に実行した後のサーバ上のプロジェクトの状態から変化しないことを表します。
**安全性** は、コマンドを実行してもサーバ上のプロジェクトの状態が変化しないことを意味します。

| コマンド | 冪等性 | 安全性 | 説明 | CLI 使用例 |
| --- | --- | --- | --- | --- |
| project list | o | o | プロジェクトの一覧を表示する | dialogapi project list --config config.yml --server TestServer |
| project setup | o | x | プロジェクトの全てのボット作成・設定を行う。 | dialogapi project setup --config config.yml --server TestServer --project DialogAPITestProject |
| project reset | o | x | 全てのボットを削除してプロジェクトを新規の状態にする。 | dialogapi project reset --config config.yml --server TestServer --project DialogAPITestProject |
| project test | o | o | プロジェクトの全てのボットをテストする。 | dialogapi project test  --config config.yml --server TestServer --project DialogAPITestProject |
| bot list | o | o | ボットの一覧を表示する。 | dialogapi bot list --config config.yml --server TestServer --project DialogAPITestProject |
| bot setup | o | x | 設定ファイルに従ってボットを作成・設定してプロジェクトに追加する | dialogapi bot setup --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| bot add | x | x | プロジェクトへボットを追加する | dialogapi bot add --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| bot remove | x | x | プロジェクトからボットを削除する。 | dialogapi bot remove --config config.yml --server TestServer --project --bot QBot |
| bot update | x | x | ボットを更新する。 | dialogapi bot update --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| bot compile | o | x | ボットをコンパイルする。 | dialogapi bot compile --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| bot transfer | o | x | ボットを転送する。 | dialogapi bot transfer --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| bot test | o | o | テストファイルに従ってボットをテストする。 | dialogapi bot test --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| aiml upsert | o | x | AIMLを追加する。存在すれば上書きする。 | dialogapi aiml upsert --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| set upsert | o | x | SETを追加する。存在すれば上書きする。 | dialogapi set upsert --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| map upsert | o | x | MAPを追加する。存在すれば上書きする。 | dialogapi map upsert --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| property upsert | o | x | BotPropertyを追加する。存在すれば上書きする。 | dialogapi property upsert --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
| config upsert | o | x | BotConfigを追加する。存在すれば上書きする。 | dialogapi config upsert --config config.yml --server TestServer --project DialogAPITestProject --bot QBot |
