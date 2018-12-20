# Tubデータ再生ツール tubpayer.py

Tubディレクトリ上のファイルをマジックナンバーの小さい順に開き、一定間隔（デフォルトは1/20秒）でMQTTブローカへ送信する。

本コードの対象とするMQTTブローカは、IBM Watson IoT Platformのみとする。

Donkey Carへ [coolerking/donkeypart_telemetry](https://github.com/coolerking/donkeypart_telemetry) をインストールせずに、Tubディレクトリを取得した状態を　[Donkey Telemetry](https://github.com/coolerking/donkey_telemetry) で再現することが可能である。


## インストール

### ブローカの作成

1. IBM Cloud コンソールを開く
2. ログイン
3. 「カタログ」を選択
4. 「IoT」> 「Internet of Things Platform」
5. 「デプロイする地域/ロケーションの選択」を適当に選択
6. 「組織の選択」を適当に選択
7. 「スペースの選択」を適当に選択
8. 画面右下の「作成」押下
9. ダッシュボード画面のCloudFoundryサービス上から作成したサービスを選択
10. 「起動」押下

### デバイス（Publisher）の追加

1. 「＋デバイスの追加」押下
2. 「デバイスタイプ」に`donkeycar`と入力
3. 「デバイスID」にDonkeyCar固有名を入力（例：RaspberryPiのホスト名やMacアドレス）
4. 「次へ」押下
5. 「次へ」押下
6. 「次へ」押下
7. 「完了」押下
8. 画面に表示された、組織ID、デバイスタイプ、デバイスID、認証トークンをメモしておく

実際に接続しているかどうかを確認したい場合は、該当デバイスを選択することで詳細な状態確認可能。

### 設定ファイルの作成

1. ローカルPC上の`device.ini`を`<デバイスID>.ini`という名前でコピー
2. `<デバイスID>.ini`を編集
3. `{}`部分をすべて編集
4. `auth-metho`行は編集不要
5. `clean-session` 行は`true`としておく

### Pythonパッケージのインストール

1. ローカルPCでPythonを実行できるコンソールを開く
2. 以下のコマンドを実行し、必要なPythonパッケージをインストールする
   ```
   pip install docopt
   pip install ibmiotf
   ```

## 実行

以下のように実行すると、`./tub_test` ディレクトリに入っているTubデータを順番に1/20秒の間隔でMQTTブローカへ送信する。
```bash
python tubplayer.py --tub tub_test
```

すべてのTubデータを送信終了すると、接続を閉じ終了する。

ほかの引数については、以下のコマンドを実行して確認のこと。
```bash
python tubplayer.py --help
```

終了させたい場合は、Ctrl+Cを押す。