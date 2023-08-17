import os
import sys
import logging
import coloredlogs


class Manager:
  terms = ["linux", "xterm", "xterm-256color"]
  console_fmt = '%(message)s'
  c_level_styles = {'debug': {'color': 'white'},
                    'info': {'color': 'green'},
                    'warning': {'color': 'yellow'},
                    'error': {'color': 'red'},
                    'critical': {'bold': True, 'color': 'red'}}

  def __init__(self):
    self.handlers = {}
    self._set_default()
    self.logger = logging.getLogger("scrippy.main")

  def _set_default(self):
    console_handler = logging.StreamHandler(sys.stdout)
    if "TERM" in os.environ and os.environ["TERM"] in self.terms:
      console_handler.setFormatter(
          coloredlogs.ColoredFormatter(fmt=self.console_fmt,
                                       level_styles=self.c_level_styles))
    else:
      console_handler.setFormatter(logging.Formatter(fmt=self.console_fmt))
    logging.basicConfig(level=logging.INFO,
                        handlers=[console_handler])

  def set_log_level(self, level):
    self.logger.setLevel(level)
