import subprocess
import fire
from loguru import logger


class Scooper(object):
    def __init__(self):
        pass

    def clear_scoop_cache(self, cmd):
        """
        Clear the scoop cache
        :param cmd: the command to clear the scoop cache
        :return: None
        """
        logger.info("Clearing the scoop cache")
        try:
            result = subprocess.run(cmd, shell=True, check=True)
            logger.info(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to run cmd: {cmd}")
            logger.error(f"Error message: {e}")
            raise e

    def main(self):
        cmd = 'scoop cache rm -a'
        self.clear_scoop_cache(cmd)

if __name__ == '__main__':
    fire.Fire(Scooper)