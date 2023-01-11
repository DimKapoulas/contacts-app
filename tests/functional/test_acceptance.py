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


@scenario("../acceptance/list_contacts.feature", "Listing Added Contacts")
def test_listing_added_contacts(capsys):
    pass

@scenario("../acceptance/delete_contact.feature", "Removing a Basic Contact")
def test_deleting_contact():
    pass


@given("I have a contact book", target_fixture="contactbook")
def contactbook():
    return contacts.Application()

@given(parsers.parse("I have a first {first} contact"))
def have_a_first_contact(contactbook, first):
    contactbook.add(first, "000")
    return first

@given(parsers.parse("I have a second {second} contact"))
def have_a_second_contact(contactbook, second):
    contactbook.add(second, "000")
    return second

@then(parsers.parse("the output contains {listed_contacts} contacts"))
def output_contains(listed_contacts, capsys):
    expected_list = "".join([
        f"{c} 000\name" for c in listed_contacts.split(",")
    ])
    out, _ = capsys.readouterr()
    assert expected_list == out


@given(parsers.parse('I have a "{contactname}" contact'))
def have_a_contact(contactbook, contactname):
    contactbook.add(contactname, "000")


@when(parsers.parse('I run the "{command}" command'))
def runcommand(contactbook, command):
    contactbook.run(command)


@then("My contacts book is now empty")
def emptlylist(contactbook):
    assert contactbook._contacts == []
