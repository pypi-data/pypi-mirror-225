import socketio
class PrivamBot:
    def __init__(self, token):
        self.token = token
        self.socket = socketio.Client()
        self.socket.connect("https://privam.top")
        self.init_socket()

    def init_socket(self):
        @self.socket.on("connect")
        def on_connect():
            self.socket.emit("bot", {"token": self.token})

        @self.socket.on("private_message")
        def on_private_message(message):
            command = message["message"].split(" ")[0]
            if hasattr(self, command):
                getattr(self, command)(message)

        @self.socket.on("username_error")
        def on_username_error(message):
            print(message)

        @self.socket.on("username_success")
        def on_username_success(username):
            print(username)

    def send(self, recipient, message):
        self.socket.emit("private_message", {"token": self.token, "recipient": recipient, "message": message})

    def command(self, command, handler):
        setattr(self, command, handler)