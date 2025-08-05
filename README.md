# AWS Auto-Stop for RDS & DocumentDB Clusters

This repository documents a cost optimization solution for automatically stopping Aurora RDS and DocumentDB clusters that reboot every two weeks on their own. It uses AWS EventBridge Scheduler and a Lambda function to detect and shut down unnecessary clusters without human intervention.

---

## Problem Statement

RDS and DocumentDB clusters incur unnecessary costs when left running. Even after manual shutdown, AWS automatically restarts them every 7 or 14 days. Manually shutting them down again is inefficient and error-prone.

---

## Solution

- Create an AWS Lambda function that:
  - Identifies Aurora RDS and DocumentDB clusters (excluding protected ones).
  - Starts clusters to allow AWS to complete its automatic reboot.
  - Waits until all clusters are available.
  - Then immediately shuts them down again.

- Schedule the Lambda function to run **every 7 days** using **EventBridge Scheduler**.

---

## AWS Services Used

- **AWS Lambda**: Core logic to check, start, wait, and stop clusters.
- **Amazon RDS & DocumentDB**: The managed database services being targeted.
- **Amazon EventBridge Scheduler**: Triggers the Lambda weekly.
- **AWS IAM**: Manages fine-grained roles and policies for secure execution.
- **CloudWatch Logs**: Monitors and debugs Lambda execution.

```text
aws-auto-stop-clusters/
├── lambda/
│   └── auto_stop_clusters.py                  # Main Lambda function
├── eventbridge/
│   └── scheduler_config.json                  # JSON export of EventBridge Scheduler config
├── iam/
│   ├── EventBridgeSchedulerExecutionPolicy.json
│   ├── LambdaInvokePolicy.json
│   └── LambdaStopDBPolicy.json
├── terraform/
│   ├── eventbridge_schedule.tf
│   └── trust_relationships/
│       ├── EventBridgeTrustPolicy.json
│       └── LambdaTrustPolicy.json
├── .gitignore
└── README.md
```

## Notes

- Region: `ap-southeast-2`
- Timezone: `Asia/Singapore`
- Cluster exclusions are configurable inside the script.
- Logs can be monitored in **CloudWatch > Log groups > /aws/lambda/AutoStopClusters**

---

## Testing

To simulate/test locally:
```bash
aws lambda invoke --function-name AutoStopClusters out.json
```

---

## Author

@kimdobinn
