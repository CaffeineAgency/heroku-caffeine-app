import lxml.html
import cssselect
import requests


class ConversationBotController:
    def __init__(self, obj, hooker, text):
        self.commands_list = ["help", "cmds", "wake", "sfw"]
        self.command_dict = {
            "help": lambda *_: "**Краткий референс**\nПример использования: \n.{cmd} arg1|arg2|<...>",
            "cmds": lambda *_: "Доступные команды:\n" + "\n".join(self.commands_list),
            "wake": lambda *_: "Awaken!",
            "sfw": self.get_random_booru_image,
            "notify_creator": lambda msg, *_: hooker.notify_creator(msg, self.sender),
        }

        self.sender = obj["peer_id"]
        self.text = text
        self.hooker = hooker
        self.parsed_command_result = self.try_parse_command()

    def try_parse_command(self):
        text = self.text
        command_dict = self.command_dict

        try:
            command_name, command_args = text.split(maxsplit=1)
        except:
            command_name, command_args = text.strip(), None
        if command_name not in self.command_dict:
            return "bot@Celesta > Command not recognized."
        command_args = command_args.split("|") if command_args else []
        return command_dict[command_name](*command_args)

    def execute(self):
        if self.parsed_command_result:
            if type(self.parsed_command_result) == dict:
                msg, att = self.parsed_command_result["msg"], self.parsed_command_result["att"]
                self.hooker.send_message(self.sender, msg, att)
            else:
                self.hooker.send_message(self.sender, self.parsed_command_result)

    def get_random_booru_image(self):
        rand_furry_link = "http://safebooru.org/index.php?page=post&s=random"
        html = requests.get(rand_furry_link).text
        root = lxml.html.fromstring(html)
        image = "http:" + root.cssselect("img#image")[0].attrib["src"]
        return {
            "msg": "Catch it!",
            "att": self.hooker.upload_photo(image)
        }
