from __future__ import absolute_import
from insights.parsers.lvm import Pvs, PvsHeadings
from insights.tests import context_wrap
from .test_lvm import compare_partial_dicts

FD_LEAK_HEADER = "File descriptor 5 (/dev/null) leaked on invocation. Parent PID 99999: timeout\n"

PVS_INFO = """
    WARNING: Locking disabled. Be careful! This could corrupt your metadata.
    LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='500.00m'|LVM2_PV_NAME='/dev/sda1'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='1'
    LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='JvSULk-ileq-JbuS-GGgg-jkif-thuW-zvFBEl'|LVM2_DEV_SIZE='476.45g'|LVM2_PV_NAME='/dev/sda2'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='1020.00k'|LVM2_PE_START='1.00m'|LVM2_PV_SIZE='476.45g'|LVM2_PV_FREE='4.00m'|LVM2_PV_USED='476.45g'|LVM2_PV_ATTR='a--'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='121971'|LVM2_PV_PE_ALLOC_COUNT='121970'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='1'|LVM2_PV_MDA_USED_COUNT='1'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '

""".strip()

PVS_SDA2_INFO = {
    'Fmt': 'lvm2',
    'PV': '/dev/sda2',
    'PSize': '476.45g',
    'PFree': '4.00m',
    'Attr': 'a--',
    'VG': None,
    '#PMda': '1',
    '#PMdaUse': '1',
    '1st_PE': '1.00m',
    'Alloc': '121970',
    'Allocatable': 'allocatable',
    'BA_size': '0',
    'BA_start': '0',
    'DevSize': '476.45g',
    'Exported': '',
    'Missing': '',
    'PE': '121971',
    'PMdaFree': '0',
    'PMdaSize': '1020.00k',
    'PV_Tags': '',
    'PV_UUID': 'JvSULk-ileq-JbuS-GGgg-jkif-thuW-zvFBEl',
    'Used': '476.45g'
}

