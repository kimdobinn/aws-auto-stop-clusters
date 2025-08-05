resource "aws_scheduler_schedule" "weekly_cluster_reboot" {
  name        = "WeeklyClusterReboot"
  group_name  = "default"
  schedule_expression   = "rate(7 days)"
  schedule_expression_timezone = "Asia/Singapore"
  #start_time = "2025-07-13T00:00:00Z"

  flexible_time_window {
    mode = "OFF"
  }

  state = "ENABLED"

  target {
    arn      = "arn:aws:lambda:ap-southeast-2:xxxxxxxxxxxx:function:AutoStopClusters"
    role_arn = "arn:aws:iam::xxxxxxxxxxxx:role/Amazon_EventBridge_Scheduler_LAMBDA_AutoStopClusters"
  }
}
