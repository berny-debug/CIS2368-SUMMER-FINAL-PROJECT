import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import app as backend_app


class AppSprint2Tests(unittest.TestCase):
    def setUp(self):
        self.client = backend_app.app.test_client()
        self.read_patcher = patch("app.execute_read_query")
        self.query_patcher = patch("app.execute_query")
        self.mock_read = self.read_patcher.start()
        self.mock_query = self.query_patcher.start()
        self.addCleanup(self.read_patcher.stop)
        self.addCleanup(self.query_patcher.stop)

    def test_room_resident_endpoint_returns_room_and_residents(self):
        self.mock_read.side_effect = [
            [{"id": 1, "capacity": 2, "number": 101, "floor": 1}],
            [{"id": 10, "firstname": "Ada", "lastname": "Lovelace", "age": 20, "room": 1}],
        ]

        response = self.client.get("/rooms/1/residents")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["room"]["id"], 1)
        self.assertEqual(payload["residents"][0]["firstname"], "Ada")

    def test_stats_endpoint_returns_summary_counts(self):
        self.mock_read.side_effect = [
            [{"count": 2}],
            [{"count": 4}],
            [{"count": 3}],
        ]

        response = self.client.get("/stats")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["floor_count"], 2)
        self.assertEqual(payload["room_count"], 4)
        self.assertEqual(payload["resident_count"], 3)


if __name__ == "__main__":
    unittest.main()
