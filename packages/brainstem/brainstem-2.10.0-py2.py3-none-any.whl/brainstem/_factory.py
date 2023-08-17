import struct
from . import _BS_C, str_or_bytes_to_bytearray
from .module import Entity
from .result import Result


class _Factory(Entity):
    """ For internal use only.

    """
    MATCH_MASK = (~((1 << _BS_C.factoryError_Bit) |
                    (1 << _BS_C.factoryStart_Bit) |
                    (1 << _BS_C.factoryEnd_Bit) |
                    (1 << _BS_C.factorySet_Bit)) & 0xFF)

    def __init__(self, module, index):
        """Store initializer"""
        super(_Factory, self).__init__(module, _BS_C.cmdFACTORY, index)

    def getFactoryData(self, command):
        result = Result(_BS_C.aErrNone, None)
        count = 0
        first_command = True
        length = 28
        match = ([(command & _Factory.MATCH_MASK), ((command & _Factory.MATCH_MASK) | (1 << _BS_C.factoryError_Bit))],)
        result_data = bytearray()
        while result.error == Result.NO_ERROR and length == _BS_C.MAX_PACKET_BYTES:
            if self.module.link is None:
                result._error = Result.CONNECTION_ERROR
                break
            else:
                if first_command:
                    data = struct.pack('B', command | (1 << _BS_C.factoryStart_Bit))
                    first_command = False
                else:
                    data = struct.pack('B', command)

                error = self.module.link.send_command_packet(self.module.address, _BS_C.cmdFACTORY, 1, data)

                if error == Result.NO_ERROR:
                    result = self.module.link.receive_command_packet(self.module.address,
                                                                     _BS_C.cmdFACTORY,
                                                                     match, 1000)
                else:
                    result._error = error

                if result.error == Result.NO_ERROR:
                    vals = str_or_bytes_to_bytearray(result.value, 0, _BS_C.MAX_PACKET_BYTES)
                    length = result._length
                    if (vals[1] & (1 << _BS_C.factoryError_Bit)) > 0:
                        result._error = vals[2]
                        result_data = None
                    else:
                        count = count + (length - 2)
                        result_data = result_data + vals[2:length]
                else:
                    result._error = Result.TIMEOUT
                    result_data = None

        if result.error == Result.NO_ERROR:
            data = struct.pack('BBB',
                               command | (1 << _BS_C.factoryEnd_Bit),
                               ((count & 0x0000FF00) >> 8),
                               ((count & 0x000000FF) >> 0))

            error = self.module.link.send_command_packet(self.module.address, _BS_C.cmdFACTORY, 3, data)

            if error == Result.NO_ERROR:
                result = self.module.link.receive_command_packet(self.module.address,
                                                                 _BS_C.cmdFACTORY,
                                                                 match, 1000)
            else:
                result._error = error

            if result.error == Result.NO_ERROR:
                vals = str_or_bytes_to_bytearray(result.value, 0, 28)
                if (vals[1] & (1 << _BS_C.factoryError_Bit)) > 0:
                    result._error = vals[2]
                    if result.error != Result.NO_ERROR:
                        result_data = None
            else:
                result._error = Result.TIMEOUT
                result_data = None

        result = Result(result.error, tuple(result_data) if result_data else None)

        return result

    def setFactoryData(self, command, data, length):
        err = Result.NO_ERROR
        count = 0
        first_command = True
        match = ([(command & _Factory.MATCH_MASK), ((command & _Factory.MATCH_MASK) | (1 << _BS_C.factoryError_Bit))],)
        while err == Result.NO_ERROR and count < length:
            if first_command:
                packet = struct.pack('B', command | (1 << _BS_C.factoryStart_Bit) | (1 << _BS_C.factorySet_Bit))
                first_command = False
            else:
                packet = struct.pack('B', command | (1 << _BS_C.factorySet_Bit))

            block = length - count

            if block > (_BS_C.MAX_PACKET_BYTES - 2):
                block = (_BS_C.MAX_PACKET_BYTES - 2)

            packet = packet + data[count:(count + block)]

            if self.module.link is None:
                err = Result.CONNECTION_ERROR
            else:
                err = self.module.link.send_command_packet(self.module.address,
                                                           _BS_C.cmdFACTORY,
                                                           len(packet), packet)

                result = Result(Result.TIMEOUT, 0)
                if err == Result.NO_ERROR:
                    result = self.module.link.receive_command_packet(self.module.address,
                                                                     _BS_C.cmdFACTORY,
                                                                     match, 1000)

                if result.error == Result.NO_ERROR:
                    vals = str_or_bytes_to_bytearray(result.value, 0, _BS_C.MAX_PACKET_BYTES)
                    if (vals[1] & (1 << _BS_C.factoryError_Bit)) > 0:
                        err = vals[2]
                    else:
                        count = count + block
                else:
                    err = result.error

        if err == Result.NO_ERROR:
            data = struct.pack('BBB',
                               command | (1 << _BS_C.factoryEnd_Bit),
                               ((count & 0x0000FF00) >> 8),
                               ((count & 0x000000FF) >> 0))

            err = self.module.link.send_command_packet(self.module.address, _BS_C.cmdFACTORY, 3, data)

            result = Result(Result.TIMEOUT, 0)
            if err == Result.NO_ERROR:
                result = self.module.link.receive_command_packet(self.module.address,
                                                                 _BS_C.cmdFACTORY,
                                                                 match, 1000)

            if err == Result.NO_ERROR and result.error == Result.NO_ERROR:
                vals = str_or_bytes_to_bytearray(result.value, 0, 28)
                if (vals[1] & (1 << _BS_C.factoryError_Bit)) > 0:
                    err = vals[2]

            else:
                err = Result.TIMEOUT

        return err
