import invoke
import logging
import os
import boto3

logger = logging.getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)


def invoke_run(command):
    logging.info(command)
    invoke.run(command, pty=True)


def get_aws_account_info():
    # セッションを作成
    session = boto3.session.Session()

    # STSクライアントを使用してアカウントIDを取得
    sts_client = session.client("sts")
    account_id = sts_client.get_caller_identity()["Account"]

    # セッションからリージョン名を取得
    region = session.region_name

    return account_id, region


@invoke.task
def env(c):
    invoke_run("python3 -m venv .venv")
    print("source .venv/bin/activate.fish")


@invoke.task
def install(c):
    invoke_run("pip install -r requirements.txt -r requirements-dev.txt")


# CDK
@invoke.task
def diff(c):
    invoke_run("cdk diff")


@invoke.task
def deploy(c):
    invoke_run("cdk deploy --require-approval never")


@invoke.task
def hotswap(c):
    invoke_run("cdk deploy --require-approval never --hotswap")



@invoke.task
def test(c):
    invoke_run("pytest -v")


@invoke.task
def test_unit(c):
    invoke_run("pytest -v tests/unit")

@invoke.task
def front(c):
    logging.info("start frontend")
    invoke_run(
        "streamlit run frontend/app.py --logger.level=debug",
    )
    logging.info("finish")
