# Copyright (c) 2021-2022 The BlitzManager project Authors. All rights reserved. Use of this
# source code is governed by a BSD-style license that can be found in the LICENSE file.

import argparse


class ArgumentsParser(object):

    def __init__(self, prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=None,
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True,
                 allow_abbrev=True):
        """

        :param prog:
        :param usage:
        :param description:
        :param epilog:
        :param parents:
        :param formatter_class:
        :param prefix_chars:
        :param fromfile_prefix_chars:
        :param argument_default:
        :param conflict_handler:
        :param add_help:
        :param allow_abbrev:
        """
        if parents is None:
            parents = []
        self.flags = []
        self.__parser = argparse.ArgumentParser(prog=prog,
                                                usage=usage,
                                                description=description,
                                                epilog=epilog,
                                                parents=parents,
                                                formatter_class=formatter_class,
                                                prefix_chars=prefix_chars,
                                                fromfile_prefix_chars=fromfile_prefix_chars,
                                                argument_default=argument_default,
                                                conflict_handler=conflict_handler,
                                                add_help=add_help,
                                                allow_abbrev=allow_abbrev)

    def add_flag(self, flag_name: str, *args, **kwargs):
        """

        :param flag_name:
        :param args:
        :param kwargs:
        :return:
        """
        if flag_name.replace("-", "") in self.flags:
            raise RuntimeError(f"Flag {flag_name} already exist")
        self.flags.append(flag_name.replace("-", ""))

        self.__parser.add_argument(flag_name, *args, **kwargs)

    def parse(self, args=None, namespace=None):
        """

        :param args:
        :param namespace:
        :return:
        """

        return self.__parser.parse_args(args=args, namespace=namespace)


__all__ = ["ArgumentsParser"]
