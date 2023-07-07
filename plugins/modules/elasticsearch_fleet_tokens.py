#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
from kibana.kibana import kibana

DOCUMENTATION = """
---
module: elasticsearch_fleet_tokens
short_description: Manage Fleet Integration tokens
description:
    - This module allows you to manage Integration tokens.
    - It can Output the tokens or generate a new one

author: Linus

options:
  state:
    description:
      - Specifies whether the user should be present or absent.
    choices: ['get']
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

  token_type:
    description:
      - Which token type you want to get
    choices: ['service_token', 'enrolment_key']
    required: true

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
        state=dict(type="str", choices=["get"], required=True),
        kb_url=dict(type="str", required=True),
        kb_user=dict(type="str", required=True),
        kb_pass=dict(type="str", required=True, no_log=True),
        token_type=dict(
            type="str", required=True, choices=["service_token", "enrolment_key"]
        ),
        agent_policy_name=dict(type="str", required=False),
        tls_verify=dict(type=bool),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    state = module.params["state"]
    kb_url = module.params["kb_url"]
    kb_user = module.params["kb_user"]
    kb_pass = module.params["kb_pass"]
    token_type = module.params["token_type"]
    agent_policy_name = module.params["agent_policy_name"]
    tls_verify = module.params["tls_verify"]

    if tls_verify == False:
        kb = kibana(
            base_url=kb_url, username=kb_user, password=kb_pass, ssl_verify=False
        )
    else:
        kb = kibana(base_url=kb_url, username=kb_user, password=kb_pass)

    if state == "get":
        if token_type == "service_token":
            service_token = kb.get_service_token()
            module.exit_json(changed=False, msg=f"Token generated", token=service_token)
        if token_type == "enrolment_key" and agent_policy_name:
            enrollment_key = kb.get_enrollment_key(agent_policy_name=agent_policy_name)
            if enrollment_key:
                module.exit_json(
                    changed=False, msg=f"Enrolment key found", token=enrollment_key
                )
            else:
                module.fail_json(
                    msg="Enrolment key not found. Please check the agent policy name."
                )
        else:
            module.fail_json(
                msg="No agent policy name specified. Please specify an agent policy name."
            )
    module.fail_json(msg="No state specified. Please specify a state.")


if __name__ == "__main__":
    main()
