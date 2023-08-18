import argparse
import codecs
import os
from typing import List

import frida
from frida_tools.application import ConsoleApplication


class UIOpenApplication(ConsoleApplication):
    def _initialize(self, parser: argparse.ArgumentParser, options: argparse.Namespace, args: List[str]) -> None:
        self.url = options.url

    def _usage(self) -> str:
        return 'A frida command-line tool that supports iOS devices that attempt to open resources at a specified ' \
               'URL. (openURL)\n%(prog)s [options] URL\n%(prog)s <command> [options] [<args>]'

    def _add_options(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("url", help="A URL (Universal Resource Locator). UIKit supports many common schemes, "
                                        "including the http, https, tel, facetime, and mailto schemes.")

    def is_ios_device(self) -> bool:
        params = self._device.query_system_parameters()
        system = params['os']['id']
        return system == 'ios'

    def _needs_target(self) -> bool:
        return False

    def _start(self) -> None:
        try:
            if not self.is_ios_device():
                self._update_status("This command tool only supports iOS system devices.")
                self._exit(-1)
                return

            sp = frida.get_usb_device().get_process("SpringBoard")
            self._attach(sp.pid)
            data_dir = os.path.dirname(__file__)
            with codecs.open(os.path.join(data_dir, "uiopen_agent.js"), "r", "utf-8") as f:
                source = f.read()

            assert self._session is not None
            script = self._session.create_script(name="uiopen", source=source)
            self._on_script_created(script)
            script.load()
            result = script.exports_sync.uiopen(self.url)
            if result['code'] != 0:
                self._update_status(result['message'])
                self._exit(-1)
                return
            self._exit(0)
        except Exception as e:
            self._update_status(f"{e}")
            self._exit(1)
            return


def main() -> None:
    app = UIOpenApplication()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
