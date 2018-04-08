from bots.GroupApiHooks import GroupApiHooks


class BotController:

    def __init__(self, obj, hooker):
        self.commands_list = ["help", "cmds", "wake"]
        self.command_dict = {
            "help": lambda *_: "**Краткий референс**\nПример использования: \n.{cmd} arg1|arg2|<...>",
            "cmds": lambda *_: "Доступные команды:\n" + "\n".join(self.commands_list),
            "wake": lambda *_: "Awaken!",
            "notify_creator": lambda msg, *_: hooker.notify_creator(msg, self.sender),
        }

        self.sender = obj["user_id"]
        self.text = obj["body"].strip()
        self.hooker = hooker
        self.parsed_command_result = self.try_parse_command()

    def try_parse_command(self):
        text = self.text[1:].strip()
        command_dict = self.command_dict

        try:
            command_name, command_args = text.split(maxsplit=1)
        except:
            command_name, command_args = text.strip(), None
        if command_name not in self.command_dict:
            return "bot@Clyde > Такой команды, увы, нет."
        command_args = command_args.split("|") if command_args else []
        return command_dict[command_name](*command_args)

    def execute(self):
        if self.parsed_command_result:
            self.hooker.send_message(self.sender, self.parsed_command_result)