PVS_INFO_LONG = """
  WARNING: Locking disabled. Be careful! This could corrupt your metadata.
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data1/lv_brick1'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='28'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data1/lv_hdfs1'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='41'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data2/lv_brick2'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='30'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data2/lv_hdfs2'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='42'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data3/lv_brick3'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='32'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data3/lv_hdfs3'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='43'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data4/lv_brick4'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='34'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data4/lv_hdfs4'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='44'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data5/lv_brick5'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='36'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data5/lv_hdfs5'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='45'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data6/lv_brick6'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='38'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data6/lv_hdfs6'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='46'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data7/lv_brick7'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='40'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='3.62t'|LVM2_PV_NAME='/dev/data7/lv_hdfs7'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='47'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='100.00g'|LVM2_PV_NAME='/dev/loop0'|LVM2_PV_MAJOR='7'|LVM2_PV_MINOR='0'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='2.00g'|LVM2_PV_NAME='/dev/loop1'|LVM2_PV_MAJOR='7'|LVM2_http://m.abc.com/obituaries/2017/apr/10/charles-dietz-2017-04-10/PV_MINOR='1'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='100.00g'|LVM2_PV_NAME='/dev/mapper/docker-253:3-100685290-pool'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='5'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='976.00g'|LVM2_PV_NAME='/dev/rhel_ceehadoop1/home'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='2'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='2.57t'|LVM2_PV_NAME='/dev/rhel_ceehadoop1/opt'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='4'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='50.00g'|LVM2_PV_NAME='/dev/rhel_ceehadoop1/root'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='0'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='16.00g'|LVM2_PV_NAME='/dev/rhel_ceehadoop1/swap'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='1'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='50.00g'|LVM2_PV_NAME='/dev/rhel_ceehadoop1/var'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='3'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='1.00g'|LVM2_PV_NAME='/dev/sda2'|LVM2_PV_MAJOR='8'|LVM2_PV_MINOR='2'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
  LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='3e2mRe-1y3a-iUSj-F3tH-yG1M-t3qD-8uNDf5'|LVM2_DEV_SIZE='3.63t'|LVM2_PV_NAME='/dev/sda3'|LVM2_PV_MAJOR='8'|LVM2_PV_MINOR='3'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='1020.00k'|LVM2_PV_EXT_VSN='2'|LVM2_PE_START='1.00m'|LVM2_PV_SIZE='3.63t'|LVM2_PV_FREE='0 '|LVM2_PV_USED='3.63t'|LVM2_PV_ATTR='a--'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='952831'|LVM2_PV_PE_ALLOC_COUNT='952831'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='1'|LVM2_PV_MDA_USED_COUNT='1'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE='used'|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME='rhel_ceehadoop1'
  LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='dhr134-VxSA-R7dW-op7s-HCco-7J2A-7MvaeN'|LVM2_DEV_SIZE='3.64t'|LVM2_PV_NAME='/dev/sdb1'|LVM2_PV_MAJOR='8'|LVM2_PV_MINOR='17'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='252.00k'|LVM2_PV_EXT_VSN='2'|LVM2_PE_START='256.00k'|LVM2_PV_SIZE='3.64t'|LVM2_PV_FREE='4.00m'|LVM2_PV_USED='3.64t'|LVM2_PV_ATTR='a--'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='953853'|LVM2_PV_PE_ALLOC_COUNT='953852'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='1'|LVM2_PV_MDA_USED_COUNT='1'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE='used'|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME='data1'
  LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='sxTsQE-raAM-8s3b-FSy0-LhL2-Naue-f2ebcA'|LVM2_DEV_SIZE='3.64t'|LVM2_PV_NAME='/dev/sdc1'|LVM2_PV_MAJOR='8'|LVM2_PV_MINOR='33'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='252.00k'|LVM2_PV_EXT_VSN='2'|LVM2_PE_START='256.00k'|LVM2_PV_SIZE='3.64t'|LVM2_PV_FREE='4.00m'|LVM2_PV_USED='3.64t'|LVM2_PV_ATTR='a--'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='953853'|LVM2_PV_PE_ALLOC_COUNT='953852'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='1'|LVM2_PV_MDA_USED_COUNT='1'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE='used'|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME='data2'
  LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='yxj2qs-qOKA-57XF-228r-qWQj-3zez-i0Vaiw'|LVM2_DEV_SIZE='3.64t'|LVM2_PV_NAME='/dev/sdd1'|LVM2_PV_MAJOR='8'|LVM2_PV_MINOR='49'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='252.00k'|LVM2_PV_EXT_VSN='2'|LVM2_PE_START='256.00k'|LVM2_PV_SIZE='3.64t'|LVM2_PV_FREE='4.00m'|LVM2_PV_USED='3.64t'|LVM2_PV_ATTR='a--'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='953853'|LVM2_PV_PE_ALLOC_COUNT='953852'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='1'|LVM2_PV_MDA_USED_COUNT='1'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE='used'|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME='data3'
  LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='94oczR-Utni-dOzj-3CMQ-efOJ-TVa8-yak25P'|LVM2_DEV_SIZE='3.64t'|LVM2_PV_NAME='/dev/sde1'|LVM2_PV_MAJOR='8'|LVM2_PV_MINOR='65'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='252.00k'|LVM2_PV_EXT_VSN='2'|LVM2_PE_START='256.00k'|LVM2_PV_SIZE='3.64t'|LVM2_PV_FREE='4.00m'|LVM2_PV_USED='3.64t'|LVM2_PV_ATTR='a--'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='953853'|LVM2_PV_PE_ALLOC_COUNT='953852'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='1'|LVM2_PV_MDA_USED_COUNT='1'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE='used'|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME='data4'
  LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='r3UW8H-pLz5-rpsn-GK2u-1kJE-GKsy-uOeoIz'|LVM2_DEV_SIZE='3.64t'|LVM2_PV_NAME='/dev/sdf1'|LVM2_PV_MAJOR='8'|LVM2_PV_MINOR='81'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='252.00k'|LVM2_PV_EXT_VSN='2'|LVM2_PE_START='256.00k'|LVM2_PV_SIZE='3.64t'|LVM2_PV_FREE='4.00m'|LVM2_PV_USED='3.64t'|LVM2_PV_ATTR='a--'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='953853'|LVM2_PV_PE_ALLOC_COUNT='953852'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='1'|LVM2_PV_MDA_USED_COUNT='1'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE='used'|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME='data5'
  LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='oZtJSv-HM9w-4She-1TU0-Z31G-dgKX-liJNID'|LVM2_DEV_SIZE='3.64t'|LVM2_PV_NAME='/dev/sdg1'|LVM2_PV_MAJOR='8'|LVM2_PV_MINOR='97'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='252.00k'|LVM2_PV_EXT_VSN='2'|LVM2_PE_START='256.00k'|LVM2_PV_SIZE='3.64t'|LVM2_PV_FREE='4.00m'|LVM2_PV_USED='3.64t'|LVM2_PV_ATTR='a--'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='953853'|LVM2_PV_PE_ALLOC_COUNT='953852'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='1'|LVM2_PV_MDA_USED_COUNT='1'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE='used'|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME='data6'
  LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='Ys0p6S-WJOW-TAZT-czmX-iOYq-0Tgg-v4cl0H'|LVM2_DEV_SIZE='3.64t'|LVM2_PV_NAME='/dev/sdh1'|LVM2_PV_MAJOR='8'|LVM2_PV_MINOR='113'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='252.00k'|LVM2_PV_EXT_VSN='2'|LVM2_PE_START='256.00k'|LVM2_PV_SIZE='3.64t'|LVM2_PV_FREE='4.00m'|LVM2_PV_USED='3.64t'|LVM2_PV_ATTR='a--'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='953853'|LVM2_PV_PE_ALLOC_COUNT='953852'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='1'|LVM2_PV_MDA_USED_COUNT='1'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE='used'|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME='data7'
""".strip()   # noqa: W291

