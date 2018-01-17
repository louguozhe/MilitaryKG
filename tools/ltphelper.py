#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import codecs
import sys

from ctypes import *  # Python的一个外部库，提供和C语言兼容的数据类型，可以很方便地调用C DLL中的函数.访问dll，首先需引入ctypes库

libFile = './nlpir/NLPIR32.dll'
dll = CDLL(libFile)


def loadFun(exportName, restype, argtypes):
    global dll
    f = getattr(dll, exportName)
    f.restype = restype
    f.argtypes = argtypes
    return f


class ENCODING:
    GBK_CODE = 0  # 默认支持GBK编码
    UTF8_CODE = GBK_CODE + 1  # UTF8编码
    BIG5_CODE = GBK_CODE + 2  # BIG5编码
    GBK_FANTI_CODE = GBK_CODE + 3  # GBK编码，里面包含繁体字


class SegAtom(Structure):
    _fields_ = [("start", c_int32), ("length", c_int32),
                ("sPOS", c_char * 40), ("iPOS", c_int32),
                ("word_ID", c_int32), ("word_type", c_int32), ("weight", c_int32)
                ]


Init = loadFun('NLPIR_Init', c_int, [c_char_p, c_int, c_char_p])
ParagraphProcessA = loadFun('NLPIR_ParagraphProcessA', POINTER(SegAtom), [c_char_p, c_void_p, c_bool])

if not Init('', ENCODING.UTF8_CODE, ''):
    print("Initialization failed!")
    exit(-111111)


def segment(paragraph):
    count = c_int32()
    result = ParagraphProcessA(paragraph, byref(count), c_bool(True))
    count = count.value
    atoms = cast(result, POINTER(SegAtom))
    return [atoms[i] for i in range(0, count)]


def Seg(paragraph):
    atoms = segment(paragraph)  # 调用segment()
    for a in atoms:
        if len(a.sPOS) < 1: continue
        i = paragraph[a.start: a.start + a.length]  # .decode('utf-8')#.encode('type')
        yield (i, a.sPOS)


if __name__ == "__main__":
    for j in range(1, 10):
        for i in range(10, 1005):
            try:
                f = codecs.open('/Users/Administrator/Desktop/traintxt500/%d/%d.txt' % (j, i), 'r', "gb2312")
                p = f.read().encode("utf-8")  # 读入txt文件的所有内容
                print(j, i)
                for t in Seg(p):
                    s = '%s\t%s' % (t[0], t[1])  # 把一条分词结果赋给s,包括词性
                    b = open('/Users/Administrator/Desktop/wordsegresult500/%d/%d.txt' % (j, i), 'a')
                    b.write(s)
                    b.close()
                    b = open('/Users/Administrator/Desktop/wordsegresult500/%d/%d.txt' % (j, i), 'a')
                    b.write('\n')
                    b.close()
            except:
                continue