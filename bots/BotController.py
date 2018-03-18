from bots.GroupApiHooks import GroupApiHooks


class BotController:

    def __init__(self, obj, hooker):
        self.commands_list = ["help", "cmds", "wake"]
        self.command_dict = {
            "help": lambda *_: "**Краткий референс**\nПример использования: .{command_name} arg1|arg2|3|(256)|...",
            "cmds": lambda *_: "Доступные команды:\n" + "\n".join(self.commands_list),
            "wake": lambda *_: "Awaken!",
            "test_notify": lambda *_: GroupApiHooks.notify_creator("Test notify"),
        }

        self.sender = obj["user_id"]
        self.text = obj["body"].strip()
        self.hooker = hooker
        self.start_checking()

    def start_checking(self):
        if self.text.startswith("."):
            try:
                self.parsed_command_result = self.try_parse_command()
            except Exception as e:
                GroupApiHooks.notify_creator("Error(s) happend: " + ", ".join(e.args))

    def try_parse_command(self):
        text = self.text[1:].strip()
        command_dict = self.command_dict

        command_name, *command_args = text.split()
        if command_name not in self.command_dict:
            return "bot@Clyde > Такой команды, увы, нет."
        command_args = command_args if command_args else None
        return command_dict[command_name](command_args)

    def execute(self):
        send_message = self.hooker.send_message
        sender = self.sender
        parsed_command_result = self.parsed_command_result
        send_message(sender, parsed_command_result)