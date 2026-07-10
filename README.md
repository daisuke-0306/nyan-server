# 🐱 にゃん.jp - AWS Infrastructure Portfolio

> AWS上に構築したインフラポートフォリオです。  
> Docker・Flask・PostgreSQLを利用したWebシステムをAWS上で公開し、
> CloudFront・Application Load Balancer・CloudWatch・Lambdaを組み合わせた
> 本番運用を想定した構成を構築しています。

---

## 🌐 Public Website

**Production**

https://にゃん.jp

---

## 📊 Current Status

| Item | Status |
|------|--------|
| 🟢 Service | Online |
| ☁️ CloudFront | Enabled |
| ⚖️ Application Load Balancer | Enabled |
| 🔒 HTTPS | Enabled |
| 🐳 Docker | Running |
| 🚀 GitHub Actions | Enabled |
| 🧪 pytest | Enabled |
| 📈 CloudWatch Monitoring | Enabled |
| 📣 Discord Alert | Enabled |

---

# 📖 Overview

本プロジェクトは、AWSを利用したインフラ構築・運用を学ぶことを目的として作成したポートフォリオです。

単にWebサイトを公開するだけではなく、

- 可用性
- 保守性
- 運用性
- 監視
- 自動化

まで考慮した構成を目標に設計・構築しています。

現在はEC2上でDockerコンテナを利用し、

- nginx
- Flask
- PostgreSQL

によるWebシステムを公開しています。

さらに、本番環境ではCloudFront・Application Load Balancerを利用し、CloudWatch・SNS・Lambda・Discordを組み合わせた監視基盤を構築しています。

また、学習環境ではApplication Load Balancer・Target Group・Launch Template・Auto Scaling Groupを利用した高可用性構成を検証しています。

---

# 🎯 Project Goals

本プロジェクトでは以下を目標として構築しています。

- AWSを利用した実践的なインフラ構築
- Dockerを利用した環境の再現性
- GitHub ActionsによるCI/CD
- CloudFrontによるCDN配信
- ALBによる負荷分散
- CloudWatchによる監視
- Lambdaを利用したイベント駆動処理
- Discordへの障害通知
- Auto Scalingによる高可用性構成の学習

---

# 🏗 Production Architecture

```text
                           User
                            │
                     HTTPS (443)
                            │
                            ▼
                 Amazon CloudFront
                            │
                     HTTP (Origin)
                            │
                            ▼
            Application Load Balancer
                            │
                            ▼
                    Target Group
                            │
                            ▼
                      Amazon EC2
                            │
                    Docker Compose
          ┌────────────┼────────────┐
          │            │            │
       nginx        Flask      PostgreSQL
```
---

# ☁️ AWS Design

本番環境では、単にAWSサービスを利用するだけではなく、「なぜそのサービスを採用したのか」を意識して設計しています。

---

# ☁️ Amazon CloudFront

## Purpose

公開サイトのレスポンス速度向上と、EC2へのリクエスト数削減を目的としてCloudFrontを導入しました。

CloudFrontは世界中のエッジロケーションへ静的コンテンツをキャッシュすることで、日本からAWS Sydneyリージョンへ毎回アクセスする必要がなくなり、ページ表示を高速化できます。

---

## Design

CloudFrontのOriginにはEC2を直接指定せず、Application Load Balancerを設定しています。

これにより、

- EC2の増減時にCloudFront側の設定変更が不要
- 将来的なAuto Scalingへの対応
- 負荷分散をALBへ委任

できる構成としています。

---

## Cache Behavior

| Path Pattern | Cache Policy | Purpose |
|---------------|--------------|----------|
| `Default (*)` | `CachingOptimized` | HTML・CSS・JavaScript・画像などの静的コンテンツ |
| `/api/*` | `CachingDisabled` | CPU使用率などリアルタイムデータ |

CPU使用率などのAPIは約5秒ごとに値が更新されます。

そのためCloudFrontには古いデータを保持させないよう、`/api/*`のみキャッシュを無効化しています。

静的コンテンツのみをCloudFrontから配信し、リアルタイムデータのみEC2から取得する構成としています。

---

## Troubleshooting

CloudFront導入直後、CloudFront経由のアクセスで **504 Gateway Timeout** が発生しました。

原因は、

CloudFront

↓

HTTPS

↓

