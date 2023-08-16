import socketio, logging

class PrivamBot:
    def __init__(self, token):
        self.token = token
        self.socket = socketio.Client()
        self.socket.connect("https://privam.top")
        self.init_socket()

    def init_socket(self):
        self.socket.emit("bot", {"token": self.token})
        logging.info("Connected to Privam")

        @self.socket.on("private_message")
        def on_private_message(message):
            command = message["message"].split(" ")[0]
            if hasattr(self, command):
                getattr(self, command)(message)

        @self.socket.on("username_error")
        def on_username_error(message):
            logging.error("Username error: {}".format(message["error"]))

        @self.socket.on("username_success")
        def on_username_success(username):
            name = username["username"]
            logging.info(f"Logged in as {name}")

    def send(self, recipient, message):
        self.socket.emit("private_message", {"token": self.token, "recipient": recipient, "message": message})

    def new(self, command, handler):
        setattr(self, command, handler)

