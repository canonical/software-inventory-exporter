"""CLI unit tests."""
import pytest
import yaml

from software_inventory_exporter import cli


def test_main(tmp_path, mocker):
    """Test the main function."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("settings:\n  bind_address: 0.0.0.0\n  port: 8675")
    uvicorn_mock = mocker.patch.object(cli.uvicorn, "run")
    cli.main([str(config_file)])
    uvicorn_mock.assert_called_once()


@pytest.mark.parametrize(
    "error", [(True, False, False), (False, True, False), (False, False, True)]
)
def test_main_exit(mocker, tmp_path, error):
    """Test the main function when exit."""
    file_error, key_error, yaml_error = error
    config_file = tmp_path / "config.yaml"
    uvicorn_mock = mocker.patch.object(cli.uvicorn, "run")
    if file_error:
        with pytest.raises(SystemExit) as mock_exception:
            cli.main(["/tmp/config.yaml"])
    elif key_error:
        config_file.write_text("settings:\n  port: 8675")
        with pytest.raises(SystemExit) as mock_exception:
            cli.main([str(config_file)])
    elif yaml_error:
        mocker.patch.object(cli.yaml, "safe_load", side_effect=yaml.YAMLError)
        config_file.write_text("settings:\n  bind_address: 0.0.0.0\n  port: 8675")
        with pytest.raises(SystemExit) as mock_exception:
            cli.main([str(config_file)])
    assert mock_exception.value.code == 1
    uvicorn_mock.assert_not_called()
