set -eu

alias dialogapi="python -u -m dialogapi.main"

cd da

# Test setup: 初期化
dialogapi project reset --config config.yml --server TestServer --project DialogAPITestProject

# プロジェクトコマンドのテスト
dialogapi project list  --config config.yml --server TestServer
dialogapi project setup --config config.yml --server TestServer      --project DialogAPITestProject
dialogapi project setup --config config.yml --server TestServer      --project DialogAPITestProject  # 冪等テスト
dialogapi project test  --config config.yml --server TestServer      --project DialogAPITestProject
dialogapi project test  --config config.yml --server TestServer-http --project DialogAPITestProject  # http エンドポイントへのテスト
dialogapi project reset --config config.yml --server TestServer      --project DialogAPITestProject

# ボットのテスト
dialogapi bot       list     --config config.yml --server TestServer --project DialogAPITestProject
dialogapi bot       add      --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi bot       update   --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi aiml      upsert   --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi set       upsert   --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi map       upsert   --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi property  upsert   --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi bot       compile  --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi bot       transfer --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi bot       test     --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi bot       remove   --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi bot       setup    --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi bot       remove   --config config.yml --server TestServer --project DialogAPITestProject --bot QBot

# ボットプロパティのテスト
dialogapi bot      add    --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi property upsert --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi property upsert --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi bot      remove --config config.yml --server TestServer --project DialogAPITestProject --bot QBot

# ボットコンフィグのテスト
dialogapi bot      add    --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi config   upsert --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi config   upsert --config config.yml --server TestServer --project DialogAPITestProject --bot QBot
dialogapi bot      remove --config config.yml --server TestServer --project DialogAPITestProject --bot QBot

# Test tear down: 初期化
dialogapi project reset --config config.yml --server TestServer --project DialogAPITestProject

#  IP指定のhttps接続でSSL検証しない例 - エラーが発生しないことを確認する
dialogapi project list  --config config.yml --server TestServer-host_ip-ssl_noverify

# SSL検証が失敗する例 - エラーが発生することを確認する
echo "--- Start SSL verification failure test ---"
result=0
dialogapi project list  --config config.yml --server TestServer-host_ip-ssl_verify || result=$?
if [ "${result}" = 1 ]; then
    echo "Finished SSL verification failure test succesfully exited with status code ${result}"
else
    echo "SSL verification failure test failed with status code ${result}"
    exit 1
fi
echo "--- Succesfully finished SSL verification failure test ---"
