# 作業分解用LLMワークフローサンプル

## 概要
作業分解を行うLLMワークフローのサンプルソースです。

## 実行方法
リポジトリ内で以下を実行:

```bash
uv run python main.py
```

## 環境構築
### 必要条件
- Python 3.14
- uv (パッケージマネージャー)

### 手順
1. uvのインストール
   ```bash
   # macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Windows
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. プロジェクトセットアップ
   ```bash
   uv sync
   ```

3. APIキーの登録
   ```bash
   cp .env.sample .env
   ```
   `OLLAMA_API_KEY`に自身のAPIキーを登録。

### Ollama Cloud APIキー発行方法
Ollama公式ページでアカウントを作成後、右上のアイコンからSettings -> Keys -> Add API Keyでキーを発行。

Ollama 公式ページリンク:
https://ollama.com/