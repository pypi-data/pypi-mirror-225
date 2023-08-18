import subprocess


def command_available(segments) -> bool:
    try:
        subprocess.run(segments, stdout=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False


def has_json_pp():
    return command_available(['json_pp', '-v'])


def has_curl():
    return command_available(['curl', '-V'])


class CurlRenderer:

    def __init__(self):
        self.self_has_pp = has_json_pp()

    def render_url(self, url, limit=None, body=None, content_type=None):
        extra_flag = ''
        suffix_pipe = ''
        query = ''
        if self.self_has_pp:
            extra_flag = ' -s'
            suffix_pipe = ' | json_pp'
        if limit is not None:
            query = f"?limit={limit}"
        if body is not None:
            extra_flag += f" -X POST -d '{body}'"
        if content_type is not None:
            extra_flag += f" -H \"Content-Type: {content_type}\""
        return f"curl -H \"Authorization: $BEARER_TOKEN\"{extra_flag} '{url}{query}'{suffix_pipe}"
