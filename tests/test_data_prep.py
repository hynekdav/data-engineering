from pathlib import Path

from dagster import ExecuteInProcessResult

from data_prep import all_assets, all_assets_job


def test_job():
    job = all_assets_job.resolve(assets=all_assets, source_assets=[])
    result = job.execute_in_process()

    # return type is ExecuteInProcessResult
    assert isinstance(result, ExecuteInProcessResult)
    assert result.success
    assert Path("/tmp/criminality.pqt").exists()
