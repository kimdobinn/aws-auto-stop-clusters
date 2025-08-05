# Architecture Overview

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   EventBridge   │───▶│  Lambda Function │───▶│   RDS/DocDB     │
│   Scheduler     │    │                 │    │   Clusters      │
│  (Weekly Cron)  │    │ auto_stop_      │    │                 │
└─────────────────┘    │ clusters.py     │    └─────────────────┘
                       └─────────────────┘              │
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   CloudWatch    │    │   Cost Savings  │
                       │     Logs        │    │   Analytics     │
                       └─────────────────┘    └─────────────────┘
```

## Data Flow

1. **EventBridge Scheduler** triggers Lambda function weekly
2. **Lambda Function** queries RDS/DocumentDB clusters
3. **Start Phase**: Starts stopped clusters to allow AWS auto-reboot
4. **Wait Phase**: Monitors cluster status until all are available
5. **Stop Phase**: Immediately stops all clusters after reboot
6. **Logging**: All actions logged to CloudWatch for monitoring

## Security Model

- **Principle of Least Privilege**: IAM policies grant minimal required permissions
- **Resource-based Access**: Policies scoped to specific RDS/DocumentDB operations
- **Cross-service Trust**: EventBridge trusted to invoke Lambda via IAM roles

## Cost Optimization Strategy

- **Automated Management**: Eliminates manual intervention
- **Predictive Scheduling**: Runs before AWS auto-restart cycles
- **Selective Targeting**: Configurable cluster exclusion list
- **Monitoring**: CloudWatch logs enable cost tracking
