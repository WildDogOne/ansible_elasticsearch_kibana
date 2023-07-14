#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
from kibana.kibana import kibana

DOCUMENTATION = """
---
module: elasticsearch_fleet_package
short_description: Configure Elastic Security Rules
description:
    - This module allows you to manage Rules.
    - It can create/enable/delete/disable, or check status of Rules.

author: Linus

options:
  state:
    description:
      - Specifies whether the Prebuild rules should be installed/enabled. Or if you want to check the status of the rules.
    choices: ['enabled', 'absent', 'disabled']
    required: true
  rule_name:
    description:
      - Name of the rule.
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
        state=dict(
            type="str",
            choices=["present", "status", "enabled", "absent", "disabled"],
            required=True,
        ),
        kb_url=dict(type="str", required=True),
        kb_user=dict(type="str", required=True),
        kb_pass=dict(type="str", required=True, no_log=True),
        rule_name=dict(type="str", required=True, no_log=True),
        tls_verify=dict(type=bool),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    state = module.params["state"]
    kb_url = module.params["kb_url"]
    kb_user = module.params["kb_user"]
    kb_pass = module.params["kb_pass"]
    tls_verify = module.params["tls_verify"]
    rule_name = module.params["rule_name"]

    if tls_verify == False:
        kb = kibana(
            base_url=kb_url, username=kb_user, password=kb_pass, ssl_verify=False
        )
    else:
        kb = kibana(base_url=kb_url, username=kb_user, password=kb_pass)

    if state == "enabled":
        ids = []
        rules = kb.get_all_rules()
        for x in rules:
            if x["name"].lower() == rule_name.lower():
                ids.append(x["id"])
        kb.bulk_change_rules(rule_ids=ids, action="enable")
        module.exit_json(changed=True, msg=f"Rule {rule_name} enabled successfully.")
    if state == "disabled":
        ids = []
        rules = kb.get_all_rules()
        for x in rules:
            if x["name"].lower() == rule_name.lower():
                ids.append(x["id"])
        kb.bulk_change_rules(rule_ids=ids, action="disable")
        module.exit_json(changed=True, msg=f"Rule {rule_name} disabled successfully.")
    if state == "absent":
        ids = []
        rules = kb.get_all_rules()
        for x in rules:
            if x["name"].lower() == rule_name.lower():
                ids.append(x["id"])
        kb.bulk_change_rules(rule_ids=ids, action="delete")
        module.exit_json(changed=True, msg=f"Rule {rule_name} removed successfully.")


if __name__ == "__main__":
    main()
