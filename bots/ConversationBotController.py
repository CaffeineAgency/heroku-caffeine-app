import lxml.html
import cssselect
import requests


class ConversationBotController:
    def __init__(self, obj, hooker, text):
        self.commands_list = [
            "help - помощь",
            "cmds - список команд",
            "wake - `оживить` бота(желательно выполнять, если бот давно не работал)",
            "booruhelp - список буру"
        ]
        self.command_dict = {
            # Utility commands
            "help": lambda *_: "іди нахуй. cmds в допомогу.",
            "cmds": lambda *_: "Доступные команды:\n" + "\n".join(self.commands_list),
            "wake": lambda *_: {"message": "Awaken!", "attachment": "audio307982226_456239370"},
            "booruhelp": lambda *_: self.booruhelp(),
            # Booru related commands
            "sfw": lambda *_: self.get_random_image("sfw", True),
            "e621": lambda *_: self.get_random_image("e621", False),
            "loli": lambda *_: self.get_random_image("loli", False),
            "clop": lambda *_: self.get_random_image("clop", False),
            "svtfoe": lambda *_: self.get_random_image("svtfoe", False),
            "allgirl": lambda *_: self.get_random_image("allgirl", False),
            "gf": lambda *_: self.get_random_image("gf", False),
            "rm": lambda *_: self.get_random_image("rm", False),
            "r34": lambda *_: self.get_random_image("r34", False),
            "furry": lambda *_: self.get_random_image("furry", False),
            "meme": lambda *_: self.get_random_image("meme", False),
            "xbooru": lambda *_: self.get_random_image("xbooru", False),
            "gelbooru": lambda *_: self.get_random_image("gelbooru", False),
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
        boorus = {
            "sfw": "http://safebooru.org/index.php?page=post&s=random",
            "e621": "https://e621.net/post/random",
            "loli": "https://lolibooru.moe/post/random",
            "clop": "http://clop.booru.org/index.php?page=post&s=random",
            "svtfoe": "http://svtfoe.booru.org/index.php?page=post&s=random",
            "allgirl": "http://allgirl.booru.org/index.php?page=post&s=random",
            "gf": "http://gravityfalls.booru.org/index.php?page=post&s=random",
            "rm": "http://rm.booru.org/index.php?page=post&s=random",
            "r34": "https://rule34.xxx/index.php?page=post&s=random",
            "furry": "http://furry.booru.org/index.php?page=post&s=random",
            "meme": "http://meme.booru.org/index.php?page=post&s=random",
            "xbooru": "https://xbooru.com/index.php?page=post&s=random",
            "gelbooru": "https://gelbooru.com/index.php?page=post&s=random",
        }
        rand_link = boorus.get(_type)
        try:
            html = requests.get(rand_link).text
            root = lxml.html.fromstring(html)
            image = "http:" if needfix else ""
            image += root.cssselect("img#image")[0].attrib["src"]
            print("bot@Celesta > parsed link", image)
            att_image = self.hooker.upload_photo(image)
            print("bot@Celesta > created attachment", att_image)
            return {
                "message": "",
                "attachment": att_image
            }
        except Exception as e:
            self.hooker.notify_creator("We've got error: " + str(e), self.sender)
            return "bot@Celesta > error > " + str(e)

    def booruhelp(self):
        return "Нестабильные сервисы зачастую ничего не возвращают\n" \
               "r34 - [NSFW]r34\n" \
               "sfw - [SFW]safebooru\n" \
               "e621 - [MIXED]e621 - unstable\n" \
               "loli - [NSFW]lolicon - unstable\n" \
               "clop - [NSFW]mlp r34\n" \
               "svtfoe - [NSFW]svtfoe booru\n" \
               "gf - [MIXED]gravityfalls booru\n" \
               "rm - [SFW]rozenmaiden booru\n" \
               "furry - [NSFW]furry booru\n" \
               "meme - [SFW]meme booru\n" \
               "xbooru - [NSFW]xbooru\n" \
               "gelbooru - [MIXED]gelbooru\n" \
               "allgirl - [MIXED]allgirl booru"
