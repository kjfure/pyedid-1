#! /usr/bin/env python
# -*-coding:utf-8-*-
import os
import platform
import binascii
import time
import socket
import datetime


def _get_edid(edid):
    compress_ascii = {'00001': 'A', '00010': 'B', '00011': 'C', '00100': 'D', '00101': 'E', '00110': 'F',
                      '00111': 'G', '01000': 'H', '01001': 'I', '01010': 'J', '01011': 'K', '01100': 'L',
                      '01101': 'M', '01110': 'N', '01111': 'O', '10000': 'P', '10001': 'Q', '10010': 'R',
                      '10011': 'S', '10100': 'T', '10101': 'U', '10110': 'V', '10111': 'W', '11000': 'X',
                      '11001': 'Y', '11010': 'Z', '11011': '', '11100': '', '11101': '', '11110': '',
                      '11111': '', '00000': ''}
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                  11: 'Nov', 12: 'Dec'}
    tmp_bin = ''
    for i in edid[16:20]:
        tmp_bin += bin(int(i, 16)).replace('0b', '').zfill(4)
    manufacturer = "%s%s%s" % (
        compress_ascii[tmp_bin[1:6]], compress_ascii[tmp_bin[6:11]], compress_ascii[tmp_bin[11:16]])
    week = int(edid[32:34], 16)
    year = int(edid[34:36], 16) + 1990
    month = week * 7 / 30
    date_of_Mfg = "%s.%s(%s)" % (year, month, month_dict[month])
    sn = binascii.unhexlify(edid[152:180]).replace('\n', '').replace('\x00', '')
    model = binascii.unhexlify(edid[188:214]).replace('\n', '').replace('\x00', '')

    return {'manufacturer': manufacturer, 'model': model, 'sn': sn, 'date_of_Mfg': date_of_Mfg}


def get_monitor_info():

    hostname = socket.getfqdn()

    if platform.system() == "Linux":
        edid_dict = {}
        display_dict = {}

        xrandr_info = os.popen('xrandr --prop').read().split('\n')
        tmp_num = 0
        for info in xrandr_info:
            if '\t\t' in info:
                display_dict[tmp_num][-1] += info.replace('\t', '')
            elif '\t' in info or '   ' in info:
                display_dict[tmp_num].append(info.replace('\t', ''))
            else:
                tmp_num += 1
                display_dict[tmp_num] = []
                display_dict[tmp_num].append(info.replace('\t', ''))

        tmp_num = 0
        for key in display_dict.keys():
            line_tmp = display_dict[key][0].split('(')
            tmp = line_tmp[0].split(' ')
            if not tmp[0]:
                break
            if tmp[1] == 'connected':
                tmp_num += 1
                edid_dict[tmp_num] = {}
                edid_dict[tmp_num]['port'] = tmp[0]
                if tmp[2] == 'primary':
                    edid_dict[tmp_num]['connect'] = 'primary'
                else:
                    edid_dict[tmp_num]['connect'] = 'normal'
                if tmp[-2] in ['left', 'right', 'inverted']:
                    edid_dict[tmp_num]['rotate'] = tmp[-2]
                else:
                    edid_dict[tmp_num]['rotate'] = 'normal'
                if 'x' in tmp[-2]:
                    edid_dict[tmp_num]['resolution'] = tmp[-2]
                elif 'x' in tmp[-3]:
                    edid_dict[tmp_num]['resolution'] = tmp[-3]
                else:
                    edid_dict[tmp_num]['resolution'] = ''
                size = line_tmp[-1].split(')')[-1].split('x')
                edid_dict[tmp_num]['height'] = size[0]
                edid_dict[tmp_num]['width'] = size[1]
                for i in display_dict[key]:
                    if ':' in i:
                        tmp = i.split(':')
                        if len(tmp[1:]) > 1:
                            edid_dict[tmp_num][tmp[0]] = i
                        else:
                            edid_dict[tmp_num][tmp[0]] = tmp[1].replace(' ', '')
                edid_dict[tmp_num] = dict(_get_edid(edid_dict[tmp_num]['EDID']).items() + edid_dict[tmp_num].items())
        # with open('/tmp/monitor.info', 'w') as f:
        #     f.write('')

        info = ''
        for key in edid_dict.keys():
            info += "%s: %s\t%s\t%s\t%s\t%s\t%s\t%s\r\n" % (
            key, edid_dict[key]['model'], edid_dict[key]['port'], edid_dict[key]['connect'], edid_dict[key]['sn'],
            edid_dict[key]['date_of_Mfg'], hostname, datetime.datetime.now())
            # with open('/tmp/monitor.info', 'a') as f:
            #     f.write(str(info))
    return info
