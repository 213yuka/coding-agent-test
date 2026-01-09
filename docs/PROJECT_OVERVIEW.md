# coding-agent-test プロジェクト概要

## プロジェクト構造

```
coding-agent-test/
├── agents/                    # エージェント関連のプロンプトファイル
│   └── plan-docsAutomation.prompt.md
├── docs/                      # プロジェクトドキュメント
│   ├── PROJECT_OVERVIEW.md   # このファイル
│   └── SEQUENCE_DIAGRAMS.md  # シーケンス図
└── prompts/                   # その他のプロンプトファイル（もしあれば）
```

## 概要

このプロジェクトは、AIエージェントを使用したコーディング支援のテストリポジトリです。

### agentsフォルダ

AIエージェントの動作を定義するプロンプトファイルを格納しています。

- **plan-docsAutomation.prompt.md**: ドキュメント自動化の計画を行うエージェントのプロンプト定義

### docsフォルダ

プロジェクトの技術ドキュメントを格納しています。

## 使用方法

1. `agents`フォルダ配下のプロンプトファイルを参照
2. 各エージェントの定義に従って処理を実行

## 今後の拡張予定

- 追加のエージェント定義
- APIドキュメント
- 使用例とサンプルコード

---
Last updated: 2026-01-09 00:25:32 UTC
