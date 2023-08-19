[
  {
    "type": "divider"
  },
  {
    "type": "section",
    "text": {
      "type": "mrkdwn",
      "text": "*{{ last_version_url }}*: Unittests *FAILED*\n*Pipeline*: {{pipeline_url}}\n*Build log*: {{ build_status_url }}\n*Test Reports*: {{report_group_url}}\n*Build time*: {{ build_time }}\n*Git*: {{ git_info }}"
    },
    "accessory": {
      "type": "image",
      "image_url":  "https://ads-utils-icons.s3-us-west-2.amazonaws.com/ci-buildbot/flask-red.png",
      "alt_text": "Unittests failed"
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
