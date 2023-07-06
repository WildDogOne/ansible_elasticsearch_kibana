#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
from kibana.kibana import kibana

DOCUMENTATION = """
---
module: elasticsearch_fleet_package
short_description: Manage Fleet Integration Packages
description:
    - This module allows you to manage Integration Packages.
    - It can create, update, or delete Integration Packages.

author: Linus

options:
  state:
    description:
      - Specifies whether the user should be present or absent.
    choices: ['present', 'absent']
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

  package_name:
    description:
      - Name of the Package.
    required: true

  package_version:
    description:
      - Package version, if not defined it will default to the latest version.
    required: false

  tls_verify:
    description:
      - Whether to verify TLS certificates.
    required: false
    type: bool

notes:
  - This module requires the `elasticsearch` Python library to be installed.

requirements:
  - elasticsearch

seealso:
  - module: elasticsearch_security_role
"""


def main():
    module_args = dict(
        state=dict(
            type="str", choices=["present", "absent", "update-password"], required=True
        ),
        kb_url=dict(type="str", required=True),
        kb_user=dict(type="str", required=True),
        kb_pass=dict(type="str", required=True, no_log=True),
        package_name=dict(type="str", required=True),
        package_version=dict(type="str", required=False),
        tls_verify=dict(type=bool),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    state = module.params["state"]
    kb_url = module.params["kb_url"]
    kb_user = module.params["kb_user"]
    kb_pass = module.params["kb_pass"]
    package_name = module.params["package_name"]
    package_version = module.params["package_version"]
    tls_verify = module.params["tls_verify"]

    if tls_verify == False:
        kb = kibana(
            base_url=kb_url, username=kb_user, password=kb_pass, ssl_verify=False
        )
    else:
        kb = kibana(base_url=kb_url, username=kb_user, password=kb_pass)

    installation_status = kb.get_install_status(package_name=package_name)
    if state == "present":
        if not installation_status:
            kb.install_package(
                package_name=package_name, package_version=package_version
            )
            module.exit_json(
                changed=True, msg=f"Package {package_name} installed successfully."
            )
        else:
            module.exit_json(
                changed=False,
                msg=f"Package {package_name} already installed.",
            )
    elif state == "absent":  # if state is absent, delete the dataview
        if installation_status:
            kb.delete_package(package_name=package_name)
            module.exit_json(
                changed=True, msg=f"Package {package_name} removed successfully."
            )
        else:
            module.exit_json(
                changed=False,
                msg=f"Package {package_name} not present.",
            )


if __name__ == "__main__":
    main()
