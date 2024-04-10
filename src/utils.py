from fastapi import Request


def get_host_ip(request: Request) -> str:
    if request.client:
        return request.client.host
    else:
        return "undefined"
