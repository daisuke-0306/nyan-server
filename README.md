# 🐱 にゃん.jp - Infrastructure Portfolio

🌐 https://にゃん.jp
🟢 Status: Online
🔒 HTTPS Enabled
🚀 CI/CD Enabled
📣 Discord Monitoring Enabled

---

## 概要

AWS EC2上にDocker・nginx・Flask・PostgreSQLを用いた
Webシステムを構築しました。

GitHub ActionsによるCI/CD、
pytestによる自動テスト、
Discordによる障害監視・復旧通知を実装し、
本番運用を意識したインフラ構成を目指しました。

---

## 使用技術

- AWS EC2 (Ubuntu)
- nginx (リバースプロキシ)
- Docker / Docker Compose
- Flask
- PostgreSQL
- GitHub Actions (CI/CD)
- pytest
- Discord Webhook
- Let's Encrypt (HTTPS)

---

## アーキテクチャ

```text
User
 ↓ HTTPS
nginx (Reverse Proxy)
 ↓
Docker
 ├─ Flask (app)
 └─ PostgreSQL (db)
```

---

## 主な機能

- HTTPS対応Webサイト公開
- Flask + PostgreSQLによるDB連携
- Health Checkページ (`/health`)
- ステータスページ (`/status`)
- DB確認ページ (`/read`)
- GitHub ActionsによるCI/CD
- pytestによる自動テスト
- Discordによる障害通知・復旧通知

---

## CI/CD

```text
git push
 ↓
GitHub Actions
 ↓
pytest
 ↓
テスト成功時のみAWSへデプロイ
```

不具合を含むコードが本番環境へ反映されるリスクを低減しています。

---

## 監視・通知

```text
DB障害
 ↓
Database: NG
 ↓
Discordへ障害通知（1回のみ）

DB復旧
 ↓
Discordへ復旧通知
```

障害通知の連投を防ぐため、
同一障害では一度だけ通知し、
復旧時に状態をリセットする仕組みを実装しています。

---

## 工夫した点

- Dockerによる環境分離と再現性の確保
- GitHub ActionsによるCI/CDの自動化
- pytestによる品質担保
- Discordを用いた障害監視・復旧通知
- 障害通知の連投防止機能
- Web UIによるシステム状態の可視化

---

## 苦労した点

さくらVPSでの検証後、AWS EC2へ移行して再構築しました。
SSH設定ミスによるサーバー再構築や、
nginx・Docker・GitHub Actionsの設定で多くのエラーを経験しましたが、
ログを確認しながら原因を切り分け、
試行錯誤しながら解決する力を身につけました。
