#! /usr/bin/env python
# Copyright 2016 to 2022, Cisco Systems, Inc., all rights reserved.
import os
import sys
import logging
import traceback
from collections import OrderedDict
import itertools
import subprocess
from pathlib import Path
import shutil
from distutils import sysconfig
from six import string_types
from copy import deepcopy
from sly import Lexer
from grpc_tools import protoc

log = logging.getLogger('__name__')

class ProtoParserException(Exception):
    pass


class ProtoLexer(Lexer):
    """Token class that defines protobuf tokens."""

    # Set of token names.  This is always required before token rules
    tokens = {ID, SERVICE, RPC, MESSAGE, COMMENT, NEWLINE, LBRACE, RBRACE,
              LPAREN, RPAREN, LESS, GREATER, COMMA, SEMICOLON, DOT, TICK,
              EQUAL, SERVICE, RPC, MESSAGE, SYNTAX, PACKAGE, IMPORT, OPTION,
              EXTEND, RETURNS, STREAM, STRING, UINT32, INT32, UINT64, INT64,
              BOOL, BYTES, MAP, REPEATED, ENUM, ONEOF, BYTES} # noqa

    # String containing ignored characters between tokens
    ignore = ' \t\r'

    # Regular expression rules for tokens
    COMMENT = r'\/\/'
    NEWLINE = r'\n'
    LBRACE = r'{'
    RBRACE = r'}'
    LPAREN = r'\('
    RPAREN = r'\)'
    LESS = r'\<'
    GREATER = r'\>'
    COMMA = r'\,'
    SEMICOLON = r'\;'
    DOT = r'\.'
    TICK = r"'"
    EQUAL = r'='
    ID = r'[a-zA-Z0-9\"\.\,\:\/_\-\[\]\|\+&][a-zA-Z0-9\"\.\:\/_\-\[\]\|\+&]*'
    ID['service'] = SERVICE # noqa
    ID['rpc'] = RPC # noqa
    ID['message'] = MESSAGE # noqa
    ID['syntax'] = SYNTAX # noqa
    ID['package'] = PACKAGE # noqa
    ID['import'] = IMPORT # noqa
    ID['option'] = OPTION # noqa
    ID['extend'] = EXTEND # noqa
    ID['returns'] = RETURNS # noqa
    ID['stream'] = STREAM # noqa
    ID['string'] = STRING # noqa
    ID['uint32'] = UINT32 # noqa
    ID['int32'] = INT32 # noqa
    ID['uint64'] = UINT64 # noqa
    ID['int64'] = INT64 # noqa
    ID['bool'] = BOOL # noqa
    ID['bytes'] = BYTES # noqa
    ID['map'] = MAP # noqa
    ID['repeated'] = REPEATED # noqa
    ID['enum'] = ENUM # noqa
    ID['oneof'] = ONEOF # noqa
    ID['bytes'] = BYTES # noqa


