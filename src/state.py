import boto3
from loguru import logger

from src.config import aws_key, aws_region, aws_secret, cfg


class State:
    def __init__(self) -> None:
        self.client = boto3.client(
            "dynamodb",
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region,
        )
        self.table = cfg.state.dynamodb_table
        self.key = cfg.state.last_tweet_key

    def get_last_id(self) -> str | None:
        try:
            resp = self.client.get_item(TableName=self.table, Key={"id": {"S": self.key}})
            if "Item" in resp and "value" in resp["Item"]:
                value = resp["Item"]["value"]["S"]
                return str(value) if value else None
            return None
        except Exception as e:
            logger.error(f"get_last_id failed: {e}")
            return None

    def set_last_id(self, tweet_id: str) -> None:
        try:
            self.client.put_item(
                TableName=self.table,
                Item={"id": {"S": self.key}, "value": {"S": tweet_id}},
            )
            logger.info(f"set_last_id: {tweet_id}")
        except Exception as e:
            logger.error(f"set_last_id failed: {e}")
