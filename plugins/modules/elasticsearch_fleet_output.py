#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
from kibana.kibana import kibana

DOCUMENTATION = """
---
module: elasticsearch_fleet_output
short_description: Manage Fleet outputs
description:
    - This module allows you to manage Fleet output.
    - It can create a new output, delete it, or update it

author: Linus

options:
  state:
    description:
      - Specifies whether the user should be present or absent.
    choices: ['present', 'absent', 'update']
    required: true

  kb_url:
    description:
      - URL of the Elasticsearch cluster.
    required: true

  kb_user:
    description:
      - Elasticsearch username.
    required: true

  kb_pass:
    description:
      - Elasticsearch password.
    required: true
    no_log: true

  output_type:
    description:
      - Which output type you want to create/update. Fallback to elasticsearch if not specified.
    required: false
    choices: ['elasticsearch', 'logstash']

  output_hosts:
    description:
      - List of hosts to send the data to.
    required: true

  output_id:
    description:
      - The output id if you want to set it manually. Otherwise it will be generated.
    required: false

  output_name:
    description:
      - The output name
    required: true
  
  is_default:
    description:
      - Whether this output should be the default output. Default: True
    required: false

  is_default_monitoring:
    description:
      - Whether this output should be the default monitoring output. Default: True
    required: false

  ca_trusted_fingerprint:
    description:
      - The SHA256 fingerprint of the certificate authority's certificate. This is used to verify the certificate presented by the remote host belongs to the expected remote host.
    required: false

  config_yaml:
    description:
      - Additional config in yaml format
    required: false

  agent_policy_name:
    description:
      - The agent policy name you want to get the enrolment key from. Only required to get the enrolment key.
    required: false

  tls_verify:
    description:
      - Whether to verify TLS certificates.
    required: false
    type: bool

notes:
  - This module requires the `python-kibana` Python library to be installed.

requirements:
  - python-kibana

"""


def main():
    module_args = dict(
        kb_url=dict(type="str", required=True),
        kb_user=dict(type="str", required=True),
        kb_pass=dict(type="str", required=True, no_log=True),
        state=dict(type="str", required=True, choices=["present", "absent", "update"]),
        output_type=dict(type="str", required=False),
        output_hosts=dict(type="list", required=True),
        output_id=dict(type="str", required=False),
        output_name=dict(type="str", required=True),
        is_default=dict(type=bool, required=False),
        is_default_monitoring=dict(type=bool, required=False),
        ca_trusted_fingerprint=dict(type="str", required=False),
        config_yaml=dict(type="str", required=False),
        tls_verify=dict(type=bool),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    state = module.params["state"]
    kb_url = module.params["kb_url"]
    kb_user = module.params["kb_user"]
    kb_pass = module.params["kb_pass"]
    state = module.params["state"]
    tls_verify = module.params["tls_verify"]
    output_type = module.params["output_type"]
    output_hosts = module.params["output_hosts"]
    output_id = module.params["output_id"]
    output_name = module.params["output_name"]
    is_default = module.params["is_default"]
    is_default_monitoring = module.params["is_default_monitoring"]
    ca_trusted_fingerprint = module.params["ca_trusted_fingerprint"]
    config_yaml = module.params["config_yaml"]

    if tls_verify == False:
        kb = kibana(
            base_url=kb_url, username=kb_user, password=kb_pass, ssl_verify=False
        )
    else:
        kb = kibana(base_url=kb_url, username=kb_user, password=kb_pass)

    if state == "present":
        if output_name and output_hosts:
            if kb.get_fleet_output(output_name):
                module.exit_json(
                    changed=False, msg=f"Output {output_name} already exists"
                )
            else:
                payload = {
                    "hosts": output_hosts,
                    "output_name": output_name,
                }
                if output_type:
                    payload["type"] = output_type
                if output_id:
                    payload["output_id"] = output_id
                if is_default is not None:
                    payload["is_default"] = is_default
                if is_default_monitoring is not None:
                    payload["is_default_monitoring"] = is_default_monitoring
                if ca_trusted_fingerprint:
                    payload["ca_trusted_fingerprint"] = ca_trusted_fingerprint
                if config_yaml:
                    payload["config_yaml"] = config_yaml
                kb.create_fleet_output(**payload)
                module.exit_json(changed=True, msg=f"Output {output_name} created")
        else:
            module.fail_json(msg="No Output Name or Hosts Specified.")

    if state == "absent":
        if output_name:
            if not kb.get_fleet_output(output_name):
                module.exit_json(
                    changed=False, msg=f"Output {output_name} doesn't exist"
                )
            else:
                kb.delete_fleet_output(output_name=output_name)
                module.exit_json(changed=True, msg=f"Output {output_name} removed")
        else:
            module.fail_json(msg="No Output Name Specified.")

    if state == "update":
        if output_name:
            if not kb.get_fleet_output(output_name):
                module.fail_json(
                    changed=False, msg=f"Output {output_name} doesn't exist"
                )
            else:
                payload = {"output_name": output_name}
                if output_type:
                    payload["type"] = output_type
                if output_hosts:
                    payload["hosts"] = output_hosts
                if is_default is not None:
                    payload["is_default"] = is_default
                if is_default_monitoring is not None:
                    payload["is_default_monitoring"] = is_default_monitoring
                if ca_trusted_fingerprint:
                    payload["ca_trusted_fingerprint"] = ca_trusted_fingerprint
                if config_yaml:
                    payload["config_yaml"] = config_yaml
                x = kb.update_fleet_output(**payload)
                module.exit_json(
                    changed=True, msg=f"Output {output_name} Updated", output=x
                )
        else:
            module.fail_json(msg="No Output Name Specified.")


if __name__ == "__main__":
    main()
