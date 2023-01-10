from typing import List, Tuple, Any
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
        _, cmd = text.split(maxsplit=1)
        try:
            cmd, args = cmd.split(maxsplit=1)
            name, num = args.rsplit(maxsplit=1)
        except ValueError:
            args = None

        if cmd == "add":
            try:
                self.add(name, num)
            except ValueError as err:
                print(err)
                return
        elif cmd == "del":
            self.delete(args)

        else:
            raise ValueError(f"Invalid command: {cmd}")

    def add(self, name: str, phonenum: str) -> None:
        """Adds a new contact"""
        self.validate_phone_number(phonenum)
        self._contacts.append((name, phonenum))
        self.save()

    def delete(self, name: str | None) -> None:
        """Deletes contact with the given NAME [SURNAME].
        Does nothing if no or wrong name provided"""
        self._contacts = [c for c in self._contacts if c[0] != name]
        self.save()

    def validate_phone_number(self, phonenum: str) -> None:
        """Helper function for validating the provided phone number
        Raises: ValueError if phonenumber is not string or in invalid format"""
        if not isinstance(phonenum, str):
            raise ValueError("A valid phone number is required")

        if not self.PHONE_EXPR.match(phonenum):
            raise ValueError(f"Invalid phone number: {phonenum}")

    def load(self) -> None:
        """Loads the saved contacts of the app"""
        with open("./contacts.json", encoding="utf-8") as f:
            self._contacts = [tuple(entry) for entry in json.load(f)["_contacts"]]

    def save(self) -> None:
        """Saves contact in json format"""
        with open("./contacts.json", "w+", encoding="utf-8") as f:
            json.dump({"_contacts": self._contacts}, f)