class ProtoParser:
    """Token parser logic to build jsTree."""

    # Should be at least package and syntax defined.
    #
    # syntax "proto3";
    # package gnoi.A;
    #
    MINIMUM_PROTO_SIZE = 35
    REQUIRED_CONTENT = ['syntax ', 'package ']
    SKIP = [
        'SYNTAX',
        'PACKAGE',
        'OPTION',
        'EXTEND'
    ]
    DATATYPE = [
        'STRING',
        'UINT32',
        'INT32',
        'UINT64',
        'INT64',
        'BOOL',
        'BYTES',
    ]

    def __init__(self, counter=None):
        self.lexer = ProtoLexer()
        if counter is None:
            self.cntr = itertools.count(1)
        else:
            self.cntr = counter
        self.data = ''
        self.service_name = 'No service'
        self.service_comment = ''
        self.imports = []
        self.service = {
            'id': next(self.cntr),
            'text': '',
            'data': {'comment': ''},
            'children': [
                {
                    'id': next(self.cntr),
                    'text': 'rpcs',
                    'children': []
                }
            ]
        }
        self.rpcs = []
        self.messages = OrderedDict()
        self.enums = OrderedDict()
        self.oneofs = []
        self.tree = OrderedDict()

    def _validate_proto_str(self, proto_str):
        if not isinstance(proto_str, string_types):
            raise ProtoParserException(
                'Invalid string: {0}'.format(str(proto_str))
            )
        if len(proto_str) < self.MINIMUM_PROTO_SIZE:
            raise ProtoParserException(
                'Not enough content in proto file to be valid.'
            )
        for item in self.REQUIRED_CONTENT:
            if item not in proto_str:
                raise ProtoParserException(
                    'Proto file must have at least one {0}'.format(item)
                )

    def parse_from_file(self, proto_path):
        if not os.path.isfile(proto_path):
            raise ProtoParserException(
                'File path invalid: {0}'.format(proto_path)
            )
        self.service_name = proto_path[
            proto_path.rfind('/')+1: proto_path.rfind('.proto')
        ]
        self.data = open(proto_path).read()
        self._validate_proto_str(self.data)
        self.process_proto()

    def parse_from_str(self, proto_str):
        self.data = proto_str
        self._validate_proto_str(self.data)
        self.process_proto()

    def process_proto(self, proto_str=None):
        comment = ''
        index = ''
        import_proto = ''
        in_comment = False
        in_skip = False
        in_service = False
        in_rpc = False
        rpc_name = ''
        rpc_stream = False
        rpc = {}
        in_message = False
        message = ''
        message_child = {}
        datatype = ''
        in_enum = False
        enum_name = ''
        enum_child = {}
        in_repeated = False
        in_import = False
        in_oneof = False
        oneof_name = ''
        in_map = False
        map_first = {}
        map_second = {}
        in_equal = False

        if proto_str is not None:
            self._validate_proto_str(proto_str)
            self.data = proto_str

        for token in self.lexer.tokenize(self.data):

            if token.type == 'COMMENT':
                in_comment = True
            elif token.type != 'NEWLINE' and in_comment:
                if not in_skip:
                    comment += token.value + ' '
            elif token.type == 'NEWLINE':
                in_comment = False
                in_equal = False
                in_skip = False
            elif token.type in self.SKIP:
                in_skip = True
                comment = ''
            elif token.type == 'EQUAL':
                in_equal = True
            elif token.type == 'IMPORT':
                in_import = True
            elif token.type == 'SEMICOLON':
                if in_service and in_rpc and rpc:
                    # rpc can end with "{}" or ";"
                    self.rpcs.append(rpc)
                    rpc = {}
                    in_rpc = False
                    rpc_name = ''
                continue
            elif in_skip:
                continue
            elif token.type == 'SERVICE':
                self.service_comment = comment
                comment = ''
                in_service = True
            elif token.type == 'RPC':
                in_rpc = True
            elif token.type == 'STREAM' and in_rpc:
                rpc_stream = True
            elif token.type == 'MESSAGE':
                in_message = True
            elif token.type in self.DATATYPE:
                if in_map:
                    if not map_first:
                        map_first = {
                            'text': 'name',
                            'data': {
                                'nodetype': 'map_name',
                                'datatype': token.value
                            }
                        }
                    elif not map_second:
                        map_second = {
                            'text': 'value',
                            'data': {
                                'nodetype': 'map_value',
                                'datatype': token.value
                            }
                        }
                        datatype = 'map'
                else:
                    datatype = token.value
            elif token.type == 'ENUM':
                in_enum = True
            elif token.type == 'ONEOF':
                in_oneof = True
            elif token.type == 'REPEATED':
                in_repeated = True
            elif token.type == 'MAP':
                in_map = True
            elif token.type == 'ID':
                if in_equal and any((in_message, in_enum)):
                    index = token.value
                elif in_import:
                    comment = ''
                    import_proto = token.value
                    if '/' in import_proto:
                        import_proto = import_proto[import_proto.rfind('/')+1:]
                        import_proto = import_proto.replace('"', '')
                    in_import = False
                    if import_proto in self.imports:
                        import_proto = ''
                        continue
                    prp = ProtoParser(counter=self.cntr)
                    prp.imports = self.imports
                    try:
                        prp.parse_from_file(import_proto)
                    except ProtoParserException:
                        log.warning(
                            'Imported {0} not found'.format(import_proto)
                        )
                    self.cntr = prp.cntr
                    self.messages.update(prp.messages)
                    self.enums.update(prp.enums)
                    self.imports.append(import_proto)
                    import_proto = ''

                elif in_service:
                    if in_rpc:
                        if not rpc_name:
                            rpc_name = token.value
                            rpc = {
                                'id': next(self.cntr),
                                'text': rpc_name,
                                'data': {
                                    'name': rpc_name,
                                    'service': self.service_name,
                                    'comment': comment,
                                    'nodetype': 'rpc',
                                },
                                'children': []
                            }
                            comment = ''
                        elif len(rpc['children']) == 0:
                            rpc['children'].append({
                                'id': next(self.cntr),
                                'text': token.value,
                                'data': {
                                    'name': token.value,
                                    'rpc': rpc_name,
                                    'service': self.service_name,
                                    'comment': comment,
                                    'nodetype': 'request',
                                    'stream': str(rpc_stream)
                                }
                            })
                            comment = ''
                            rpc_stream = False
                        elif len(rpc['children']) == 1:
                            rpc['children'].append({
                                'id': next(self.cntr),
                                'text': token.value,
                                'data': {
                                    'name': token.value,
                                    'rpc': rpc_name,
                                    'service': self.service_name,
                                    'comment': comment,
                                    'nodetype': 'response',
                                    'stream': str(rpc_stream)
                                }
                            })
                            comment = ''
                            rpc_stream = False
                    else:
                        self.service['text'] = token.value

                elif in_enum:
                    if not enum_name:
                        enum_name = token.value
                        self.enums.update({
                            enum_name: {
                                'id': next(self.cntr),
                                'text': enum_name,
                                'data': {
                                    'name': enum_name,
                                    'comment': comment,
                                    'nodetype': 'parameter',
                                    'datatype': 'enum',
                                    'options': []
                                },
                                'children': []
                            }
                        })
                        comment = ''
                        continue
                    else:
                        if enum_child:
                            self.enums[enum_name]['data']['options'].append(
                                [index, enum_child, comment]
                            )
                        enum_child = token.value
                        index = ''
                        comment = ''

                elif in_message:
                    if not message:
                        message = token.value
                        self.messages.update({
                            message: {
                                'id': next(self.cntr),
                                'text': message,
                                'data': {
                                    'name': message,
                                    'comment': comment,
                                    'nodetype': 'message'
                                }
                            }
                        })
                        comment = ''
                        continue
                    if in_oneof:
                        if not oneof_name:
                            oneof_name = token.value
                            oneof = {
                                'id': next(self.cntr),
                                'text': token.value,
                                'data': {
                                    'name': oneof_name,
                                    'index': '',
                                    'comment': '',
                                    'oneof': oneof_name,
                                    'nodetype': 'oneof',
                                    'datatype': 'oneof',
                                    'message': message
                                },
                                'children': []
                            }
                            if 'children' in self.messages[message]:
                                self.messages[message]['children'].append(
                                    oneof
                                )
                            else:
                                self.messages[message]['children'] = [
                                    oneof
                                ]
                            self.oneofs.append(oneof)
                            continue
                        if oneof and message_child:
                            message_child['data']['index'] = index
                            message_child['data']['comment'] = comment
                            oneof['children'].append(message_child)
                            index = ''
                            comment = ''
                            message_child = {}

                    if datatype:
                        if message_child:
                            message_child['data']['index'] = index
                            message_child['data']['comment'] = comment
                            if 'children' in self.messages[message]:
                                self.messages[message]['children'].append(
                                    message_child
                                )
                            else:
                                self.messages[message]['children'] = [
                                    message_child
                                ]
                            index = ''
                            comment = ''
                        message_child = {
                            'id': next(self.cntr),
                            'text': token.value,
                            'data': {
                                'name': token.value,
                                'comment': '',
                                'index': '',
                                'nodetype': 'parameter',
                                'datatype': datatype,
                                'message': message
                            }
                        }
                        if datatype == 'bool':
                            message_child['data']['options'] = [
                                ['true', True, ''],
                                ['false', False, '']
                            ]
                        if in_map and map_first and map_second:
                            map_first['data']['map'] = token.value
                            map_second['data']['map'] = token.value
                            message_child['children'] = [map_first, map_second]
                            in_map = False
                            map_first = {}
                            map_second = {}
                        if in_repeated:
                            message_child['data']['repeated'] = True
                            in_repeated = False
                        comment = ''
                        datatype = ''
                    else:
                        datatype = token.value

            elif token.type == 'LBRACE':
                if in_service:
                    self.service['data']['comment'] = comment
                    comment = ''
                continue
            elif token.type == 'RBRACE':
                if in_service and in_rpc:
                    self.rpcs.append(rpc)
                    rpc = {}
                    in_rpc = False
                    rpc_name = ''
                elif in_service:
                    in_service = False
                    comment = ''
                elif in_enum:
                    if enum_child:
                        self.enums[enum_name]['data']['options'].append(
                            [index, enum_child, comment]
                        )
                    index = ''
                    comment = ''
                    in_enum = False
                    enum_name = ''
                    enum_child = {}
                    datatype = ''
                elif in_message:
                    if in_oneof:
                        if oneof and message_child:
                            message_child['data']['index'] = index
                            message_child['data']['comment'] = comment
                            oneof['children'].append(message_child)

                    if message_child:
                        message_child['data']['index'] = index
                        message_child['data']['comment'] = comment
                        if in_map:
                            message_child['children'] = [map_first, map_second]
                            map_first = {}
                            map_second = {}
                            datatype = ''
                            in_map = False
                        if 'children' in self.messages[message]:
                            self.messages[message]['children'].append(
                                message_child
                            )
                        else:
                            self.messages[message]['children'] = [
                                message_child
                            ]
                    index = ''
                    comment = ''
                    in_message = False
                    datatype = ''
                    message = ''
                    message_child = {}
                    in_map = False
                    in_oneof = False
                    oneof_name = ''

    def _get_messages_for_rpcs(self):
        if self.rpcs:
            for key in self.messages.keys():
                for rpc in self.rpcs:
                    children = []
                    for idx, ch in enumerate(rpc.get('children', [])):
                        ch['data']['rpc'] = rpc['data']['name']
                        if idx == 0:
                            ch['data']['nodetype'] = 'request'
                        else:
                            ch['data']['nodetype'] = 'response'
                        if ch.get('text', '') == key:
                            children.append(self.messages[key])
                        else:
                            children.append(ch)
                        for c in ch.get('children', []):
                            c['data']['rpc'] = rpc['data']['name']

                    if 'children' in rpc:
                        rpc['children'] = children

    def _get_nested_messages(self, items={}):
        for key in self.messages.keys():
            for chkey in items.keys():
                children = []
                for ch in self.messages[key].get('children', []):
                    dt = ch['data'].get('datatype', '')
                    if dt[dt.find('.')+1:] == chkey:
                        ch['data']['messagetype'] = dt
                        if 'options' in items[chkey]['data']:
                            ch['data']['options'] = items[chkey]['data'][
                                'options'
                            ]
                            ch['data']['datatype'] = items[chkey]['data'][
                                'datatype'
                            ]
                        else:
                            ch['children'] = items[chkey]['children']
                    children.append(deepcopy(ch))
                if children:
                    self.messages[key]['children'] = children

    def _get_nested_oneofs(self):
        for oneof in self.oneofs:
            for ch in oneof.get('children'):
                if ch['data'].get('datatype') in self.messages:
                    ch['children'] = [self.messages[ch['data']['datatype']]]

    def to_tree(self):
        if self.messages:
            self._get_nested_messages(self.messages)
            self._get_nested_messages(self.enums)
            self._get_nested_oneofs()
        if self.rpcs:
            self._get_messages_for_rpcs()
            self.service['children'][0]['children'] = self.rpcs
            self.service['data'] = {'comment': self.service_comment}
        else:
            self.service = {
                'id': 0,
                'text': self.service_name,
                'nodetype': 'service',
                'data': {'comment': self.service_comment},
                'children': []
            }
            if self.enums:
                enums = {
                    'id': next(self.cntr),
                    'text': 'enums',
                    'nodetype': 'enum',
                    'data': 'Defined ENUMs',
                    'children': [v for v in self.enums.values()]
                }
                self.service['children'].append(enums)
            if self.messages:
                messages = {
                    'id': next(self.cntr),
                    'text': 'messages',
                    'nodetype': 'message',
                    'data': {'comment': 'Defined messages'},
                    'children': [v for v in self.messages.values()]
                }
                self.service['children'].append(messages)

        return self.service


