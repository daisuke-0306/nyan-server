# 🐱 にゃん.jp - Infrastructure Portfolio

🌐 https://にゃん.jp 
🟢 Status: Online 
🔒 HTTPS Enabled 
🚀 CI/CD Enabled 
📣 Discord Monitoring Enabled

---

## 概要

AWS EC2上にDocker・nginx・Flask・PostgreSQLを用いたWebシステムを構築しました。

GitHub ActionsによるCI/CD、pytestによる自動テスト、Discordによる障害監視・復旧通知を実装し、本番運用を意識したインフラ構成を目指しました。

また、本番環境とは別に学習用AWS環境を構築し、Application Load Balancer（ALB）とAuto Scaling Group（ASG）を用いた高可用性構成や自己修復（Self Healing）の仕組みを検証しました。

---

## 使用技術

- AWS EC2 (Ubuntu)
- nginx (Reverse Proxy)
- Docker / Docker Compose
- Flask
- PostgreSQL
- GitHub Actions (CI/CD)
- pytest
- Discord Webhook
- Let's Encrypt (HTTPS)
- Application Load Balancer (ALB)
- Auto Scaling Group (ASG)

---

## 本番環境アーキテクチャ

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

障害通知の連投を防ぐため、同一障害では一度だけ通知し、復旧時に状態をリセットする仕組みを実装しています。

---

## 工夫した点

- Dockerによる環境分離と再現性の確保
- GitHub ActionsによるCI/CDの自動化
- pytestによる品質担保
- Discordを用いた障害監視・復旧通知
- 障害通知の連投防止機能
- Web UIによるシステム状態の可視化
- 手動デプロイによる人的ミスを減らすため、自動テストと自動デプロイを導入
- 障害発生時と復旧時のみ通知を送信し、不要な通知の連投を防止

---

## AWS 高可用性・Auto Scaling検証

本番環境とは別に学習用AWS環境を構築し、高可用性と自己修復（Self Healing）の仕組みを検証しました。

### 構成

```text
Internet
    ↓
Application Load Balancer (ALB)
    ↓
Auto Scaling Group (ASG)
   ↙                 ↘
EC2 (AZ1)         EC2 (AZ2)
```

### 実施内容

- EC2インスタンスを2台構築
- nginxを導入し、ALBによる負荷分散を実装
- Target GroupとHealth Checkを設定
- Launch Templateを作成
- Auto Scaling Groupを構築
- EC2を2つのAvailability Zoneへ分散配置
- EC2インスタンスを意図的にTerminateし、自動的に新しいEC2インスタンスが生成されることを確認

### 学んだこと

- ALBは複数のEC2へリクエストを分散し、可用性を向上させること
- Health Checkにより異常なEC2が自動的に切り離されること
- Auto Scaling GroupはDesired Capacityを維持するため、自動でインスタンスを生成すること
- クラウドでは「サーバーを修理する」のではなく、「設計図から再作成する」という考え方が重要であること
- 単一サーバー構成だけでなく、障害発生を前提としたシステム設計の重要性

---

## 苦労した点

本システムは、一度さくらVPS上で約2週間かけて構築した環境が、SSHの設定変更によってサーバーへ接続できなくなり、復旧が困難になったことをきっかけに、AWS EC2上でゼロから再構築したものです。

再構築では、nginx・Docker・Flask・PostgreSQL・GitHub Actions・Discord通知などを一つずつ組み直し、本番運用を意識したインフラ環境の構築に取り組みました。さらに、学習用環境ではALBやAuto Scaling Groupを用いた高可用性構成の検証も行いました。

その過程で、nginxの設定ミス、Dockerのビルドエラー、GitHub Actionsの認証エラー、ALBの503エラー、Target GroupのUnused・Unhealthy状態など、多くの問題に直面しました。しかし、ログやHealth Checkの状態を確認し、Security Group・Target Group・アプリケーション設定を一つずつ切り分けながら原因を特定し、試行錯誤を重ねて解決しました。

この経験を通して、インフラでは「壊れないように作る」だけでなく、「障害発生時に原因を切り分け、再構築・復旧できる力」が重要であることを実践的に学びました。

---

## 今後の展望

- Amazon RDSを利用したDBの分離
- ALB + HTTPS + 独自ドメイン構成への発展
- Dockerコンテナを利用したAuto Scaling環境の構築
- Infrastructure as Code（IaC）の導入
- 監視・ログ分析機能のさらなる強化
