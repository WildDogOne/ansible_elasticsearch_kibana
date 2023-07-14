#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
from kibana.kibana import kibana

DOCUMENTATION = """
---
module: elasticsearch_fleet_package
short_description: Install Elastic Security Prebuilt Rules
description:
    - This module allows you to manage Prebuilt Rules.
    - It can create, or check status of Prebuilt Rules.
    - It is not possible to remove prebuilt rules. Once installed, always installed

author: Linus

options:
  state:
    description:
      - Specifies whether the Prebuild rules should be installed. Or if you want to check the status of the rules.
    choices: ['present', 'status']
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
        state=dict(type="str", choices=["present", "status"], required=True),
        kb_url=dict(type="str", required=True),
        kb_user=dict(type="str", required=True),
        kb_pass=dict(type="str", required=True, no_log=True),
        tls_verify=dict(type=bool),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    state = module.params["state"]
    kb_url = module.params["kb_url"]
    kb_user = module.params["kb_user"]
    kb_pass = module.params["kb_pass"]
    tls_verify = module.params["tls_verify"]

    if tls_verify == False:
        kb = kibana(
            base_url=kb_url, username=kb_user, password=kb_pass, ssl_verify=False
        )
    else:
        kb = kibana(base_url=kb_url, username=kb_user, password=kb_pass)

    if state == "present":
        kb.load_prebuilt_rules()
        module.exit_json(changed=True, msg=f"Prebuild Rules installed successfully.")
    elif state == "status":  # if state is absent, delete the dataview
        status = kb.get_prebuilt_rules_status()
        module.exit_json(changed=True, msg=f"Prebuild Rules Status", status=status)


if __name__ == "__main__":
    main()
