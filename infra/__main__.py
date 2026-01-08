import json

import pulumi
import pulumi_aws as aws

cfg = pulumi.Config()
twitter_session = cfg.require_secret("twitter_session")
discord_webhook = cfg.require_secret("discord_webhook")

table = aws.dynamodb.Table(
    "yura-bot-state",
    name="yura-bot-state",
    billing_mode="PAY_PER_REQUEST",
    hash_key="id",
    attributes=[{"name": "id", "type": "S"}],
    tags={"Project": "yura-bot"},
)

role = aws.iam.Role(
    "yura-bot-lambda-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Effect": "Allow",
                }
            ],
        }
    ),
)

aws.iam.RolePolicyAttachment(
    "yura-bot-lambda-basic",
    role=role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
)

dynamodb_policy = aws.iam.RolePolicy(
    "yura-bot-dynamodb-policy",
    role=role.id,
    policy=table.arn.apply(
        lambda arn: json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "dynamodb:GetItem",
                            "dynamodb:PutItem",
                            "dynamodb:UpdateItem",
                        ],
                        "Resource": arn,
                    }
                ],
            }
        )
    ),
)

func = aws.lambda_.Function(
    "yura-bot",
    name="yura-bot",
    runtime="python3.11",
    handler="src.handler.handler",
    role=role.arn,
    code=pulumi.FileArchive("../lambda_package.zip"),
    timeout=300,
    memory_size=512,
    environment={
        "variables": {
            "TWITTER_SESSION": twitter_session,
            "DISCORD_WEBHOOK_URL": discord_webhook,
            "AWS_REGION": "us-east-1",
        }
    },
    tags={"Project": "yura-bot"},
)

rule = aws.cloudwatch.EventRule(
    "yura-bot-schedule",
    name="yura-bot-schedule",
    schedule_expression="rate(1 hour)",
    tags={"Project": "yura-bot"},
)

aws.lambda_.Permission(
    "yura-bot-eventbridge-permission",
    action="lambda:InvokeFunction",
    function=func.name,
    principal="events.amazonaws.com",
    source_arn=rule.arn,
)

aws.cloudwatch.EventTarget(
    "yura-bot-target",
    rule=rule.name,
    arn=func.arn,
)

pulumi.export("lambda_function_name", func.name)
pulumi.export("dynamodb_table_name", table.name)
pulumi.export("eventbridge_rule_name", rule.name)