ALB

という設定になっていた一方で、

ALBにはHTTPリスナーしか設定されていなかったことでした。

Origin Protocol Policyを **HTTP Only** へ変更し、

CloudFront → ALB

間の通信方式を統一することで問題を解決しました。

この経験から、

CloudFrontだけではなく、Origin側との通信方式も一致させる必要があることを学びました。

---

# ⚖️ Application Load Balancer

CloudFrontのオリジンとしてApplication Load Balancerを配置しています。

---

## Purpose

Application Load Balancerを利用することで、

- EC2へのリクエスト分散
- 将来的な複数EC2への対応
- Health Checkによる正常インスタンスへの振り分け

を実現しています。

現在はEC2を1台で運用していますが、Auto Scaling Groupと組み合わせることで、インスタンスが増減してもCloudFront側の設定変更なしで運用できる構成となっています。

---

## Health Check

Target Groupでは以下のHealth Checkを設定しています。

| Item | Value |
|------|-------|
| Protocol | HTTP |
| Port | 80 |
| Path | `/health` |

Flaskアプリケーションではデータベース接続も確認し、

- Server : OK
- Database : OK

を返すHealth Checkページを実装しています。

これによりWebサーバーだけではなく、DB接続状態まで確認できるようにしています。

---

## Learned

Application Load Balancerは単なる負荷分散装置ではなく、

- 高可用性
- 障害検知
- Auto Scalingとの連携

を実現する重要なサービスであることを学びました。

---

# 📈 Monitoring

本番環境ではCloudWatchを利用してEC2を監視しています。

CPU使用率はCloudWatch APIから取得し、Chart.jsを利用してWeb画面上へリアルタイム表示しています。

約5秒ごとに更新することで、EC2の負荷状況をブラウザから確認できます。

---

# 🚨 CloudWatch Alarm

CloudWatch Alarmを利用し、

EC2 CPUUtilization

を継続的に監視しています。

設定したしきい値を超えると、自動的にAlarm状態へ変更されます。

監視を自動化することで、異常発生時に人が常時監視する必要がない構成を実現しています。

---

# 📨 Amazon SNS

CloudWatch Alarmの通知先としてAmazon SNSを利用しています。

CloudWatch AlarmがAlarm状態になると、

SNS Topic

へイベントが送信されます。

SNSを経由することで、Lambdaだけではなく、メールや他サービスへの通知にも拡張できる構成としています。

---

# ⚡ AWS Lambda

SNSから送信されたイベントを受信すると、AWS Lambdaが自動で実行されます。

LambdaではPythonを利用し、

Discord Webhook

へHTTP POSTを送信しています。

サーバーを常時起動することなく、イベント発生時のみ処理を実行できるため、運用コストを抑えられる構成となっています。

---

## Notification Flow

```text
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
        │
        ▼
Discord Channel
```

---

## Learned

Lambdaを利用することで、

イベントが発生した時だけプログラムを実行する

という**イベント駆動アーキテクチャ**を学びました。

従来のようにサーバーを常時起動する必要がなく、

必要な時だけ処理を実行できることがLambdaの大きな特徴です。

---

# 🚀 CI / CD

GitHub Actionsを利用し、自動テスト・自動デプロイ環境を構築しています。

コードをGitHubへPushすると、

```text
Developer
      │
      ▼
 Git Push
      │
      ▼
GitHub Actions
      │
      ▼
pytest
      │
      ▼
Deploy
      │
      ▼
Production
```

という流れで自動実行されます。

pytestが失敗した場合はデプロイされないため、

品質を維持したまま本番環境へ反映できる構成となっています。

---

## Benefits

- デプロイ作業の自動化
- 人的ミスの削減
- テストによる品質担保
- 継続的インテグレーション（CI）
- 継続的デリバリー（CD）

---

# 🧪 AWS High Availability Lab

本番環境とは別に、AWS上へ学習用環境を構築し、高可用性（High Availability）とSelf Healingを検証しました。

本番環境へ影響を与えない環境で、AWSが提供する可用性向上の仕組みを実際に構築・検証しています。

---

## Architecture

```text
                 Internet
                     │
                     ▼
        Application Load Balancer
                     │
              Target Group
                     │
         Auto Scaling Group (ASG)
             ┌──────────────┐
             ▼              ▼
      EC2 (AZ-A)      EC2 (AZ-B)
```

