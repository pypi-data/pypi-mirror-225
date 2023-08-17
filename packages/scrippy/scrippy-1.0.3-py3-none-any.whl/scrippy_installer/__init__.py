import os
import sys
import logging
import argparse
import subprocess
import yaml
from scrippy_installer import logger
from scrippy_installer.error import ScrippyCoreError


def load_default():
  logging.info("[+] Loading default configuration")
  home_dir = os.path.expanduser("~")
  env = {"env": {"logdir": os.path.join(home_dir,
                                        ".local/share/scrippy/log"),
                 "histdir": os.path.join(home_dir,
                                         ".local/share/scrippy/hist"),
                 "reportdir": os.path.join(home_dir,
                                           ".local/share/scrippy/reports"),
                 "tmpdir": os.path.join(home_dir,
                                        ".local/share/scrippy/tmp"),
                 "datadir": os.path.join(home_dir,
                                         ".local/share/scrippy/data"),
                 "templatedir": os.path.join(home_dir,
                                             ".local/share/scrippy/templates"),
                 "confdir": os.path.join(home_dir,
                                         ".local/share/scrippy/conf")}}
  return env


def build_config():
  logging.info("[+] Configuration edition")
  env = load_default()
  for key, value in env.get("env").items():
    logging.warning(f"  {key} [{value}]:")
    env["env"][key] = input() or value
  return env


def load_config(config):
  env = load_default()
  logging.info(f"[+] Loading configuration from: {config}")
  if os.path.isfile(config):
    with open(config, mode="r", encoding="utf-8") as conf_file:
      scrippy_conf = yaml.load(conf_file, Loader=yaml.FullLoader)
      for key, value in env.get("env").items():
        env.get("env")[key] = scrippy_conf.get("env").get(key) or value
  else:
    raise ScrippyCoreError(f"File `{config}` not found")
  return env


def install_from_config(config):
  logging.info("[+] Configuration to be installed:")
  logging.warning("  env:")
  for key, value in config.get("env").items():
    logging.warning(f"    {key}: {value}")
  logging.info("Confirm new configuration (overwrite preexisting configuration) [Y/n]")
  resp = input().upper() or "Y"
  if resp == "Y":
    home_dir = os.path.expanduser("~")
    main_config_dir = os.path.join(home_dir, ".config/scrippy")
    main_config_file = os.path.join(main_config_dir, "scrippy.yml")
    os.makedirs(main_config_dir, mode=0o750, exist_ok=True)
    for key, value in config.get("env").items():
      logging.info(f"[+] Creating {key}")
      os.makedirs(value, mode=0o750, exist_ok=True)
    logging.info(f"[+] Saving main configuration file: {main_config_file}")
    with open(main_config_file, mode="w", encoding="utf-8") as scrippy_conf:
      yaml.dump(config, scrippy_conf)
      logging.info("  => Configuration updated.")
      install_scrippy_packages()
  else:
    logging.info("  => Installation cancelled")


def install_scrippy_packages():
  logging.info("[+] Installing Scrippy packages")
  packages = ["scrippy-core",
              "scrippy-remote",
              "scrippy-api",
              "scrippy-template",
              "scrippy-db",
              "scrippy-mail",
              "scrippy-git",
              "scrippy-snmp"]
  subprocess.check_call([sys.executable,
                         "-m",
                         "pip",
                         "install",
                         "--upgrade",
                         *packages])


def install(interactive=False, config=None):
  if not interactive and config is None:
    return install_from_config(config=load_default())
  if not interactive and config is not None:
    return install_from_config(config=load_config(config=config))
  if interactive:
    return install_from_config(config=build_config())


def parse_args():
  parser = argparse.ArgumentParser(prog="scrippy",
                                   description="Scrippy framework installation and configuration helper.")
  subparsers = parser.add_subparsers()
  inst = subparsers.add_parser("install")
  inst.add_argument("-i",
                    "--interactive",
                    action="store_true",
                    required=False,
                    help="Optional. Prompt for configuration values.")
  inst.add_argument("-c",
                    "--config",
                    required=False,
                    help="Optional. Configure Scrippy framework according to specified YAML file.")
  args = parser.parse_args()
  try:
    if args.interactive and args.config is not None:
      logging.critical("Error: --interactive and --config options are mutually exclusive")
      inst.print_help()
      sys.exit(1)
  except AttributeError:
    logging.critical("Error: missing keyword or option")
    inst.print_help()
    sys.exit(1)
  return args


def main():
  log_manager = logger.Manager()
  log_manager.set_log_level(logging.INFO)
  args = parse_args()
  install(interactive=args.interactive,
          config=args.config)


if __name__ == "__main__":
  main()
