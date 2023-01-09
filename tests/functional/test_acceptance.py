import contacts


class TestAddingEntries(self):
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
            app = contancts.Application()

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