class ProtoCompile:
    """Parse proto file and generate python libraries.

    GNOI_GIT_DIR == path to gnoi cloned proto files.
    GNOI_PROTO_DIR == path to output python modules to.
    proto == proto file name without ".proto"
    proto_dir == path to input proto file.

    pc = ProtoCompile(proto_name, proto_dir, GNOI_GIT_DIR, GNOI_PROTO_DIR)
    pc.compile_libs()

    """
    def __init__(self, proto, proto_dir, compile_dir, output=None):
        self.proto_name = proto.replace('.proto', '')
        if output is None:
            output = os.getcwd()
        self.proto_lib = os.path.join(output, proto.replace('.proto', ''))
        self.proto_file = os.path.join(proto_dir, proto)
        self.compile_dir = compile_dir
        self.proto_dir = proto_dir
        self.output_dir = output

    def fixup_proto_imports(self, protos=[]):
        fixup = []
        import_protos = []

        for proto in protos:
            if proto in os.listdir(self.tmpdir):
                continue
            if not os.path.exists(
                os.path.join(self.proto_dir, proto)
            ):
                log.info('Import {0} not found'.format(proto))
                continue
            proto_str = open(os.path.join(self.proto_dir, proto)).read()

            for line in proto_str.splitlines():
                if line.startswith('import'):
                    import_proto = line[
                        line.rfind('/')+1:
                    ].strip().replace('";', '')
                    if import_proto not in self.import_protos:
                        import_protos.append(import_proto)
                        self.import_protos.append(import_proto)
                    line = 'import "' + import_proto + '";'
                fixup.append(line)
            open(os.path.join(self.tmpdir, proto), 'w').write('\n'.join(fixup))
            fixup = []
        if import_protos:
            self.fixup_proto_imports(import_protos)

    def fixup_python_imports(self, proto):
        fixup = []

        if not os.path.exists(self.proto_file):
            log.info('Import {0} module not found'.format(proto))
            return
        proto_str = open(proto).read()
        for line in proto_str.splitlines():
            if line and line.startswith('from') and \
                'google.protobuf' not in line and \
                    not line.endswith(' grpc'):
                lsplt = line.split()
                lsplt[1] = '.'
                line = ' '.join(lsplt)
            fixup.append(line)
        open(proto, 'w').write('\n'.join(fixup))

    def compile_command(self):
        # _proto = os.path.join(
        #     sysconfig.get_python_lib(),
        #     'grpc_tools',
        #     '_proto'
        # )
        cmd = [
            'python',
            '-m',
            'grpc_tools.protoc',
            '--proto_path=' + self.compile_dir,
            '--proto_path=' + self.proto_dir,
            '--python_out=' + self.output_dir,
            '--grpc_python_out=' + self.output_dir,
            self.proto_file
        ]
        # for imp_proto in reversed(self.import_protos):
        #     if imp_proto == 'descriptor.proto':
        #         continue
        #     cmd.append(os.path.join(self.tmpdir, imp_proto))
        #     result = protoc.main(cmd)
        #     log.info(result)
        #     cmd.pop()
        # cmd.append(os.path.join(self.tmpdir, proto))
        # result = protoc.main(cmd)
        result = subprocess.run(cmd)
        log.info(result)

    def relocate_libs(self):
        if os.path.isdir(os.path.join(self.output_dir, self.proto_name)):
            source = os.path.join(self.output_dir, self.proto_name)
            dest = self.output_dir
            for f in os.listdir(source):
                shutil.copy(os.path.join(source, f), self.output_dir)
            shutil.rmtree(source)

    def compile_libs(self):
        cwd = os.getcwd()
        try:
            os.chdir(self.compile_dir)
            self.compile_command()
            for pfile in os.listdir(self.proto_lib):
                if pfile.endswith('py'):
                    self.fixup_python_imports(
                        os.path.join(self.proto_lib, pfile)
                    )
            self.relocate_libs()
            # Path(os.path.join(self.proto_lib, '__init__.py')).touch()
        except Exception:
            traceback.format_exc()
        finally:
            os.chdir(cwd)
        

if __name__ == '__main__':
    from pprint import pprint as ppr
    if len(sys.argv) == 1:
        print('parse of compile?')
    if sys.argv[1] == 'parse':
        pp = ProtoParser()
        breakpoint()
        pp.parse_from_file('./system.proto')
        ppr(pp.to_tree())
    elif sys.argv[1] == 'compile':
        pc = ProtoCompile('system.proto')
        pc.compile_libs()
    else:
        print('parse of compile?')
