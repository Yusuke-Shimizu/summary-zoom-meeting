import invoke
import logging
import os

logger = logging.getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)


def invoke_run(command):
    logging.info(command)
    invoke.run(command, pty=True)


@invoke.task
def env(c):
    invoke_run("python3 -m venv .venv")
    print("source .venv/bin/activate.fish")


@invoke.task
def install(c):
    invoke_run(
        "pip install -r requirements.txt -r requirements-dev.txt -r frontend/requirements.txt"
    )


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