PVS_INFO_DUP = """
WARNING: Locking disabled. Be careful! This could corrupt your metadata.
WARNING: Device for PV mn5KxB-YKlY-u4hK-zuZJ-Ia6r-3dTg-8IDjsM not found or rejected by a filter.
WARNING: Device for PV V4xZ9b-FXOz-CrRA-Eu2e-8iOS-9EDF-YZYftK not found or rejected by a filter.
WARNING: Device for PV mn5KxB-YKlY-u4hK-zuZJ-Ia6r-3dTg-8IDjsM not found or rejected by a filter.
WARNING: Device for PV V4xZ9b-FXOz-CrRA-Eu2e-8iOS-9EDF-YZYftK not found or rejected by a filter.
LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='mn5KxB-YKlY-u4hK-zuZJ-Ia6r-3dTg-8IDjsM'|LVM2_DEV_SIZE='0 '|LVM2_PV_NAME='unknown device'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PE_START='1.00m'|LVM2_PV_SIZE='9.51g'|LVM2_PV_FREE='0 '|LVM2_PV_USED='9.51g'|LVM2_PV_ATTR='a-m'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING='missing'|LVM2_PV_PE_COUNT='2434'|LVM2_PV_PE_ALLOC_COUNT='2434'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_VG_NAME='rhel'
LVM2_PV_FMT='lvm2'|LVM2_PV_UUID='V4xZ9b-FXOz-CrRA-Eu2e-8iOS-9EDF-YZYftK'|LVM2_DEV_SIZE='0 '|LVM2_PV_NAME='unknown device'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PE_START='1.00m'|LVM2_PV_SIZE='196.00m'|LVM2_PV_FREE='96.00m'|LVM2_PV_USED='100.00m'|LVM2_PV_ATTR='a-m'|LVM2_PV_ALLOCATABLE='allocatable'|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING='missing'|LVM2_PV_PE_COUNT='49'|LVM2_PV_PE_ALLOC_COUNT='25'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_VG_NAME='vgtest'
""".strip()    # noqa: W291

PVS_HEADINGS = """
  WARNING: Locking disabled. Be careful! This could corrupt your metadata.
    Scanning all devices to update lvmetad.
    No PV label found on /dev/loop0.
    No PV label found on /dev/loop1.
    No PV label found on /dev/sda1.
    No PV label found on /dev/fedora/root.
    No PV label found on /dev/sda2.
    No PV label found on /dev/fedora/swap.
    No PV label found on /dev/fedora/home.
    No PV label found on /dev/mapper/docker-253:1-2361272-pool.
    Wiping internal VG cache
    Wiping cache of LVM-capable devices
  PV                                                    VG     Fmt  Attr PSize   PFree DevSize PV UUID                                PMdaFree  PMdaSize  #PMda #PMdaUse PE
  /dev/fedora/home                                                  ---       0     0  418.75g                                               0         0      0        0      0
  /dev/fedora/root                                                  ---       0     0   50.00g                                               0         0      0        0      0
  /dev/fedora/swap                                                  ---       0     0    7.69g                                               0         0      0        0      0
  /dev/loop0                                                        ---       0     0  100.00g                                               0         0      0        0      0
  /dev/loop1                                                        ---       0     0    2.00g                                               0         0      0        0      0
  /dev/mapper/docker-253:1-2361272-pool                             ---       0     0  100.00g                                               0         0      0        0      0
  /dev/mapper/luks-7430952e-7101-4716-9b46-786ce4684f8d fedora lvm2 a--  476.45g 4.00m 476.45g FPLCRf-d918-LVL7-6e3d-n3ED-aiZv-EesuzY        0   1020.00k     1        1 121970
  /dev/sda1                                                         ---       0     0  500.00m                                               0         0      0        0      0
  /dev/sda2                                                         ---       0     0  476.45g                                               0         0      0        0      0
    Reloading config files
    Wiping internal VG cache
""".strip()

