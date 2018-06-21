import lxml.html
import cssselect
import requests


class ConversationBotController:
    def __init__(self, obj, hooker, text):
        self.commands_list = ["help", "cmds", "wake", "sfw"]
        self.command_dict = {
            # Utility commands
            "help": lambda *_: "**Краткий референс**\nПример использования: \n.{cmd} arg1|arg2|<...>",
            "cmds": lambda *_: "Доступные команды:\n" + "\n".join(self.commands_list),
            "wake": lambda *_: "Awaken!",
            # Booru related commands
            "sfw": self.get_random_image("sfw", True),
            "e621": self.get_random_image("e621", False),
            # The most important command
            "notify_creator": lambda msg, *_: hooker.notify_creator(msg, self.sender),
        }

        self.sender = obj["peer_id"]
        self.invoked_by = obj["conversation_message_id"]
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
                self.hooker.send_message(self.sender, "", self.parsed_command_result)
            else:
                self.hooker.send_message(self.sender, self.parsed_command_result)

    def get_random_image(self, _type, needfix):
        print("bot@Celesta > requests for", _type, "photo from", self.sender)
        if _type == "sfw":
            rand_link = "http://safebooru.org/index.php?page=post&s=random"
        elif _type == "e621":
            rand_link = "https://e621.net/post/random"
        else:
            return
        html = requests.get(rand_link).text
        root = lxml.html.fromstring(html)
        image = "http:" if needfix else ""
        image += root.cssselect("img#image")[0].attrib["src"]
        print("bot@Celesta > parsed link", image)
        att_image = self.hooker.upload_photo(image)
        print("bot@Celesta > created attachment", att_image)
        return {
            "message": "",
            "attachment": att_image,
            "forward_messages": str(self.invoked_by)
        }
