import os
from unittest.mock import call, patch

from django.db import connections
from django.test import TestCase

from test_queries import NumQueriesMixin

current_directory = os.getcwd()


class TestNumQueriesMixin(NumQueriesMixin, TestCase):
    def test_basic_functionality(self):
        with self.assertNumQueries(1):
            connections["default"].cursor().execute("SELECT 1")

    def test_file_creation(self):
        # This test checks if the SQL log file is created
        # You might need to adjust the expected filename based on your implementation
        expected_filename = "path_to_expected_file.sqllog"  # Adjust this
        with self.assertNumQueries(1):
            connections["default"].cursor().execute("SELECT 1")
        self.assertTrue(os.path.exists(expected_filename))

    def test_file_comparison(self):
        # This test checks if the SQL log files are compared correctly
        # You might need to adjust the expected filename and contents based on your implementation
        expected_filename = "path_to_expected_file.sqllog"  # Adjust this
        with open(expected_filename, "w") as f:
            f.write("SELECT 1")
        with self.assertNumQueries(1):
            connections["default"].cursor().execute("SELECT 1")

    def test_file_comparison_function(self):
        expected_filename = "path_to_expected_file.sqllog"  # Adjust this
        with open(expected_filename, "w") as f:
            f.write("SELECT 1")

        def call_sql():
            connections["default"].cursor().execute("SELECT 1")

        self.assertNumQueries(1, call_sql)

    def test_environment_variables(self):
        os.environ["TEST_QUERIES_DISABLE"] = "1"
        with self.assertNumQueries(1):
            connections["default"].cursor().execute("SELECT 1")
        # Test content of the SQL log files
        with open(
            "tests/sqllog/test_num_queries.TestNumQueriesMixin.test_environment_variables.0.sqllog.new",
            "r",
        ) as f:
            self.assertEqual(f.read(), "SELECT 1\n")

    def test_file_comparison_with_existing_lines(self):
        # This test checks if the SQL log files are compared correctly when the file already has lines
        # You might need to adjust the expected filename and contents based on your implementation
        expected_filename = (
            "tests/sqllog/test_num_queries.TestNumQueriesMixin.test_file_comparison_with_existing_lines.0.sqllog"
        )
        with open(expected_filename, "w") as f:
            f.write("SELECT 1\nSELECT 2")  # Writing multiple lines to the file
        with self.assertNumQueries(2):
            connections["default"].cursor().execute("SELECT 1")
            connections["default"].cursor().execute("SELECT 2")
        # Test content of the SQL log files
        with open(
            "tests/sqllog/test_num_queries.TestNumQueriesMixin.test_file_comparison_with_existing_lines.0.sqllog.new",
            "r",
        ) as f:
            self.assertEqual(f.read(), "SELECT 1\nSELECT 2\n")

    def test_file_comparison_with_existing_lines_not_equal(self):
        expected_filename = (
            "tests/sqllog/test_num_queries.TestNumQueriesMixin.test_file_comparison_with_existing_lines.0.sqllog"
        )
        with open(expected_filename, "w") as f:
            f.write("SELECT 1")  # Writing multiple lines to the file
        with patch("builtins.print") as mock_print:
            with self.assertRaisesRegex(AssertionError, "Captured queries were:\n1. SELECT 1\n2. SELECT 2"):
                with self.assertNumQueries(1):
                    connections["default"].cursor().execute("SELECT 1")
                    connections["default"].cursor().execute("SELECT 2")
            self.assertEquals(mock_print.call_args_list[0], call("New query was recorded:"))
            self.assertIn("sql: SELECT 1", mock_print.mock_calls[1].args[0]),
            self.assertEquals(mock_print.call_args_list[2], call("See difference:"))
            self.assertEquals(
                mock_print.call_args_list[3],
                call(
                    f"  diff {current_directory}/tests/sqllog/test_num_queries."
                    "TestNumQueriesMixin.test_file_comparison_with_existing_lines_not_equal.0.sqllog "
                    f"{current_directory}/tests/sqllog/test_num_queries."
                    "TestNumQueriesMixin.test_file_comparison_with_existing_lines_not_equal.0.sqllog.new"
                ),
            )
            self.assertEquals(len(mock_print.call_args_list), 4)

    def test_file_comparison_with_existing_lines_delete(self):
        expected_filename = (
            "tests/sqllog/test_num_queries."
            "TestNumQueriesMixin.test_file_comparison_with_existing_lines_delete.0.sqllog"
        )
        with open(expected_filename, "w") as f:
            f.write("SELECT 1\nSELECT 3\nSELECT 3")  # Writing multiple lines to the file
        with patch("builtins.print") as mock_print:
            with self.assertRaisesRegex(AssertionError, "Captured queries were:\n1. SELECT 1\n2. SELECT 2"):
                with self.assertNumQueries(1):
                    connections["default"].cursor().execute("SELECT 1")
                    connections["default"].cursor().execute("SELECT 2")
                    connections["default"].cursor().execute("SELECT 3")
            self.assertEquals(mock_print.call_args_list[0], call("New query was recorded:"))
            self.assertIn("sql: SELECT 2", mock_print.mock_calls[1].args[0]),
            self.assertEquals(mock_print.call_args_list[2], call("See difference:"))
            self.assertEquals(
                mock_print.call_args_list[3],
                call(
                    f"  diff {current_directory}/tests/sqllog/test_num_queries."
                    "TestNumQueriesMixin.test_file_comparison_with_existing_lines_delete.0.sqllog "
                    f"{current_directory}/tests/sqllog/test_num_queries."
                    "TestNumQueriesMixin.test_file_comparison_with_existing_lines_delete.0.sqllog.new"
                ),
            )
            self.assertEquals(
                mock_print.call_args_list[4],
                call("delete    a[2:3] --> b[3:3] ['SELECT 3...'] --> []"),
            )
            self.assertEquals(len(mock_print.call_args_list), 5)

    def test_file_comparison_with_existing_lines_replace(self):
        expected_filename = (
            "tests/sqllog/test_num_queries."
            "TestNumQueriesMixin.test_file_comparison_with_existing_lines_replace.0.sqllog"
        )
        with open(expected_filename, "w") as f:
            f.write("SELECT 1\nSELECT 2\nSELECT 3\nSELECT 4\nSELECT 5")  # Writing multiple lines to the file
        with patch("builtins.print") as mock_print:
            with self.assertRaisesRegex(AssertionError, "Captured queries were:\n1. SELECT 1\n2. SELECT 2"):
                with self.assertNumQueries(1):
                    connections["default"].cursor().execute("SELECT 1")
                    connections["default"].cursor().execute("SELECT 2")
                    connections["default"].cursor().execute("SELECT 0")
                    connections["default"].cursor().execute("SELECT 4")
                    connections["default"].cursor().execute("SELECT 5")
            self.assertEquals(mock_print.call_args_list[0], call("Query was replaced:"))
            self.assertIn("sql: SELECT 0", mock_print.mock_calls[1].args[0]),
            self.assertEquals(mock_print.call_args_list[2], call("See difference:"))
            self.assertEquals(
                mock_print.call_args_list[3],
                call(
                    f"  diff {current_directory}/tests/sqllog/test_num_queries."
                    "TestNumQueriesMixin.test_file_comparison_with_existing_lines_replace.0.sqllog "
                    f"{current_directory}/tests/sqllog/test_num_queries."
                    "TestNumQueriesMixin.test_file_comparison_with_existing_lines_replace.0.sqllog.new"
                ),
            )
            self.assertEquals(len(mock_print.call_args_list), 4)
