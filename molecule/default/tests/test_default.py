import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

@pytest.mark.parametrize("package_name", ["jool-dkms", "jool-tools"])
def test_jool_packages(host, package_name):
    package = host.package(package_name)
    assert package.is_installed

@pytest.mark.parametrize("directory_path", ["/etc/jool", "/etc/jool/service-environment", "/etc/jool/instances"])
def test_jool_configuration_directories(host, directory_path):
    directory = host.file(directory_path)
    assert directory.is_directory
    assert directory.user == "root"
    assert directory.group == "root"
    assert directory.mode == 0o755

def test_jool_systemd_service(host):
    main_service = host.service("jool.service")
    template_service = host.service("jool@.service")
    package_siit_service = host.service("jool_siit.service")
    assert main_service.is_running
    assert main_service.is_enabled
    assert package_siit_service.is_masked
