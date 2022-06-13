# initq.jool

## ![jool](img/jool.png)

This role will install and configure [Jool](https://www.jool.mx), an Open Source IPv4/IPv6 Translator, funded by NIC Mexico and co-developed with ITESM.

## Role Variables

| Variable       | Required | Default | Input                                                                    | Comments                                                                                                                                                                                                      |
| -------------- | -------- | ------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| jool_instances | **yes**  | _null_  | [`[]`](https://developers.google.com/protocol-buffers/docs/proto#scalar) | A list of dictionaries containing [Jool instance configuration](https://www.jool.mx/en/config-atomic.html) in YAML format, with an additionally required `type` key that can be set to `"nat64"` or `"siit"`. |

## Usage

For each Jool instance, a Systemd service will be created that can be managed with the service name `"jool.<instance-name>.service"`.
To manage all Jool instances at once, the master service `"jool.service"` can be used.

## Requirements

This role is tested with the following, but may also work in other environments:

- Rsync
- Ubuntu
  - 20.04 LTS (Focal Fossa)

## Known Issues

- The `pool6` argument of an existing NAT64 instance cannot be changed while it is active and doing so will result in an error.

## Example Playbook

```yaml
- hosts: aftrs
  roles:
    - initq.jool
  vars:
    jool_instances:
      - instance: nat64-minimal
        type: nat64
        framework: netfilter
        global:
          pool6: "64:ff9b::/96"
```

## License

[GNU General Public License v3.0](./LICENSE)

## Author Information

Marvin Vogt (git@srv6d.space)