PVS_HEADINGS_6 = {
    'PV': '/dev/mapper/luks-7430952e-7101-4716-9b46-786ce4684f8d',
    'VG': 'fedora',
    'Fmt': 'lvm2',
    'Attr': 'a--',
    'PSize': '476.45g',
    'PFree': '4.00m',
    'DevSize': '476.45g',
    'PV_UUID': 'FPLCRf-d918-LVL7-6e3d-n3ED-aiZv-EesuzY',
    'PMdaFree': '0',
    'PMdaSize': '1020.00k',
    '#PMda': '1',
    '#PMdaUse': '1',
    'PE': '121970'
}

PVS_WITH_OTHER_ERROR_BEFORE_CONTENT = """
File descriptor 3 (/var/log/insights-client/insights-client.log) leaked on pvs invocation. Parent PID 26875: timeout
File descriptor 4 (/var/log/insights-client/insights-client.log) leaked on pvs invocation. Parent PID 26875: timeout
  WARNING: Locking disabled. Be careful! This could corrupt your metadata.
  Error reading device /dev/mapper/mpathbm at 0 length 512.
  Error reading device /dev/mapper/mpathbm at 0 length 4.
  Error reading device /dev/mapper/mpathbm at 4096 length 4.
  LVM2_PV_FMT=''|LVM2_PV_UUID=''|LVM2_DEV_SIZE='514.00g'|LVM2_PV_NAME='/dev/mapper/mpathad'|LVM2_PV_MAJOR='253'|LVM2_PV_MINOR='12'|LVM2_PV_MDA_FREE='0 '|LVM2_PV_MDA_SIZE='0 '|LVM2_PV_EXT_VSN=''|LVM2_PE_START='0 '|LVM2_PV_SIZE='0 '|LVM2_PV_FREE='0 '|LVM2_PV_USED='0 '|LVM2_PV_ATTR='---'|LVM2_PV_ALLOCATABLE=''|LVM2_PV_EXPORTED=''|LVM2_PV_MISSING=''|LVM2_PV_PE_COUNT='0'|LVM2_PV_PE_ALLOC_COUNT='0'|LVM2_PV_TAGS=''|LVM2_PV_MDA_COUNT='0'|LVM2_PV_MDA_USED_COUNT='0'|LVM2_PV_BA_START='0 '|LVM2_PV_BA_SIZE='0 '|LVM2_PV_IN_USE=''|LVM2_PV_DUPLICATE=''|LVM2_VG_NAME=''
""".strip()


