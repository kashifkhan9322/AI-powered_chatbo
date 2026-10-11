# Deployment Guide

**This project is not deployed to AWS automatically.** Choose a route and review current costs before creating resources.

## Docker local run
```bash
docker compose up --build
```
Visit `http://localhost:8080`. Stop with `docker compose down`.

## AWS Elastic Beanstalk (portfolio path)
1. Secure your AWS account with MFA and billing alerts.
2. Create a Python environment in a suitable region.
3. Package the application files and deploy to a test environment.
4. Configure the platform to use a production WSGI server and its expected port conventions.
5. Configure HTTPS and a custom domain if needed.
6. Enable CloudWatch logs, health monitoring, alarms, and a cost budget.
7. Test health, valid chat messages, invalid requests, and mobile layout after deployment.
8. Delete unused resources after the demonstration if you do not need them.

## Container architecture (advanced)
```text
Visitors -> Route 53 (optional) -> HTTPS Load Balancer
         -> ECS Fargate service (container: Flask + Waitress)
         -> intents.json / approved knowledge source
         -> CloudWatch logs, metrics, alarms
```
Use least-privilege IAM, keep internal services private, and store any future secrets in Secrets Manager or Parameter Store. The static UI can alternatively be hosted separately behind CloudFront.

## Production checklist
- Replace sample business hours, prices, policy, and contact responses.
- Use HTTPS and a production WSGI server.
- Add rate limiting and abuse protection.
- Configure privacy-conscious logs, alerts, and a retention policy.
- Load-test, validate rollback, and review accessibility.
- Set AWS billing alerts and a budget. Cost varies by region, compute size, traffic, logging, and data transfer.
