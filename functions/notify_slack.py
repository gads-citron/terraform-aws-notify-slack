def send_slack_notification(payload: Dict[str, Any]) -> str:
    """
    Send notification payload to Slack

    :params payload: formatted Slack message payload
    :returns: response details from sending notification
    """

    slack_url = os.environ["SLACK_WEBHOOK_URL"]
    if not slack_url.startswith("http"):
        slack_url = decrypt_url(slack_url)

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        slack_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        result = urllib.request.urlopen(req)
        body = result.read().decode("utf-8")
        return json.dumps(
            {
                "code": result.getcode(),
                "info": result.info().as_string(),
                "body": body,
            }
        )

    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        logging.error(f"Slack HTTPError {e.code}: {error_body}")
        return json.dumps(
            {
                "code": e.getcode(),
                "info": e.info().as_string(),
                "body": error_body,
            }
        )