---

## Implemented

- Launch Template作成
- EC2インスタンスを2台構築
- Application Load Balancer設定
- Target Group設定
- Health Check設定
- Auto Scaling Group構築
- Availability Zoneを跨いだ配置
- EC2をTerminateしSelf Healingを検証

---

## Verification

以下の内容を実際に確認しました。

### Load Balancing

ALB経由でアクセスし、Target Groupへ正常にリクエストが振り分けられることを確認しました。

---

### Health Check

`/health`

をHealth Checkとして設定し、

異常なインスタンスはTarget Groupから切り離されることを確認しました。

---

### Self Healing

Auto Scaling Group配下のEC2インスタンスを意図的にTerminateし、

Desired Capacityを維持するために新しいEC2インスタンスが自動生成されることを確認しました。

---

## Learned

この検証を通して、

クラウドでは

**「サーバーを修理する」**

のではなく、

**「新しいサーバーを自動生成する」**

という考え方で設計されていることを学びました。

また、

障害発生を前提として設計することがクラウドインフラでは重要であることを理解しました。

---

# ⚠ Troubleshooting

本プロジェクトでは多数の障害を経験し、その都度原因を切り分けながら解決しました。

---

## CloudFront

### Issue

CloudFront経由でアクセスすると

```
504 Gateway Timeout
```

が発生しました。

### Cause

CloudFrontのOrigin Protocol PolicyがHTTPSになっていた一方、

Application Load BalancerはHTTPのみを受け付ける設定になっていました。

### Solution

Origin Protocol Policyを

```
HTTP Only
```

へ変更し、

CloudFront→ALB間の通信方式を統一することで解決しました。

---

## Application Load Balancer

### Issue

Target Groupが

```
Unused
```

または

```
Unhealthy
```

となり、

ALBからアクセスできませんでした。

### Cause

- Target Group未登録
- Security Group設定
- Health Check設定

に問題がありました。

### Solution

Target GroupへEC2を登録し、

Security GroupとHealth Check設定を修正することで解決しました。

---

## AWS Lambda

### Issue

Discord通知が失敗し、

```
HTTP 403 Forbidden
```

が発生しました。

### Cause

Webhook URLの設定ミスと環境変数の設定に問題がありました。

### Solution

環境変数を利用してWebhook URLを管理し、

Pythonコードを修正することで正常にDiscordへ通知できるようになりました。

---

## GitHub Actions

### Issue

GitHub Actionsが正常に実行されませんでした。

### Cause

Secrets設定や認証情報に誤りがありました。

### Solution

GitHub Secretsを見直し、

認証情報を修正することでCI/CDを復旧しました。

---

# 💡 Lessons Learned

このプロジェクトでは、

単にAWSサービスを利用するだけではなく、

実際に構築・障害対応・改善を繰り返しながら理解を深めました。

特に、

- CloudFront
- Application Load Balancer
- CloudWatch
- SNS
- Lambda
- GitHub Actions

は、

ドキュメントを読むだけではなく、

実際にエラーへ遭遇し、

ログやAWSコンソールを確認しながら原因を特定・解決しました。

この経験を通して、

インフラエンジニアには

「壊れないシステムを作る」

だけではなく、

「障害発生時に原因を切り分け、復旧できる力」

が重要であることを学びました。

---

# 🚀 Future Roadmap

今後はさらにAWSを活用し、

より実践的なクラウドアーキテクチャを構築していきます。

## Infrastructure

- Amazon RDS
- Amazon ECS
- Amazon ECR
- AWS WAF
- AWS CloudWatch Logs

---

## IaC

- Terraform

---

## CI/CD

- Blue / Green Deployment
- Rolling Update

---

## Monitoring

- CloudWatch Logs
- メトリクスの可視化強化
- ログ分析の自動化

---

## Security

- AWS WAF導入
- IAM権限の最小化
- Security Group最適化

---

# 🙌 Conclusion

このポートフォリオでは、

Linux・Docker・Webアプリケーション開発から始まり、

AWSを利用した監視・負荷分散・CDN・イベント駆動アーキテクチャ・CI/CDまで段階的に構築しました。

今後も実際に手を動かしながら学習を継続し、

設計・構築・運用まで一貫して対応できるクラウドエンジニアを目指します。
