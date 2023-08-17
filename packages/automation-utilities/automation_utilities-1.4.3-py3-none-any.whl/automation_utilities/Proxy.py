class Proxy:
    def __init__(
            self,
            server: str | None = None,
            port: str | None = None,
            username: str | None = None,
            password: str | None = None,
            information: list[str] | None = None
    ):
        if information is None:
            self.server = server
            self.port = port
            self.username = username
            self.password = password
        else:
            self.server, self.port, self.username, self.password = information

    def __call__(self, *types: str):
        if len(types) == 0:
            types = ('http', 'https')
        return {
            f'{proxy_type}':
                f'{proxy_type}://{self.username}:{self.password}@{self.server}:{self.port}' for proxy_type in types
        }
