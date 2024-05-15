$env:WAREHOUSE_CONFIGURATION_FILE_PATH='tests\test_config.yaml'
$env:PYTHONPATH=Get-Location
pytest --cov ./src/sim