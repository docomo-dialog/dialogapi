# テストファイル

ここでは dialogapi がサポートするテストの書き方を説明します。
テストファイルは次のような YAML 形式で記述します。

```yml
config:
  keep_app_id: true

tasks:
  - name: 挨拶テスト
    request:
      voiceText: こんにちは
    tests:
      - method: equal
        param: response.systemText.expression
        expected: こんにちは。元気ですね！
  - name: NoMatchテスト
    request:
      voiceText: こんちは
      location:
        lat: 0
        lon: 0
      clientData:
        option:
          t: ols
    tests:
      - method: equal
        param: response.systemText.expression
        expected: "NOMATCH"
```

テストファイルは大きく二つのセクション `config` および `tasks` から構成されています。

`config` セクションでは、 `keep_app_id` でテスト中に `app_id` を更新するかどうか指定します。

| キー  | 必須 | 説明 |
| ---  | --- | --- |
| keep_app_id | x | テストファイル中の全てのタスクで同一の `app_id` を使用するか指定する。 `true` の場合は全てのタスクで同一の `app_id` を使用し、`false` の場合はタスク毎に異なる `app_id` を使用する。指定しない場合 `false` となる。 |

テストは **タスク** という単位に分けられ、 `tasks` セクションでタスクのリストを記述します。
タスクには次の内容を記述します。

| キー  | 必須 | 説明 |
| ---  | --- | --- |
| name | o | タスク名 |
| request | o | リクエストを記述します。ここに記述した内容が JSON ボディとなります。 |
| tests | o | テストの内容を記述します。 |

タスクは複数の **テスト** から構成されます。
テストは、 `tests` 以下にリスト形式で次の内容を記述します。

| キー  | 必須 | 説明 |
| ---  | --- | --- |
| method | o | テストに使うテストメソッドを指定します。 |
| param | o | メソッドに渡すレスポンス中のパラメータを指定します。`response` がレスポンスの JSON を表し、 `key` という値を参照するには `response.key` のように`.` でつなげて記述します。 |
| expected | o | param と比較する文字列を記述します。 |

メソッドは、テスト中の `param` が `expected` に記載した内容に合致しているか確認します。
`method` にて以下のどのメソッドを使うか指定します。

| テストメソッド名 | 動作 |
| --- | --- |
| equal | `param` で指定した文字列が `expected` と一致するかテストします。 |
| not_equal | `param` で指定した文字列が `expected` と一致しないことをテストします。 |
| in | `param` で指定した文字列が `expected` の少なくとも一つと一致しているかを確認します。 |
| not_in | `param` で指定した文字列が `expected` の全てと一致しないことをテストします。 |
| regex_equal | `param` で指定した正規表現が `expected` にマッチするかテストします。 |
| regex_not_equal | `param` で指定した正規表現が `expected` とマッチしないことをテストします。 |
| regex_in | `param` で指定した正規表現が `expected` の少なくとも一つとマッチするかテストします。 |
| regex_not_in | `param` で指定した正規表現が `expected` の全てとマッチしないことをテストします。 |

これらを使ったより複雑なテストの例をあげます。

```yaml
config:
  keep_app_id: true

tasks:
  -
    name: 「こんにちは」に対する名前・年齢質問テスト
    request:
      voiceText: こんにちは
      initTopicId: conv
    tests:
      - method: not_equal
        param: response.systemText.expression
        expected: おはよう！
      - method: in
        param: response.systemText.expression
        expected:
          - こんにちは！あなたの名前は何ですか？
          - こんにちは！あなたの年齢はいくつですか？
      - method: not_in
        param: response.systemText.expression
        expected:
          - おはよう！
          - こんにちは！
      - method: regex_equal
        param: response.systemText.expression
        expected: ^こんにちは！.+$
      - method: regex_equal
        param: response.systemText.expression
        expected: あなたの
      - method: regex_not_equal
        param: response.systemText.expression
        expected: ^こんにちは！対話システムへようこそ！$
      - method: regex_in
        param: response.systemText.expression
        expected:
          - ^.+あなたの名前は何ですか？$
          - ^.+あなたの年齢はいくつですか？
      - method: regex_not_in
        param: response.systemText.expression
        expected:
          - ^あなたの$
```