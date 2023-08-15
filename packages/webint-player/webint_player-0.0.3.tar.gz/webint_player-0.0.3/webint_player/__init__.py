"""Play media on your website."""

import web

app = web.application(__name__, prefix="player")


@app.control("")
class Player:
    """Media player."""

    def get(self):
        return app.view.index()
