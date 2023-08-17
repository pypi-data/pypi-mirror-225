# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

"""
A module that provides methods for discovering brainstem modules over USB and TPCIP.

The discovery module provides an interface for locating BrainStem modules accross
multiple transports. It provides a way to find all modules for a give transport
as well as specific modules by serial number, or first found. The result of a call
to one of the discovery functions is either a list of brainstem.link.Spec objects,
or a single brainstem.link.Spec.

The Discovery module allows users to find specific brainstem devices via their
serial number, or a list of all devices connected to the host via usb or on the
same subnet via TCP/IP. In all cases a :doc:`Spec <link>` object is returned with
connection details for the device. In addition do connection details, the BrainStem
model is returned. This model is one of a list of BrainStem device model numbers
which are accessible via the :doc:`defs <defs>` module.

A typical interactive python session finding all connected USB modules might look
like the following.

    >> import brainstem
    >> module_list = brainstem.discover.findAllModules(brainstem.link.Spec.USB)
    >> print [str(s) for s in module_list]
    ['Model: 4 LinkType: USB(serial: 0xCB4A3B25, module: 0)', 'Model: 13 LinkType: USB(serial: 0x40F5849A, module: 0)']

For an overview of links, discovery and the Brainstem network
see the `Acroname BrainStem Reference`_

.. _Acroname BrainStem Reference:
    https://acroname.com/reference
"""

from . import _BS_C, ffi
from .link import Spec, aEtherConfig
from .result import Result

def findModule(transports, serial_number, aether_config=aEtherConfig()):
    """ Return the Spec for the module with the given serial number.

        Transports can be presented as a list. TCPIP modules
        take a little longer to find due to the Multicast and gather
        necessary for finding modules on the local network segment.

        args:
            transports (list(int)): A list of transports or a single transport.
            serial_number (int): The module serial_number to look for.

        Return:
            Spec: The connection spec for the module whose serial number is
                  given in the args.
    """
    _result = None

    if not hasattr(transports, '__iter__'):
        transports = [transports]

    for trans in transports:
        # translate python Spec to C enum type.
        _trans = _get_c_transport(trans)
        if _trans is None:
            return _result

        # Now get a linkSpec* variable if there is a module.
        _cspec = _BS_C.aDiscovery_FindModule(_trans,
                                             serial_number,
                                             aether_config.networkInterface)

        if _cspec != ffi.NULL:
            _result = _get_python_find_result(_cspec)
            # Free the memory allocated by the C Lib call. CFFI didn't allocate,
            # so the _cspec doesn't "own" the memory and it won't be GC'd
            linkref = ffi.new('linkSpec**')
            linkref[0] = _cspec
            _BS_C.aLinkSpec_Destroy(linkref)

    # return translated result or None if not found.
    return _result


def findFirstModule(transport, aether_config=aEtherConfig()):
    """ Return the Spec for the first module found on the given transport.

       TCPIP modules take a little longer to find due to the Multicast and
       gather necessary for finding modules on the local network segment.

        args:
            transport (int): One of USB or TCPIP.

        return:
            Spec: The connection spec of the first module found on the
                  given transport.
    """
    _result = None

    if not hasattr(transport, '__iter__'):
        transport = [transport]

    for trans in transport:
        # translate python Spec to C enum type.
        _trans = _get_c_transport(trans)
        if _trans is None:
            return _result

        # Now get a linkSpec* variable if there is a module.
        _cspec = _BS_C.aDiscovery_FindFirstModule(_trans,
                                                  aether_config.networkInterface)

        if _cspec != ffi.NULL:
            _result = _get_python_find_result(_cspec)
            # Free the memory allocated by the C Lib call. CFFI didn't allocate,
            # so the _cspec doesn't "own" the memory and it won't be GC'd
            linkref = ffi.new('linkSpec**')
            linkref[0] = _cspec
            _BS_C.aLinkSpec_Destroy(linkref)

    # return translated result or None if not found.
    return _result


def findAllModules(transports, aether_config=aEtherConfig()):
    """ Return a list of Specs for all modules found on the transports given.

        Transports can be presented as a list, and the results would be
        a list of all modules found for those transports. TCPIP modules
        take a little longer to find due to the Multicast and gather
        necessary for finding modules on the local network segment.

        args:
            transports (list(int)): A list of transports or a single transport.

        Return:
            list(Spec): A list of the Specs for all modules found.
    """
    _results = list()
    _cresults = ffi.new_handle(_results)

    @ffi.callback("_Bool(linkSpec*, _Bool*, void*)")
    def findAll(spec, success, context):
        results = ffi.from_handle(context)
        device = _get_python_find_result(spec)
        results.append(device)
        success[0] = True
        return True

    if not hasattr(transports, '__iter__'):
        transports = [transports]

    for trans in transports:
        # translate python Spec to C enum type.
        _trans = _get_c_transport(trans)
        if _trans is None:
            return _results

        _BS_C.aDiscovery_EnumerateModules(_trans,
                                          findAll,
                                          _cresults,
                                          aether_config.networkInterface)

    return _results


