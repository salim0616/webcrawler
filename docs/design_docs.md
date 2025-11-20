# System Design for Billions of URLs

## 1. URL Ingestion
- Source: URLs provided in a text file or MySQL database for a given month.
- Ingestion Service: Script or service (Lambda, ECS, EC2) reads URLs and pushes to a message queue (SQS or Kafka). Prefer SQS for simplicity/scalability.
- Batching: Batch URLs (e.g., 10,000 per message) to reduce queue message volume.

## 2. Message Queue
- Use AWS SQS (or Kafka for advanced needs) to store URLs.
- SQS provides at-least-once delivery and scales.
- Option: multiple SQS queues for different priorities or domains.

## 3. Distributed Crawler Workers
- Worker nodes: Run multiple crawler instances (from Part 1) distributed via ECS or Kubernetes.
- Autoscaling: Scale workers based on SQS queue depth.
- Rate limiting: Respect robots.txt and add per-domain delays.
- Retries: Exponential backoff for failures; repeated failures → dead-letter queue (DLQ).

## 4. Content Processing
- Workers fetch HTML, extract metadata, and classify topics (hybrid classifier from Part 1).
- Store raw HTML in S3 for future use.

## 5. Storage
- Metadata: Amazon DynamoDB for scale (query by URL hash). Optionally Amazon Aurora for SQL needs.
- Raw HTML: Amazon S3 with lifecycle policy → Glacier after 30 days.

## 6. Monitoring and Alerting
- Metrics: CloudWatch for SQS depth, crawler count, HTTP success rates, storage metrics.
- Logging: Structured JSON logs in CloudWatch Logs or Elasticsearch.
- Alerting: CloudWatch Alarms for high error rates, queue age, system failures.

## 7. SLOs and SLAs
- Availability: 99.9% for crawling service.
- Freshness: 95% of URLs crawled within 24 hours of queuing.
- Durability: 99.999% for stored data (S3, DynamoDB).
- Accuracy: Topic classification accuracy 90% (measured on labeled set).

## 8. Cost Optimization
- Use spot instances for crawler workers.
- Use S3 Intelligent Tiering.
- Use DynamoDB auto-scaling.

## 9. Reliability
- Deploy across multiple availability zones.
- Implement circuit breakers in crawler to avoid overloading target sites.

## 10. Performance and Scale
- Horizontally scalable distributed architecture.
- Connection pooling and HTTP keep-alive to reduce TCP overhead.

## Next Steps
- Implement distributed crawler based on Part 1, adapted for distributed env.
- Provision SQS, DynamoDB, S3 using Terraform or CloudFormation.
- Deploy ingestion service and crawler workers on ECS or Kubernetes.
- Set up monitoring and alerting.
- Test with small URL set, then scale.

## Monitoring Metrics (Key)
- crawler_requests_total (with status code)
- crawler_duration_seconds
- urls_processed_total
- urls_failed_total
- queue_messages_visible (SQS)

## Tools
- Amazon CloudWatch
- Prometheus (if using Kubernetes)
- Grafana for dashboards

