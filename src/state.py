import json
import os

import boto3
from loguru import logger

from src.config import aws_key, aws_region, aws_secret, cfg
from src.utils import PATH


class State:
    def __init__(self) -> None:
        self.use_dynamodb = bool(aws_key and aws_secret)
        self.local_file = PATH.state

        if self.use_dynamodb:
            endpoint = os.getenv("AWS_ENDPOINT_URL")
            self.client = boto3.client(
                "dynamodb",
                aws_access_key_id=aws_key,
                aws_secret_access_key=aws_secret,
                region_name=aws_region,
                endpoint_url=endpoint if endpoint else None,
            )
            self.table = cfg.state.dynamodb_table
            self.key = cfg.state.last_tweet_key
            logger.info("using dynamodb for state")
        else:
            logger.info(f"using local file for state: {self.local_file}")

    def get_last_id(self) -> str | None:
        if self.use_dynamodb:
            return self._get_from_dynamodb()
        return self._get_from_file()

    def set_last_id(self, tweet_id: str) -> None:
        if self.use_dynamodb:
            self._set_to_dynamodb(tweet_id)
        else:
            self._set_to_file(tweet_id)

    def _get_from_dynamodb(self) -> str | None:
        try:
            resp = self.client.get_item(TableName=self.table, Key={"id": {"S": self.key}})
            if "Item" in resp and "value" in resp["Item"]:
                value = resp["Item"]["value"]["S"]
                return str(value) if value else None
            return None
        except Exception as e:
            logger.error(f"get_last_id from dynamodb failed: {e}")
            return None

    def _set_to_dynamodb(self, tweet_id: str) -> None:
        try:
            self.client.put_item(
                TableName=self.table,
                Item={"id": {"S": self.key}, "value": {"S": tweet_id}},
            )
            logger.info(f"set_last_id to dynamodb: {tweet_id}")
        except Exception as e:
            logger.error(f"set_last_id to dynamodb failed: {e}")

    def _get_from_file(self) -> str | None:
        try:
            if not self.local_file.exists():
                return None
            with open(self.local_file) as f:
                data: dict[str, str] = json.load(f)
                value = data.get("last_tweet_id")
                return str(value) if value else None
        except Exception as e:
            logger.error(f"get_last_id from file failed: {e}")
            return None

    def _set_to_file(self, tweet_id: str) -> None:
        try:
            with open(self.local_file, "w") as f:
                json.dump({"last_tweet_id": tweet_id}, f)
            logger.info(f"set_last_id to file: {tweet_id}")
        except Exception as e:
            logger.error(f"set_last_id to file failed: {e}")
