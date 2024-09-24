import unittest
from unittest.mock import patch, MagicMock
from src.scheduler.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler('02:00', 'UTC')

    @patch('src.scheduler.scheduler.schedule')
    def test_schedule_daily(self, mock_schedule):
        mock_job = MagicMock()
        self.scheduler.schedule_daily(mock_job)
        mock_schedule.every.return_value.day.at.assert_called_once_with('02:00')
        mock_schedule.every.return_value.day.at.return_value.do.assert_called_once()

    @patch('src.scheduler.scheduler.schedule')
    @patch('src.scheduler.scheduler.time')
    def test_run(self, mock_time, mock_schedule):
        mock_schedule.run_pending.side_effect = [None, Exception("Stop loop")]
        with self.assertRaises(Exception):
            self.scheduler.run()
        mock_schedule.run_pending.assert_called()
        mock_time.sleep.assert_called_once_with(60)

    @patch('src.scheduler.scheduler.datetime')
    def test_get_current_time(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        current_time = self.scheduler._get_current_time()
        self.assertEqual(current_time, "2023-01-01 12:00:00 UTC")