def test_pvs():
    def check(pvs_records):
        assert len(list(pvs_records)) == 2
        for k, v in PVS_SDA2_INFO.items():
            assert pvs_records.data["content"][1][k] == v
        assert pvs_records["/dev/sda1"]["Attr"] == "---"
        assert pvs_records.data["content"][0]['LVM2_PV_MINOR'] == '1'

    check(Pvs(context_wrap(PVS_INFO)))
    check(Pvs(context_wrap(FD_LEAK_HEADER + PVS_INFO)))

    pvs_records = Pvs(context_wrap(PVS_INFO_LONG))
    assert len(list(pvs_records)) == 31

    # Test vg method
    assert pvs_records.vg('data1') == [{
        'LVM2_PV_MDA_USED_COUNT': '1',
        'LVM2_PV_UUID': 'dhr134-VxSA-R7dW-op7s-HCco-7J2A-7MvaeN',
        'LVM2_DEV_SIZE': '3.64t', 'Fmt': 'lvm2', 'LVM2_PV_MDA_FREE': '0',
        'LVM2_PV_EXPORTED': '', 'LVM2_PV_SIZE': '3.64t',
        'LVM2_PV_PE_ALLOC_COUNT': '953852', 'LVM2_PV_TAGS': '',
        'PFree': '4.00m', 'LVM2_PV_ATTR': 'a--',
        'PV_UUID': 'dhr134-VxSA-R7dW-op7s-HCco-7J2A-7MvaeN', 'PV': '/dev/sdb1',
        'LVM2_PV_NAME': '/dev/sdb1', 'Missing': '', '1st_PE': '256.00k',
        'LVM2_PV_MDA_COUNT': '1', 'LVM2_PV_FREE': '4.00m',
        'LVM2_PV_ALLOCATABLE': 'allocatable', 'BA_start': '0',
        'LVM2_PV_MDA_SIZE': '252.00k', 'Exported': '', 'PE': '953853',
        'PV_Tags': '', 'LVM2_PV_EXT_VSN': '2', 'LVM2_PV_MINOR': '17',
        'Alloc': '953852', 'Attr': 'a--', 'VG': 'data1',
        'LVM2_PE_START': '256.00k', 'LVM2_PV_FMT': 'lvm2',
        'DevSize': '3.64t', 'PSize': '3.64t', 'LVM2_PV_BA_START': '0',
        'Used': '3.64t', 'LVM2_VG_NAME': 'data1', 'PMdaSize': '252.00k',
        'LVM2_PV_PE_COUNT': '953853', 'LVM2_PV_BA_SIZE': '0',
        'LVM2_PV_IN_USE': 'used', 'LVM2_PV_USED': '3.64t', '#PMda': '1',
        'PMdaFree': '0', 'Allocatable': 'allocatable', 'BA_size': '0',
        'LVM2_PV_MAJOR': '8', '#PMdaUse': '1', 'LVM2_PV_MISSING': '',
        'LVM2_PV_DUPLICATE': '',
        'PV_KEY': '/dev/sdb1+dhr134-VxSA-R7dW-op7s-HCco-7J2A-7MvaeN'
    }]


def test_pvs_dup():
    pvs_records = Pvs(context_wrap(PVS_INFO_DUP))
    assert len(list(pvs_records)) == 2
    pv_keys = set([pv['PV_KEY'] for pv in pvs_records])
    assert pv_keys == set([
        'unknown device+mn5KxB-YKlY-u4hK-zuZJ-Ia6r-3dTg-8IDjsM',
        'unknown device+V4xZ9b-FXOz-CrRA-Eu2e-8iOS-9EDF-YZYftK',
    ])


def test_pvs_headings():
    def check(pvs_records):
        assert len(pvs_records.data) == 9
        for k, v in PVS_HEADINGS_6.items():
            assert pvs_records[6][k] == v
        assert pvs_records[6]['Missing'] is None

    pvs_records = PvsHeadings(context_wrap(PVS_HEADINGS))
    check(pvs_records)
    pvs_records = PvsHeadings(context_wrap(FD_LEAK_HEADER + PVS_HEADINGS))
    check(pvs_records)

    # Test vg method
    fedora_pvs = pvs_records.vg('fedora')
    assert len(fedora_pvs) == 1
    assert compare_partial_dicts(fedora_pvs[0], {
        'PV': '/dev/mapper/luks-7430952e-7101-4716-9b46-786ce4684f8d',
        'VG': 'fedora', 'Fmt': 'lvm2', 'Attr': 'a--', 'PSize': '476.45g',
        'PFree': '4.00m', 'DevSize': '476.45g',
        'PV_UUID': 'FPLCRf-d918-LVL7-6e3d-n3ED-aiZv-EesuzY', 'PMdaFree': '0',
        'PMdaSize': '1020.00k', '#PMda': '1', '#PMdaUse': '1', 'PE': '121970',
        'PV_KEY': '/dev/mapper/luks-7430952e-7101-4716-9b46-786ce4684f8d+FPLCRf-d918-LVL7-6e3d-n3ED-aiZv-EesuzY'
    })


def test_pvs_other_error():
    pvs_records = Pvs(context_wrap(PVS_WITH_OTHER_ERROR_BEFORE_CONTENT))
    assert len(pvs_records.data['content']) == 1
    assert 'LVM2_DEV_SIZE' in pvs_records[0]
    assert pvs_records[0].get('LVM2_DEV_SIZE') == '514.00g'
