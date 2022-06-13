import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

@pytest.fixture
def jool_instances(host):
    return host.ansible.get_variables().get("jool_instances")


@pytest.mark.parametrize("package_name", ["jool-dkms", "jool-tools"])
def test_jool_packages(host, package_name):
    """Jool packages are installed."""
    package = host.package(package_name)
    assert package.is_installed


def test_jool_configuration_directory(host):
    """Jool configuration directory exists with correct permissions."""
    directory = host.file("/etc/jool")
    assert directory.is_directory
    assert directory.user == "root"
    assert directory.group == "root"
    assert directory.mode == 0o755


def test_jool_main_systemd_service(host):
    """Jool main Systemd service is running and enabled."""
    main_service = host.service("jool.service")
    assert main_service.is_running
    assert main_service.is_enabled


def test_jool_siit_systemd_service_masked(host):
    """Jool SIIT Systemd service included with package is not running and masked."""
    package_siit_service = host.service("jool_siit.service")
    assert not package_siit_service.is_running
    assert package_siit_service.is_masked


def test_jool_systemd_instance_services(host, jool_instances):
    """Jool instance Systemd services are running."""
    service_names = ["jool." + i.get("instance") + ".service" for i in jool_instances]
    for service in service_names:
        instance_service = host.service(service)
        assert instance_service.is_running
