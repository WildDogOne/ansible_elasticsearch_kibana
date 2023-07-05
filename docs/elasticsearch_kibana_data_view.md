> ELASTICSEARCH_KIBANA_DATAVIEW    (plugins/modules/elasticsearch_kibana_dataview.py)

        This module allows you to manage Kibana Dataviews.
        It can create, update, or delete dataviews.

OPTIONS (= is mandatory):

= kb_pass
        Kibana password.
        no_log: true

= kb_url
        URL of the Kibana cluster.

= kb_user
        Kibana username.

- force
        Forcefully update the user even if it already exists.
        default: null
        type: bool

= state
        Specifies whether the user should be present or absent.
        choices: [present, absent]

= dv_name
        Name of the dataview.
        required: true
= dv_title
        Pattern of the dataview.
        required: true
= dv_timeFieldName
        Time field name of the dataview.
        required: false


AUTHOR: Linus
