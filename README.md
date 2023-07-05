# Elasticsearch Security

The "Elasticsearch Kibana" collection provides Ansible modules to manage Kibana. 

## Modules

### elasticsearch_security_user

This module allows you to manage Elasticsearch security users. It can create, update, or delete users.

#### Options:

- `es_pass` (required): Elasticsearch password.
- `es_url` (required): URL of the Elasticsearch cluster.
- `es_user` (required): Elasticsearch username.
- `force`: Forcefully update the user even if it already exists.
- `state` (required): Specifies whether the user should be present or absent.
- `user_email`: Email address of the user.
- `user_full_name`: Full name of the user.
- `user_name` (required): Name of the user to be managed.
- `user_password`: Password for the user.
- `user_roles`: List of roles assigned to the user.

> This module requires the `kibana-api` Python library to be installed.

## Requirements

- `kibana-api`: Python library for interacting with Elasticsearch.

## Author

- Name: Linus