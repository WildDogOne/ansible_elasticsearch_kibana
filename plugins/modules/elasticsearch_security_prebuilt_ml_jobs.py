#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
from kibana.kibana import kibana

DOCUMENTATION = """
---
module: elasticsearch_fleet_package
short_description: Configure Prebuilt Elastic Security ML Jobs
description:
    - This module allows you to manage prebuilt ML Jobs.
    - It can enable/disable

author: Linus

options:
  state:
    description:
      - Specifies whether the Prebuild rules should be installed/enabled. Or if you want to check the status of the rules.
    choices: ['enabled', 'disabled']
    required: true
  job_name:
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
            choices=["enabled", "disabled"],
            required=True,
        ),
        kb_url=dict(type="str", required=True),
        kb_user=dict(type="str", required=True),
        kb_pass=dict(type="str", required=True, no_log=True),
        job_name=dict(type="str", required=True, no_log=True),
        tls_verify=dict(type=bool),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    state = module.params["state"]
    kb_url = module.params["kb_url"]
    kb_user = module.params["kb_user"]
    kb_pass = module.params["kb_pass"]
    tls_verify = module.params["tls_verify"]
    job_name = module.params["job_name"]

    if tls_verify == False:
        kb = kibana(
            base_url=kb_url, username=kb_user, password=kb_pass, ssl_verify=False
        )
    else:
        kb = kibana(base_url=kb_url, username=kb_user, password=kb_pass)

    if state == "enabled":
        kb.enable_prebuild_ml_job(job_name=job_name)
        module.exit_json(changed=True, msg=f"ML Job {job_name} enabled successfully.")
    if state == "disabled":
        kb.enable_prebuild_ml_job(job_name=job_name)
        module.exit_json(changed=True, msg=f"ML Job {job_name} disabled successfully.")


if __name__ == "__main__":
    main()
