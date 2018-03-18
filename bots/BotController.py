from bots.GroupApiHooks import GroupApiHooks


class BotController:

    def __init__(self, obj, hooker):
        self.commands_list = ["help", "cmds", "wake"]
        self.command_dict = {
            "help": lambda *_: "**Краткий референс**\nПример использования: \n.{cmd} arg1|arg2|<...>",
            "cmds": lambda *_: "Доступные команды:\n" + "\n".join(self.commands_list),
            "wake": lambda *_: "Awaken!",
            "notify_creator": lambda msg, *_: GroupApiHooks(gid=hooker.gid).notify_creator(str(msg)),
        }

        self.sender = obj["user_id"]
        self.text = obj["body"].strip()
        self.hooker = hooker
        self.start_checking()

    def start_checking(self):
        if self.text.startswith("."):
            self.parsed_command_result = self.try_parse_command()

    def try_parse_command(self):
        text = self.text[1:].strip()
        command_dict = self.command_dict

        command_name, command_args = text.split(maxsplit=1)
        if command_name not in self.command_dict:
            return "bot@Clyde > Такой команды, увы, нет."
        command_args = command_args.split("|") if command_args else None
        return command_dict[command_name](command_args)

    def execute(self):
        self.hooker.send_message(self.sender, self.parsed_command_result)