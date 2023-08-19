[
  {
    "type": "divider"
  },
  {
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*{{ last_version_url }}*: Unittests *SUCCESS*\n*Pipeline*: {{pipeline_url}}\n*Build log*: {{ build_status_url }}\n*Test Reports*: {{report_group_url}}\n*Run time*: {{ build_time }}\n*Git*: {{ git_info }}"
    },
    "accessory": {
      "type": "image",
      "image_url":  "https://ads-utils-icons.s3-us-west-2.amazonaws.com/ci-buildbot/flask-green.png",
      "alt_text": "Unittests success"
    }
  },
  {
    "type": "context",
    "elements": [
      {
        "type": "mrkdwn",
        "text": "{{ completed_date }} {{buildbot}}"
      }
    ]
  }
]
