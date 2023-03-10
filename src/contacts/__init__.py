from typing import List, Tuple, Any, Optional
import re
import json


class Application:
    """Class definition for the app"""

    _contacts: List[Tuple[Any, ...]]
    PHONE_EXPR = re.compile("^[+]?[0-9]{3,}$")

    def __init__(self) -> None:
        """Constructor"""
        self._clear()

    def _clear(self) -> None:
        """Clear the list of contacts"""
        self._contacts = []

    def run(self, text: str) -> None:
        """Runs the command provided"""
        cmd: str
        text = text.strip()
        _, cmd = text.split(maxsplit=1)
        try:
            cmd, args = cmd.split(maxsplit=1)
        except ValueError:
            args = None

        if cmd == "add":
            name, num = args.rsplit(maxsplit=1)  # type: ignore # mypy ignorance of exception hanlding
            try:
                self.add(name, num)
            except ValueError as err:
                print(err)
                return
        elif cmd == "del":
            self.delete(args)
        elif cmd == "ls":
            self.print_list()
        else:
            raise ValueError(f"Invalid command: {cmd}")

    def add(self, name: str, phonenum: str) -> None:
        """Adds a new contact"""
        self.validate_phone_number(phonenum)
        self._contacts.append((name, phonenum))
        self.save()

    def delete(self, name: Optional[str]) -> None:
        """Deletes contact with the given NAME [SURNAME].
        Does nothing if no or wrong name provided"""
        self._contacts = [c for c in self._contacts if c[0] != name]
        self.save()

    def print_list(self):
        """Prints a list of all contacts included in the contactbook"""
        print(*(f"{c[0]} {c[1]}" for c in self._contacts), sep="\n")

    def validate_phone_number(self, phonenum: str) -> None:
        """Helper function for validating the provided phone number
        Raises: ValueError if phonenumber is not string or in invalid format"""
        if not isinstance(phonenum, str):
            raise ValueError("A valid phone number is required")

        if not self.PHONE_EXPR.match(phonenum):
            raise ValueError(f"Invalid phone number: {phonenum}")

    def load(self) -> None:
        """Loads the saved contacts of the app"""
        try:
            with open("./contacts.json", "r+", encoding="utf-8") as f:
                self._contacts = [tuple(entry) for entry in json.load(f)["_contacts"]]
        except:
            self._clear()
            with open("./contacts.json", "w+", encoding="utf-8") as f:
                self.save()

    def save(self) -> None:
        """Saves contact in json format"""
        with open("./contacts.json", "w+", encoding="utf-8") as f:
            json.dump({"_contacts": self._contacts}, f)


def main():
    import sys

    app = Application()
    app.load()
    app.run(" ".join(sys.argv))
