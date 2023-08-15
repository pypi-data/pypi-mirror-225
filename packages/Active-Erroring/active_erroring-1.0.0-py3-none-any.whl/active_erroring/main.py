import logging
import os


class ActiveErroring:
    @staticmethod
    def drop_error(error_name=None, message=None, fake_code=None, relative_path=None) -> None:
        """
        Parameters:
            error_name (str): The name of the error you want to throw. By default, it's MeowError
            message (str):  The message of the error. By default, it's Fuck.
            fake_code (str): The fictional code that caused an error. By default, it's not included.
            relative_path (str): By default, it's set to abspath.

        Returns:
            None
        """

        if not error_name:
            error_name = "MeowError"

        if not message:
            message = "Fuck"

        if not relative_path:
            relative_path = os.path.abspath(__file__)

        if type(fake_code) is str:
            fake_code_length = len(fake_code)
            the_code = f"\n    {fake_code}\n    {fake_code_length*'~'}"
        else:
            the_code = ""

        formatted_file_path = f"\033[34m{relative_path}\033[0m"

        logger = logging.getLogger(__name__)

        out = f"""Traceback (most recent call last):
  File "{formatted_file_path}", line -1, in <module>{the_code}
{error_name}: {message}
"""

        logger.error(out)


if __name__ == '__main__':
    ActiveErroring.drop_error()
