# 🐱 にゃん.jp - Infrastructure Portfolio

🌐 https://にゃん.jp 
🟢 Status: Online 
🔒 HTTPS Enabled 
🚀 CI/CD Enabled 
📣 Discord Monitoring Enabled

---

## 概要

AWS EC2上に、Docker・nginx・Flask・PostgreSQLを用いたWebシステムを構築し、独自ドメイン「にゃん.jp」で公開しています。

本番環境では、Amazon CloudFrontをCDNとして配置し、そのオリジンにApplication Load Balancerを設定しています。CloudFrontでは静的コンテンツをキャッシュし、`/api/*` はキャッシュしないBehaviorを設定することで、表示速度の向上とリアルタイムAPIの両立を図っています。

また、GitHub ActionsによるCI/CD、pytestによる自動テスト、CloudWatchによるEC2監視を実装しています。CPU使用率がしきい値を超えた場合は、CloudWatch AlarmからSNSを経由してLambdaを実行し、Discordへ自動通知する監視基盤を構築しました。

本番環境とは別に、ALB・Target Group・Launch Template・Auto Scaling Groupを使用した高可用性構成と、EC2障害時のSelf Healingも検証しています。

---

## 使用技術

### Infrastructure / AWS

- AWS EC2
- Amazon CloudFront
- Application Load Balancer
- Target Group
- Amazon CloudWatch
- CloudWatch Alarm
- Amazon SNS
- AWS Lambda
- IAM Role
- Auto Scaling Group
- Launch Template

### Application

- Ubuntu Linux
- Docker / Docker Compose
- nginx
- Flask
- Gunicorn
- PostgreSQL
- Python / boto3

### CI/CD・監視

- GitHub Actions
- pytest
- Discord Webhook
- Let's Encrypt
- Chart.js
---

## 本番環境アーキテクチャ

```text
User
 │
 │ HTTPS
 ▼
Amazon CloudFront
 │
 │ HTTP : 80
 ▼
Application Load Balancer
 │
 ▼
Target Group
 │
 ▼
AWS EC2
 │
 ▼
Docker Compose
 ├── nginx
 ├── Flask + Gunicorn
 └── PostgreSQL

---

## 主な機能

- 独自ドメイン・HTTPS対応Webサイト
- CloudFrontによるCDN配信
- ALBを経由したEC2へのアクセス
- Flask + PostgreSQLによるDB連携
- CloudWatch APIによるCPU使用率取得
- Chart.jsを用いたリアルタイム監視画面
- CloudWatch AlarmによるCPUしきい値監視
- SNS・Lambda・Discord Webhookによる自動通知
- GitHub ActionsによるCI/CD
- pytestによる自動テスト
- Auto Scaling・Self Healing検証

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

```text
EC2 CPUUtilization
        │
        ▼
Amazon CloudWatch
        │
        ▼
CloudWatch Alarm
        │
        ▼
Amazon SNS
        │
        ▼
AWS Lambda
        │
        ▼
Discord Webhook
```
---

CloudFrontは現在、ALBをオリジンとして使用し、キャッシュBehaviorによってパスごとの扱いを変えている。AWS公式上も、CloudFrontではオリジンとCache Behaviorを設定し、エッジキャッシュを利用してオリジンへのアクセス数と遅延を減らせる。 [oai_citation:4‡AWS ドキュメント](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html?utm_source=chatgpt.com)

## Amazon CloudFront

公開サイトのレスポンス改善とEC2へのリクエスト削減を目的として、CloudFrontを導入しました。

CloudFrontのオリジンには、EC2を直接指定せずApplication Load Balancerを設定しています。これにより、将来的にEC2の台数が増減してもCloudFront側の設定を変更せず、ALB側で負荷分散できる構成にしています。

### Cache Behavior

| Path Pattern | Cache Policy | 目的 |
|---|---|---|
| `Default (*)` | `CachingOptimized` | HTML、CSS、JavaScript、画像などの配信 |
| `/api/*` | `CachingDisabled` | CPU使用率など、リアルタイムAPIの配信 |

`/api/cpu` と `/api/cpu/history` は値が継続的に変化するため、CloudFrontに古い値が保持されないようキャッシュを無効化しています。

### Troubleshooting

CloudFront導入直後、CloudFront経由のアクセスで `504 Gateway Timeout` が発生しました。

原因は、CloudFrontのOrigin Protocol Policyが `HTTPS Only` である一方、ALBにはHTTP 80番のリスナーしか設定されていなかったことです。

Origin Protocol Policyを `HTTP Only` に変更し、CloudFrontからALBへの通信をHTTP 80番に合わせることで解決しました。

---

## Application Load Balancer

CloudFrontのオリジンとしてApplication Load Balancerを配置しています。

### 役割

- EC2へのリクエスト転送
- Target Groupを利用したターゲット管理
- `/health` によるHealth Check
- 将来的な複数EC2への負荷分散
- Auto Scalingとの連携を想定した構成

### Health Check

```text
Protocol: HTTP
Port: 80
Path: /health

---

```markdown
## CloudWatch Alarm・SNS・Lambda・Discord通知

EC2のCPU使用率をCloudWatchで監視し、しきい値を超えた場合にDiscordへ自動通知する仕組みを構築しています。

### 通知フロー

```text
CloudWatch Alarm
        ↓
SNS Topic
        ↓
Lambda Function
        ↓
Discord Webhook

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

本システムの開発では、まずさくらVPS上で約2週間かけて環境を構築しました。しかし、SSHの設定変更によってサーバーへ接続できなくなるトラブルが発生し、一度環境を作り直すことになりました。その後、より実践的なクラウド環境で学習を進めるため、AWS EC2へ移行し、現在のシステムを再構築しました。

構築の過程では、nginx・Docker・Flask・PostgreSQL・GitHub Actions・Discord通知などを一つずつ組み上げました。また、学習用環境ではALBやAuto Scaling Groupを用いた高可用性構成の検証も行いました。

その中で、nginxの設定ミス、Dockerのビルドエラー、GitHub Actionsの認証エラー、ALBの503エラー、Target GroupのUnused・Unhealthy状態など、多くの問題に直面しました。しかし、ログやHealth Checkの状態を確認し、Security Group・Target Group・アプリケーション設定を一つずつ切り分けながら原因を特定し、試行錯誤を重ねて解決しました。

この経験を通して、インフラでは「壊れないように作る」だけでなく、「障害発生時に原因を切り分け、再構築・復旧できる力」が重要であることを実践的に学びました。

---

## 今後の展望

- Amazon RDSを利用したDBの分離
- ALB + HTTPS + 独自ドメイン構成への発展
- Dockerコンテナを利用したAuto Scaling環境の構築
- Infrastructure as Code（IaC）の導入
- 監視・ログ分析機能のさらなる強化
