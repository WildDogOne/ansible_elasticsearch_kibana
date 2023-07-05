#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
from kibana.kibana import kibana

DOCUMENTATION = """
---
module: elasticsearch_kibana_data_view
short_description: Manage Kibana Dataviews
description:
    - This module allows you to manage Kibana Dataviews.
    - It can create, update, or delete dataviews.

author: Your Name

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

  dv_name:
    description:
      - Name of the dataview.
    required: true
  dv_title:
    description:
      - Pattern of the dataview.
    required: true
  dv_timeFieldName:
    description:
      - Time field name of the dataview.
    required: false

  force:
    description:
      - Forcefully update the user even if it already exists.
    required: false
    type: bool

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
        dv_name=dict(type="str", required=True),
        dv_title=dict(type="str", required=True),
        dv_timeFieldName=dict(type="str", required=False),
        force=dict(type=bool),
        tls_verify=dict(type=bool),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    state = module.params["state"]
    kb_url = module.params["kb_url"]
    kb_user = module.params["kb_user"]
    kb_pass = module.params["kb_pass"]
    dv_name = module.params["dv_name"]
    dv_title = module.params["dv_title"]
    dv_timeFieldName = module.params["dv_timeFieldName"]
    force = module.params["force"]
    tls_verify = module.params["tls_verify"]

    if tls_verify == False:
        kb = kibana(
            base_url=kb_url, username=kb_user, password=kb_pass, ssl_verify=False
        )
    else:
        kb = kibana(base_url=kb_url, username=kb_user, password=kb_pass)
    if state == "present":
        existing_dataview = kb.get_dataview(dataview_id=dv_name)
        if existing_dataview:
            if force: # if force is true, delete the existing dataview and create a new one
                kb.delete_dataview(dataview_id=existing_dataview)
                pattern_json = {
                    "name": dv_name,
                    "title": dv_title,
                    "timeFieldName": dv_timeFieldName,
                }
                kb.create_dataview(dataview=pattern_json)
                module.exit_json(
                    changed=True, msg=f"Dataview {dv_name} created successfully."
                )
            else: # if force is false, exit with no change
                module.exit_json(
                    changed=False,
                    msg=f"Dataview {dv_name} already exists.",
                )
        else: # if dataview doesn't exist, create a new one
            pattern_json = {
                "name": dv_name,
                "title": dv_title,
                "timeFieldName": dv_timeFieldName,
            }
            kb.create_dataview(dataview=pattern_json)
            module.exit_json(
                changed=True, msg=f"Dataview {dv_name} created successfully."
            )
    elif state == "absent":
        dvid = kb.get_dataview(dataview_id=dv_name)
        if dvid:
            kb.delete_dataview(dataview_id=dvid)
            module.exit_json(
                changed=True, msg=f"Dataview {dv_name} removed successfully."
            )
        else:
            module.exit_json(
                changed=False,
                msg=f"Dataview {dv_name} doesn't exist. No change needed",
            )


if __name__ == "__main__":
    main()
