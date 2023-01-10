import contacts
from pytest_bdd import scenario, given, parsers, when, then


class TestAddingEntries:
    def test_basic(self):
        app = contacts.Application()

        app.run("contacts add NAME 3344554433")

        assert app._contacts == [("NAME", "3344554433")]

    def test_surnames(self):
        app = contacts.Application()

        app.run("contacts add Mario Mario 3344554433")
        app.run("contacts add Luigi Mario 3344554433")
        app.run("contacts add Princess Peach Toadstool 3339323323")

        assert app._contacts == [
            ("Mario Mario", "3344554433"),
            ("Luigi Mario", "3344554433"),
            ("Princess Peach Toadstool", "3339323323"),
        ]

    def test_international_numbers(self):
        app = contacts.Application()

        app.run("contacts add NAME +393344554433")

        assert app._contacts == [("NAME", "+393344554433")]

    def test_invalid_strings(self):
        app = contacts.Application()

        app.run("contacts add NAME InvalidString")

        assert app._contacts == []

    def test_reload(self):
        app = contacts.Application()

        app.run("contacts add NAME 3344554433")

        assert app._contacts == [("NAME", "3344554433")]

        app._clear()
        app.load()

        assert app._contacts == [("NAME", "3344554433")]

@scenario("../acceptance/delete_contact.feature", "Removing a Basic Contact")
def test_deleting_contact():
    pass
    

@given("I have a contact book", target_fixture="contactbook")
def contactbook():
    return contacts.Application()

@given(parsers.parse("I have a \"{contactname}\" contact"))
def have_a_contact(contactbook, contactname):
    contactbook.add(contactname, "000")

@when(parsers.parse("I run the \"{command}\" command"))
def runcommand(contactbook, command):
    contactbook.run(command)

@then("My contacts list is now empty")
def emptlylist(contactbook):
    assert contactbook._contacts == []