# にゃん.jp - Infrastructure Portfolio

## 概要
AWS EC2上にDocker・nginx・PostgreSQL・Flaskを用いた
Webサーバーを構築し、GitHub Actionsによる自動デプロイ環境を構築しました。

## 構成
- AWS EC2（Ubuntu）
- nginx（リバースプロキシ）
- Docker / Docker Compose
- Flask（アプリケーション）
- PostgreSQL（データベース）
- GitHub Actions（CI/CD）
- Let's Encrypt（HTTPS）

## 機能
- Webサーバー公開（HTTPS対応）
- Dockerによるコンテナ構成
- DB連携（Flask + PostgreSQL）
- 自動デプロイ（pushで更新）
- ステータスページ（/status）
- DB確認ページ（/read）

## アーキテクチャ

```text
[User]
  ↓
nginx
  ↓
Docker（web）
  ↓
Flask（app）
  ↓
PostgreSQL（db）

## こだわった点
- Dockerで環境を分離し再現性を確保
- GitHub Actionsでデプロイを自動化
- UIを整え「見せる」構成にした

## URL
https://にゃん.jp
