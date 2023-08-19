##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##


class Notifications:
    """Helper class to manage notification settings of a job.
    This class allows the user set to set notifications for when a job starts, fails
    and completes via SMS, email or other channels.
    """

    def __init__(
        self,
        channel: str = "sms",
        job_started: bool = False,
        job_failed: bool = False,
        job_completed: bool = False,
    ):
        """Constructor to initialize the Notifications object.

        Args:
            channel (str, optional): Notification channel to use. Defaults to "sms".
            job_started (bool, optional): Whether to trigger a notification on job starting. Defaults to False.
            job_failed (bool, optional): Whether to trigger a notification when job fails. Defaults to False.
            job_completed (bool, optional): Whether to trigger a notification on job completion. Defaults to False.
        """
        self._channel = channel
        self._job_started = job_started
        self._job_failed = job_failed
        self._job_completed = job_completed

    @property
    def channel(self):
        """Obtain the notification channel.

        Returns:
            str: The current notification channel.
        """
        return self._channel

    @property
    def job_started(self):
        """Determine if "job started" notifications are enabled.

        Returns:
            bool: True if "job started" notifications are enabled, False if not.
        """
        return self._job_started

    @property
    def job_failed(self):
        """Determine if "job failed" notifications are enabled.

        Returns:
            bool: True if "job failed" notifications are enabled, False if not.
        """
        return self._job_failed

    @property
    def job_completed(self):
        """Determine if "job-completed" notifications are enabled.

        Returns:
            bool: True if "job completed" notifications are enabled, False if not.
        """
        return self._job_completed

    def __str__(self):
        return "job_started=" + str(self.job_started) + ", job_failed=" + str(self.job_failed) + ", job_completed=" + str(self.job_completed)
