import testinfra.utils.ansible_runner
import pytest

@pytest.fixture
def __ansible_vars(host):
    """
    Testinfra does not expose or resolve role and inventory variables natively,
    so this fixture returns a dictionary containing the role and inventory variables.
    """
    role_default = host.ansible("include_vars","./defaults/main.yml")["ansible_facts"]
    role_var = host.ansible("include_vars","./vars/main.yml")["ansible_facts"]
    inventory = {}
    ## // inventory variables that should be resolved need to be defined here
    inventory_vars_to_resolve = [
        "jool_instances",
    ]
    if inventory_vars_to_resolve != []:
        for var_name in inventory_vars_to_resolve:
            var_content = host.ansible("ansible.builtin.debug", f"var={var_name}")[var_name]
            inventory[var_name] = var_content
    ansible_vars_dict = { "role_default": role_default, "role_var": role_var, "inventory": inventory }
    return ansible_vars_dict