def getIPv4Interfaces(list_length=30):
    data = ffi.new("uint32_t[]", list_length)
    interfaces_found = _BS_C.aDiscovery_GetIPv4Interfaces(data, list_length)
    device_list = []

    for x in range(0, interfaces_found):
        device_list.append(data[x])

    return tuple(device_list)


class DeviceNode(object):
    """
    Python representation of DeviceNode_t (C structure)
        - hub_serial_number (uint32_t): Serial number of the Acroname hub where the device was found.
        - hub_port (uint8_t): Port of the Acroname hub where the device was found.
        - id_vendor (uint16_t): Manufactures Vendor ID of the downstream device.
        - id_product (uint16_t): Manufactures Product ID of the downstream device.
        - speed (enumeration): The devices downstream device speed.
            - Unknown (0)
            - Low Speed (1)
            - Full Speed (2)
            - High Speed (3)
            - Super Speed (4)
            - Super Speed Plus (5)
        - product_name (string): USB string descriptor.
        - manufacture (string): USB string descriptor.
        - serial_number (string): USB string descriptor.
    """
    def __init__(self):

        self.hub_serial_number = 0
        self.hub_port = 0

        self.id_vendor = 0
        self.id_product = 0
        self.speed = 0
        self.product_name = ""
        self.manufacture = ""
        self.serial_number = ""

    def __str__(self):
        ret = "\n"
        ret = ret + "SN: 0x%08X\n" % self.hub_serial_number
        ret = ret + "Port: %d\n" % self.hub_port
        ret = ret + "\tVendor ID: 0x%04X\n" % self.id_vendor
        ret = ret + "\tProduct ID: 0x%04X\n" % self.id_product
        ret = ret + "\tSpeed: %d\n" % self.speed
        ret = ret + "\tProduct Name: %s\n" % self.product_name
        ret = ret + "\tManufacture: %s\n" % self.manufacture
        ret = ret + "\tSerial Number: %s\n" % self.serial_number
        return ret

    def __repr__(self):
        return self.__str__()


def getDownstreamDevices(list_length=128):
    """
    Gets downstream device USB information for all Acroname hubs.
        args:
            list_length: The amount of memory to provide for the lower level C call.
        Return:
                Result: Result object, containing NO_ERROR and a tuple of DeviceNode's
                        containing the detected downstream devices.
                        - aErrParam: Passed in values are not valid. (NULL, size etc).
                        - aErrMemory: No more room in the list
                        - aErrNotFound: No Acroname devices were found.
    """

    data = ffi.new("DeviceNode_t[]", list_length)
    num_devices_found = ffi.new("uint32_t*")
    err = _BS_C.getDownstreamDevices(data, list_length, num_devices_found)
    device_list = []

    for x in range(0, num_devices_found[0]):
        node = DeviceNode()
        node.hub_serial_number = data[x].hubSerialNumber
        node.hub_port = data[x].hubPort
        node.id_vendor = data[x].idVendor
        node.id_product = data[x].idProduct
        node.speed = data[x].speed
        node.product_name = ffi.string(data[x].productName)
        node.manufacture = ffi.string(data[x].manufacturer)
        node.serial_number = ffi.string(data[x].serialNumber)
        device_list.append(node)

    return Result(err, tuple(device_list))


def _get_c_transport(transport):
    """ Internal: Translate Spec transport to cffi transport"""
    _trans = None
    if transport == Spec.USB:
        _trans = _BS_C.USB
    elif transport == Spec.TCPIP:
        _trans = _BS_C.TCPIP
    elif transport == Spec.SERIAL:
        _trans = _BS_C.SERIAL
    elif transport == Spec.AETHER:
        _trans = _BS_C.AETHER

    return _trans


def _get_python_find_result(cspec):
    """ Internal: Translate cffi spec into python Spec"""
    if cspec.type == _BS_C.USB:
        result = Spec(Spec.USB, cspec.serial_num, cspec.module, cspec.model)
    elif cspec.type == _BS_C.TCPIP:
        result = Spec(Spec.TCPIP, cspec.serial_num, cspec.module, cspec.model,
                      ip_address=cspec.t.ip.ip_address, ip_port=cspec.t.ip.ip_port)
    elif cspec.type == _BS_C.SERIAL:
        result = Spec(Spec.SERIAL, cspec.serial_num, cspec.module, cspec.model,
                      port=cspec.t.serial.port, baudrage=cspec.t.serial.baudrate)
    elif cspec.type == _BS_C.AETHER:
        result = Spec(Spec.AETHER, cspec.serial_num, cspec.module, cspec.model,
                      ip_address=cspec.t.ip.ip_address, ip_port=cspec.t.ip.ip_port)
    return result
