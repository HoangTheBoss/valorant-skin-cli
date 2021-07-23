from InquirerPy.utils import color_print

from InquirerPy import inquirer

from ...utility.config_manager import Config as app_config


class Config_Editor:

    # my friends made me listen to alvin and the chipmunks music
    # while writing this so i apologize for how poorly its written

    def __init__(self):
        self.config = app_config.fetch_config()

        self.config_menu("main", self.config)

    def config_menu(self, section, choices, callback=None, callback_args=None):
        # recursion makes me want to die but its for a good cause

        prompt_choices = [
            {"name": f"{setting}" + ( f" ({value[0]})" if isinstance(value, list) else f" ({value})" if not isinstance(value, dict) else " (>>)"), "value": setting} for
            setting, value in choices.items()
        ]
        prompt_choices.insert(0, {"name": "back" if section != "main" else "done", "value": "back"} )

        choice = inquirer.select(
            message=f"[{section}] select a configuration option",
            choices=prompt_choices,
            pointer=">"
        ).execute()

        if choice == "back":
            if section != "main":
                callback(*callback_args)
            elif callback is None:
                app_config.modify_config(self.config)
                color_print(
                    [("LimeGreen", "config saved! restart the program for changes to take effect.")])
                return
        else:
            if isinstance(choices[choice], dict):
                self.config_menu(choice, choices[choice], callback=self.config_menu,callback_args=(section, choices, callback, callback_args))
            else:
                choices[choice] = self.config_set(choice, choices[choice])
                self.config_menu(section, choices, callback, callback_args)

    @staticmethod
    def config_set(name, option):
        if type(option) is str:
            choice = inquirer.text(
                message=f"set value for {name} (expecting str)",
                default=str(option),
                validate=lambda result: not result.isdigit(),
                filter=lambda result: str(result)
            ).execute()
            return choice

        if type(option) is int:
            choice = inquirer.text(
                message=f"set value for {name} (expecting int)",
                default=str(option),
                validate=lambda result: result.isdigit(),
                filter=lambda result: int(result)
            ).execute()
            return choice

        if type(option) is bool:
            choice = inquirer.select(
                message=f"set value for {name}",
                default=option,
                choices=[{"name": "true", "value": True},
                         {"name": "false", "value": False}],
                pointer=">"
            ).execute()
            return choice

        if type(option) is list:
            current = option[0]
            options = option[1]
            choice = inquirer.select(
                message=f"set value for {name}",
                default=current,
                choices={option:option for option in options},
                pointer=">"
            ).execute()
            option[0] = choice 
            return option