#!/usr/bin/env python
#
# Copyright (c) 2016 Cisco and/or its affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
# l
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import importlib
import sys

import callback_gen
import notification_gen
import dto_gen
import jvpp_callback_facade_gen
import jvpp_future_facade_gen
import jvpp_impl_gen
import jvpp_c_gen
import util

# Invocation:
# ~/Projects/vpp/vpp-api/jvpp/gen$ mkdir -p java/org/openvpp/jvpp && cd java/org/openvpp/jvpp
# ~/Projects/vpp/vpp-api/jvpp/gen/java/org/openvpp/jvpp$ ../../../../jvpp_gen.py -idefs_api_vpp_papi.py
#
# Compilation:
# ~/Projects/vpp/vpp-api/jvpp/gen/java/org/openvpp/jvpp$ javac *.java dto/*.java callback/*.java
#
# where
# defs_api_vpp_papi.py - vpe.api in python format (generated by vppapigen)
from util import vpp_2_jni_type_mapping

parser = argparse.ArgumentParser(description='VPP Java API generator')
parser.add_argument('-i', action="store", dest="inputfile")
args = parser.parse_args()

sys.path.append(".")

inputfile = args.inputfile.replace('.py', '')
cfg = importlib.import_module(inputfile, package=None)


# FIXME: functions unsupported due to problems with vpe.api
def is_supported(f_name):
    return f_name not in {'vnet_ip4_fib_counters', 'vnet_ip6_fib_counters'}


def is_request_field(field_name):
    return field_name not in {'_vl_msg_id', 'client_index', 'context'}


def is_response_field(field_name):
    return field_name not in {'_vl_msg_id'}


def get_args(t, filter):
    arg_list = []
    for i in t:
        if not filter(i[1]):
            continue
        arg_list.append(i[1])
    return arg_list


def get_types(t, filter):
    types_list = []
    c_types_list = []
    lengths_list = []
    for i in t:
        if not filter(i[1]):
            continue
        if len(i) is 3:  # array type
            types_list.append(vpp_2_jni_type_mapping[i[0]] + 'Array')
            c_types_list.append(i[0] + '[]')
            lengths_list.append((i[2], False))
        elif len(i) is 4:  # variable length array type
            types_list.append(vpp_2_jni_type_mapping[i[0]] + 'Array')
            c_types_list.append(i[0] + '[]')
            lengths_list.append((i[3], True))
        else:  # primitive type
            types_list.append(vpp_2_jni_type_mapping[i[0]])
            c_types_list.append(i[0])
            lengths_list.append((0, False))
    return types_list, c_types_list, lengths_list


def get_definitions():
    # Pass 1
    func_list = []
    func_name = {}
    for a in cfg.vppapidef:
        if not is_supported(a[0]):
            continue

        java_name = util.underscore_to_camelcase(a[0])

        # For replies include all the arguments except message_id
        if util.is_reply(java_name):
            types, c_types, lengths = get_types(a[1:], is_response_field)
            func_name[a[0]] = dict(
                [('name', a[0]), ('java_name', java_name),
                 ('args', get_args(a[1:], is_response_field)), ('full_args', get_args(a[1:], lambda x: True)),
                 ('types', types), ('c_types', c_types), ('lengths', lengths)])
        # For requests skip message_id, client_id and context
        else:
            types, c_types, lengths = get_types(a[1:], is_request_field)
            func_name[a[0]] = dict(
                [('name', a[0]), ('java_name', java_name),
                 ('args', get_args(a[1:], is_request_field)), ('full_args', get_args(a[1:], lambda x: True)),
                 ('types', types), ('c_types', c_types), ('lengths', lengths)])

        # Indexed by name
        func_list.append(func_name[a[0]])
    return func_list, func_name


func_list, func_name = get_definitions()

base_package = 'org.openvpp.jvpp'
dto_package = 'dto'
callback_package = 'callback'
notification_package = 'notification'
future_package = 'future'
# TODO find better package name
callback_facade_package = 'callfacade'

dto_gen.generate_dtos(func_list, base_package, dto_package, args.inputfile)
jvpp_impl_gen.generate_jvpp(func_list, base_package, dto_package, args.inputfile)
callback_gen.generate_callbacks(func_list, base_package, callback_package, dto_package, args.inputfile)
notification_gen.generate_notification_registry(func_list, base_package, notification_package, callback_package, dto_package, args.inputfile)
jvpp_c_gen.generate_jvpp(func_list, args.inputfile)
jvpp_future_facade_gen.generate_jvpp(func_list, base_package, dto_package, callback_package, notification_package, future_package, args.inputfile)
jvpp_callback_facade_gen.generate_jvpp(func_list, base_package, dto_package, callback_package, notification_package, callback_facade_package, args.inputfile)
