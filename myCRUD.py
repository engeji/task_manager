import os
import ydb

def execute_query(session):
    return session.transaction().execute(
        "select 1 as cnt;",
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
    )


def main():
    driver = ydb.Driver(
        endpoint='grpcs://ydb.serverless.yandexcloud.net:2135',
        database='/ru-central1/b1gbbtlcp64e95l4e296/etndsqtir7ubim98r45t',
        credentials=ydb.AnonymousCredentials(),
    )

    with driver:
        # wait until driver become initialized
        driver.wait(fail_fast=True, timeout=5)
        with ydb.SessionPool(driver) as pool:
            result = pool.retry_operation_sync(execute_query)
            assert result[0].rows[0].cnt == 1

main()
