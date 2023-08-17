from contextlib import contextmanager
import struct

from . import (
    _BS_C,
    str_or_bytes_to_bytearray,
    convert_int_args_to_bytes,
    deprecated,
)

from .module import Entity
from .result import Result


class _ResourceException(RuntimeError):
    pass


class System(Entity):
    """ Acccess system controls configuration and information.

        The system entity is available on all BrainStem modules, and provides
        access to system information such as module, router and serial number,
        as well as control over the user LED, and information such as the system
        input voltage.

        Useful Constants:
            * BOOT_SLOT_DISABLE (255)
    """

    BOOT_SLOT_DISABLE = 255

    def __init__(self, module, index):
        """System Entity Initializer"""
        super(System, self).__init__(module, _BS_C.cmdSYSTEM, index)

    def setModuleSoftwareOffset(self, value):
        """Set the software address offset.

            The module software offset is added to the base module address, and
            potentially a hardware offset to determine the final calculated address
            the module uses on the BrainStem network. You must save and reset
            the module for this change to become effective.

            Warning:
                changing the module address may cause the module to "drop off"
                the BrainStem network if the module is also the router. Please
                review the BrainStem network fundamentals before modifying the
                module address.

           args:
                value (int): The module address offset.

           Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.systemModuleSoftwareOffset, value)

    def getModule(self):
        """ Get the address the module uses on the BrainStem network.

            Return:
                Result: Result object, containing NO_ERROR and the current module address
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemModule)

    def getModuleBaseAddress(self):
        """ Get the base address the module.

            The software and hardware addresses are added to the base address
            to produce the effective module address.

            Return:
                Result: Result object, containing NO_ERROR and the current module address
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemModuleBaseAddress)

    def getModuleSoftwareOffset(self):
        """ Get the module address software offset.

            The address offset that is added to the module base address, and
            potentially the hardware offset to produce the module effective address.

            Return:
                Result: Result object, containing NO_ERROR and the current module address
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemModuleSoftwareOffset)

    def setRouter(self, value):
        """ Set the router address the module uses to communicate with the host.

            Warning:
                Changing the router address may cause the module to "drop off"
                the BrainStem network if the new router address is not in use by
                a BrainStem module. Please review the BrainStem network
                fundamentals before modifying the router address.

           args:
                value (int): The module address of the router module on the network.

           Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.systemRouter, value)

    def getRouter(self):
        """ Get the router address the module uses to communicate with the host.

            Return:
                Result: Result object, containing NO_ERROR and the current router address
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemRouter)

    def getRouterAddressSetting(self):
        """ Get the router address setting saved in the module.

            This setting may be different from the effective router if the router
            has been set and saved but no reset has been made.

            Return:
                Result: Result object, containing NO_ERROR and the current router address
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemRouterAddressSetting)

    def setHBInterval(self, value):
        """ Set the delay between heartbeat packets.

            For link modules, these heartbeat are sent to the host.
            For non-link modules, these heartbeats are sent to the router address.
            Interval values are in 25.6 millisecond increments Valid values are
            1-255; default is 10 (256 milliseconds).

            args:
                value (int): Heartbeat interval settings.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.systemHBInterval, value)

    def getHBInterval(self):
        """ Get the delay between heartbeat packets.

            For link modules, these heartbeat are sent to the host.
            For non-link modules, these heartbeats are sent to the router address.
            Interval values are in 25.6 millisecond increments.

            return:
                Result: Result object, containing NO_ERROR and the Heartbeat interval
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemHBInterval)

    def setLED(self, value):
        """ Set the system LED state.

            Most modules have a blue system LED. Refer to the module
            datasheet for details on the system LED location and color.

            args:
                value (int): LED State setting.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.systemLED, value)

    def getLED(self):
        """ Get the system LED state.

            Most modules have a blue system LED. Refer to the module
            datasheet for details on the system LED location and color.

            return:
                Result: Result object, containing NO_ERROR and the LED State
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemLED)

    def setBootSlot(self, value):
        """ Set a store slot to be mapped when the module boots.

            The boot slot will be mapped after the module boots from powers up,
            receives a reset signal on its reset input, or is issued a software
            reset command. Set the slot to 255 to disable mapping on boot.

            args:
                value (int): The slot number in aSTORE_INTERNAL to be marked
                             as a boot slot.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.systemBootSlot, value)

    def getBootSlot(self):
        """ Get the store slot which is mapped when the module boots.

            return:
                Result: Result object, containing NO_ERROR and slot number
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemBootSlot)

    def getVersion(self):
        """ Get the modules firmware version number.

            The version number is packed into the return value. Utility functions
            in the Version module can unpack the major, minor and patch numbers from
            the version number which looks like M.m.p.

            return:
                Result: Result object, containing NO_ERROR packed version number
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemVersion)

    def getModel(self):
        """ Get the module's model enumeration.

            A subset of the possible model enumerations is defined in
            aProtocolDefs.h under "BrainStem model codes". Other codes are be
            used by Acroname for proprietary module types.

            return:
                Result: Result object, containing NO_ERROR and model number
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemModel)

    def getHardwareVersion(self):
        """ Get the module's hardware revision information.

            The content of the hardware version is specific to each Acroname
            product and used to indicate behavioral differences between product
            revisions. The codes are not well defined and may change at any time.

            return:
                Result: Result object, containing NO_ERROR and hardware revision
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemHardwareVersion)

    def getSerialNumber(self):
        """ Get the module's serial number.

            The serial number is a unique 32bit integer which is usually
            communicated in hexadecimal format.

            return:
                Result: Result object, containing NO_ERROR and serial number
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemSerialNumber)

    def save(self):
        """ Save the system operating parameters to the persistent module flash memory.

            Operating parameters stored in the system flash will be loaded after the module
            reboots. Operating parameters include: heartbeat interval, module address,
            module router address

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.call_UEI(_BS_C.systemSave)

    def reset(self):
        """ Reset the system.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.call_UEI(_BS_C.systemReset)

    def logEvents(self):
        """ Save system log entries to slot defined by module.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.call_UEI(_BS_C.systemLogEvents)

    def getInputVoltage(self):
        """ Get the module's input voltage.

            return:
                Result: Result object, containing NO_ERROR and input voltage
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemInputVoltage)

    def getInputCurrent(self):
        """ Get the module's input current.

            return:
                Result: Result object, containing NO_ERROR and input current
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemInputCurrent)

    def getModuleHardwareOffset(self):
        """ Get the module address hardware offset.

            This is added to the base address to allow the module address to be
            configured in hardware. Not all modules support the hardware module
            address offset. Refer to the module datasheet.

            return:
                Result: Result object, containing NO_ERROR and module offset
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemModuleHardwareOffset)

    def getUptime(self):
        """ Get accumulated system uptime.

            This is the total time the system has been powered up with
            the firmware running. The returned uptime is a count of minutes
            of uptime, or may be a module dependent counter.

            return:
                Result: Result object, containing NO_ERROR and uptime in minutes
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.systemUptime)

    def getTemperature(self):
        """ Get the module's current temperature in micro-C

            return:
                Result: Result object, containing NO_ERROR and max temperature in micro-C
                        or a non zero Error code.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.systemTemperature))

    def getMinimumTemperature(self):
        """ Get the module's minimum temperature ever recorded in micro-C (uC)
            This value will persists through a power cycle.

            return:
                Result: Result object, containing NO_ERROR and max temperature in micro-C
                        or a non zero Error code.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.systemMinTemperature))

    def getMaximumTemperature(self):
        """ Get the module's maximum temperature ever recorded in micro-C (uC)
            his value will persists through a power cycle.

            return:
                Result: Result object, containing NO_ERROR and max temperature in micro-C
                        or a non zero Error code.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.systemMaxTemperature))

    def routeToMe(self, value):
        """ Enables/Disables the route to me function.

            This function allows for easy networking of BrainStem modules.
            Enabling (1) this function will send an I2C General Call to all devices
            on the network and request that they change their router address
            to the of the calling device. Disabling (0) will cause all devices
            on the BrainStem network to revert to their default address.

            args:
                value (int): Enable or disable of the route to me function 1 = enable.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.systemRouteToMe, value)

    def getPowerLimit(self):
        """
        Reports the amount of power the system has access to and thus how much
        power can be budgeted to sinking devices.

        Returns:
            Result (object):
                value (int): Power limit in milli-watts (mW)
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.systemPowerLimit)

    def getPowerLimitMax(self):
        """ Gets the user defined maximum power limit for the system.
            Provides mechanism for defining an unregulated power supplies capability.

        Returns:
            Result (object):
                value (int): Power limit in milli-watts (mW)
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.systemPowerLimitMax)

    def setPowerLimitMax(self, limit):
        """ Sets a user defined maximum power limit for the system.
            Provides mechanism for defining an unregulated power supplies capability.

        Args:
            limit (int): Limit in milli-watts (mW) to be set

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.systemPowerLimitMax, limit)

    def getPowerLimitState(self):
        """ Gets a bit mapped representation of the factors contributing to the power limit.
            Active limit can be found through PowerDeliveryClass::getPowerLimit().

        Returns:
            Result (object):
                value (int): The current power limit state.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.systemPowerLimitState)

    def getUnregulatedVoltage(self):
        """ Gets the voltage present at the unregulated port.

        Returns:
            Result (object):
                value (int): Unregulated Voltage in micro-volts (mV)
                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.systemUnregulatedVoltage))

    def getUnregulatedCurrent(self):
        """ Gets the current present at the unregulated port.

        Returns:
            Result (object):
                value (int): Unregulated current in micro-amps (mA)
                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.systemUnregulatedCurrent))

    def getInputPowerSource(self):
        """ Provides the source of the current power source in use.

        Returns:
            Result (object):
                value (int): An enumerated value representing the current input power source.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.systemInputPowerSource)

    def getInputPowerBehavior(self):
        """ Gets the systems input power behavior.
            This behavior refers to where the device sources its power from and what
            happens if that power source goes away.

        Returns:
            Result (object):
                value (int): an enumerated value representing behavior.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.systemInputPowerBehavior)

    def setInputPowerBehavior(self, behavior):
        """ Sets the systems input power behavior.
            This behavior refers to where the device sources its power from and what
            happens if that power source goes away.

        Args:
            behavior (int): An enumerated representation of behavior to be set.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.systemInputPowerBehavior, behavior)

    def getInputPowerBehaviorConfig(self):
        """ Gets the input power behavior configuration
            Certain behaviors use a list of ports to determine priority when budgeting power.

        Returns:
            Result (object):
                value (tuple(int)): A list of ports which indicate priority sequencing.
                error: Non-zero BrainStem error code on failure.
           """
        return self.check_UEIBytes(self.get_UEIBytes(_BS_C.systemInputPowerBehaviorConfig),4)

    def setInputPowerBehaviorConfig(self, config):
        """ Sets the input power behavior configuration
            Certain behaviors use a list of ports to determine priority when budgeting power.

        Args:
            config (tuple(int)): List of ports which indicate priority sequencing.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return Result.UNIMPLEMENTED_ERROR

    def getName(self):
        """ Gets a user defined name of the port.
            Helpful for identifying ports/devices in a static environment.

        Returns:
            Result (object):
                value: The current name of the port on success.
                error: Non-zero BrainStem error code on failure.
        """
        return self.bytes_to_string(self.get_UEIBytes(_BS_C.systemName))

    def setName(self, name):
        """Sets a user defined name of the port.
           Helpful for identifying ports/devices in a static environment.

        Args:
            name (string): User defined name to be set.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """

        return self.set_UEIBytes(_BS_C.systemName, name)

    def resetEntityToFactoryDefaults(self):
        """Resets the SystemClass Entity to it factory default configuration.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.call_UEI(_BS_C.systemResetEntityToFactoryDefaults)

    def resetDeviceToFactoryDefaults(self):
        """Resets the device to it factory default configuration.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.call_UEI(_BS_C.systemResetDeviceToFactoryDefaults)

    def getLinkInterface(self):
        """ Gets the link interface configuration.
            This refers to which interface is being used for control by the device.

        Returns:
            Result (object):
                value (int): an enumerated value representing interface.
                    * 0 = Auto
                    * 1 = Control Port
                    * 2 = Hub Upstream Port

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.systemLinkInterface)

    def setLinkInterface(self, linkInterface):
        """ Sets the link interface configuration.
            This refers to which interface is being used for control by the device.

        Args:
            interface (int): An enumerated representation of interface to be set.
                * 0 = Auto= systemLinkAuto
                * 1 = Control Port = systemLinkUSBControl
                * 2 = Hub Upstream Port = systemLinkUSBHub

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.systemLinkInterface, linkInterface)

    def getErrors(self):
        """
        Gets System level errors.
        Calling this function will clear the current errors.
        If the error persists it will be set again.

        Returns:
            Result (object):
                value: Bit mapped value representing the errors.
                See product datasheet for details.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.systemErrors)


class Analog(Entity):
    """ The AnalogClass is the interface to analog entities on BrainStem modules.

        Analog entities may be configured as a input or output depending on hardware
        capabilities. Some modules are capable of providing actual voltage readings,
        while other simply return the raw analog-to-digital converter (ADC) output
        value. The resolution of the voltage or number of useful bits is also
        hardware dependent.

        Useful constants:
            * CONFIGURATION_INPUT (0)
            * CONFIGURATION_OUTPUT (1)
            * HERTZ_MINIMUM (7,000)
            * HERTZ_MAXIMUM (200,000)
            * BULK_CAPTURE_IDLE (0)
            * BULK_CAPTURE_PENDING (1)
            * BULK_CAPTURE_FINISHED (2)
            * BULK_CAPTURE_ERROR (3)

    """

    CONFIGURATION_INPUT = 0
    CONFIGURATION_OUTPUT = 1
    HERTZ_MINIMUM = 7000
    HERTZ_MAXIMUM = 200000
    BULK_CAPTURE_IDLE = 0
    BULK_CAPTURE_PENDING = 1
    BULK_CAPTURE_FINISHED = 2
    BULK_CAPTURE_ERROR = 3

    def __init__(self, module, index):
        """ Analog Entity Initializer """
        super(Analog, self).__init__(module, _BS_C.cmdANALOG, index)

    def setConfiguration(self, value):
        """ Set the analog configuration.

            Some analogs can be configured as DAC outputs. Please see your module
            datasheet to determine which analogs can be configured as DAC.

            Param:
                value (int): Set 1 for output 0 for input. Default configuration
                is input.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.analogConfiguration, value)

    def getConfiguration(self):
        """ Get the analog configuration.

            If the configuraton is 1 the analog is configured as an output, if
            the configuration is 0, the analog is set as an input.

            return:
                Result: Result object, containing NO_ERROR and analog configuration
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.analogConfiguration)

    def setRange(self, value):
        """ Set the range of an analog input.

            Set a value corresponding to a discrete range option.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.analogRange, value)

    def getRange(self):
        """ Get the range setting of an analog input

            Get a value corresponding to a discrete range option.

            return:
                Result: Result object, containing NO_ERROR and analog range
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.analogRange)

    def setValue(self, value):
        """ Set the value of an analog output (DAC) in bits.

            Set a 16 bit analog set point with 0 corresponding to the negative
            analog voltage reference and 0xFFFF corresponding to the positive
            analog voltage reference.

            Note:
                Not all modules are provide 16 useful bits; the least significant bits
                are discarded. E.g. for a 10 bit DAC, 0xFFC0 to 0x0040 is the useful
                range. Refer to the module's datasheet to determine analog bit
                depth and reference voltage.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI16(_BS_C.analogValue, value)

    def getValue(self):
        """ Get the raw ADC value in bits.

            Get a 16 bit analog set point with 0 corresponding to the negative
            analog voltage reference and 0xFFFF corresponding to the positive
            analog voltage reference.

            Note:
                Not all modules provide 16 useful bits; the least significant bits
                are discarded. E.g. for a 10 bit ADC, 0xFFC0 to 0x0040 is the useful
                range. Refer to the module's datasheet to determine analog bit
                depth and reference voltage.

            return:
                Result: Result object, containing NO_ERROR and analog value
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.analogValue)

    def setVoltage(self, value):
        """ Set the voltage level of an analog output (DAC) in microVolts with
            reference to ground.

            Set a 16 bit signed integer as voltage output (in microVolts).

            Note:
                Voltage range is dependent on the specific DAC channel range.
                See datasheet and setRange for options.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.analogVoltage, value)

    def getVoltage(self):
        """ Get the scaled micro volt value with reference to ground.

            Get a 32 bit signed integer (in microVolts) based on the boards
            ground and reference voltages.

            Note:
                Not all modules provide 32 bits of accuracy; Refer to the module's
                datasheet to determine the analog bit depth and reference voltage.

            return:
                Result: Result object, containing NO_ERROR and microVolts value
                        or a non zero Error code.

        """
        return _BS_SignCheck(self.get_UEI(_BS_C.analogVoltage))

    def setEnable(self, enable):
        """ Set the enable state of an analog output.

            Set a boolean value corresponding to on/off

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.analogEnable, enable)

    def getEnable(self):
        """ Get the enable state an analog output

            Get a boolean value corresponding to on/off

            return:
                Result: Result object, containing NO_ERROR and enable state
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.analogEnable)

    def setBulkCaptureSampleRate(self, value):
        """ Set the sample rate for this analog when bulk capturing.

            Sample rate is set in samples per second (Hertz).

            Minimum Rate: 7,000 Hertz
            Maximum Rate: 200,000 Hertz

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.analogBulkCaptureSampleRate, value)

    def getBulkCaptureSampleRate(self):
        """ Get the current sample rate setting for this analog when bulk capturing.

            Sample rate is in samples per second (Hertz).

            return:
                Result: Result object, containing NO_ERROR and sample rate
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.analogBulkCaptureSampleRate)

    def setBulkCaptureNumberOfSamples(self, value):
        """ Set the number of samples to capture for this analog when bulk capturing.

            Minimum # of Samples: 0
            Maximum # of Samples: (BRAINSTEM_RAM_SLOT_SIZE / 2) = (3FFF / 2) = 1FFF = 8191

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.analogBulkCaptureNumberOfSamples, value)

    def getBulkCaptureNumberOfSamples(self):
        """ Get the current number of samples setting for this analog when bulk capturing.

            return:
                Result: Result object, containing NO_ERROR and sample number
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.analogBulkCaptureNumberOfSamples)

    def initiateBulkCapture(self):
        """ Initiate a BulkCapture on this analog. Captured measurements are stored in the
            module's RAM store (RAM_STORE) slot 0. Data is stored in a contiguous byte array
            with each sample stored in two consecutive bytes, LSB first.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure. When the bulk capture is complete
                getBulkCaptureState() will return either finished or error.
        """
        return self.call_UEI(_BS_C.analogBulkCapture)

    def getBulkCaptureState(self):
        """ Get the current bulk capture state for this analog.

            Possible states of the bulk capture operation are;
            idle = 0
            pending = 1
            finished = 2
            error = 3

            return:
                Result: Result object, containing NO_ERROR and bulk capture state
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.analogBulkCaptureState)


class App(Entity):
    """ The AppClass calls defined app reflexes on brainstem modules.

        Calls a remote procedure defined in an active map file on a brainstem
        module. The remote procedure may return a value or not.
    """

    def __init__(self, module, index):
        """ Clock Entity Initializer """
        super(App, self).__init__(module, _BS_C.cmdAPP, index)

    def execute(self, param):
        """ Execute an App reflex on a module.

            Param:
                param (int): App routine parameter.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.appExecute, param)

    def executeAndWaitForReturn(self, param, msTimeout):
        """ Execute an App reflex on a module, and wait for it to return a
            result.

            Param:
                param (int): App routine parameter.
            Param:
                msTimeout (int): millisecons to wait for routine to complete.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        self.drain_UEI(_BS_C.appReturn)
        err = self.set_UEI32(_BS_C.appExecute, param)
        if err == Result.NO_ERROR:
            return self.await_UEI_Val(_BS_C.appReturn, msTimeout)
        else:
            return Result(err, None)


class Clock(Entity):
    """ The ClockClass is the interface to the realtime clock.

        For modules that support realtime clocks, this class supports getting
        and setting clock values for year, month, day, hour, minute and second.
    """

    def __init__(self, module, index):
        """ Clock Entity Initializer """
        super(Clock, self).__init__(module, _BS_C.cmdCLOCK, index)

    def setYear(self, year):
        """ Set the current year

            Param:
                value (int): Current 4 digit year.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI16(_BS_C.clockYear, year)

    def getYear(self):
        """ Get the current year

            return:
                Result: Result object, containing NO_ERROR and current year or
                        a non zero Error code.
        """
        return self.get_UEI(_BS_C.clockYear)

    def setMonth(self, month):
        """ Set the current month

            Param:
                value (int): Current 2 digit month.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.clockMonth, month)

    def getMonth(self):
        """ Get the current month

            return:
                Result: Result object, containing NO_ERROR and current month or
                        a non zero Error code.
        """
        return self.get_UEI(_BS_C.clockMonth)

    def setDay(self, day):
        """ Set the current day of the month

            Param:
                value (int): Current 2 digit day.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.clockDay, day)

    def getDay(self):
        """ Get the current day of the month

            return:
                Result: Result object, containing NO_ERROR and current day or
                        a non zero Error code.
        """
        return self.get_UEI(_BS_C.clockDay)

    def setHour(self, hour):
        """ Set the current hour

            Param:
                value (int): Current 2 digit hour.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.clockHour, hour)

    def getHour(self):
        """ Get the current hour

            return:
                Result: Result object, containing NO_ERROR and current hour or
                        a non zero Error code.
        """
        return self.get_UEI(_BS_C.clockHour)

    def setMinute(self, minute):
        """ Set the current minute

            Param:
                value (int): Current 2 digit minute.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.clockMinute, minute)

    def getMinute(self):
        """ Get the current minute

            return:
                Result: Result object, containing NO_ERROR and current minute or
                        a non zero Error code.
        """
        return self.get_UEI(_BS_C.clockMinute)

    def setSecond(self, second):
        """ Set the current second

            Param:
                value (int): Current 2 digit second.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.clockSecond, second)

    def getSecond(self):
        """ Get the current second

            return:
                Result: Result object, containing NO_ERROR and current second or
                        a non zero Error code.
        """
        return self.get_UEI(_BS_C.clockSecond)


class Digital(Entity):
    """ The DigitalClass is the interface to digital entities on BrainStem modules.

        Digital entities have the following 5 possabilities: Digital Input,
        Digital Output, RCServo Input, RCServo Output, and HighZ.
        Other capabilities may be available and not all pins support all
        configurations. Please see the product datasheet.

        Useful Constants:
            * VALUE_LOW (0)
            * VALUE_HIGH (1)
            * CONFIGURATION_INPUT (0)
            * CONFIGURATION_OUTPUT (1)
            * CONFIGURATION_RCSERVO_INPUT (2)
            * CONFIGURATION_RCSERVO_OUTPUT (3)
            * CONFIGURATION_HIGHZ (4)
            * CONFIGURATION_INPUT_PULL_UP (0)
            * CONFIGURATION_INPUT_NO_PULL (4)
            * CONFIGURATION_INPUT_PULL_DOWN (5)
            * CONFIGURATION_SIGNAL_OUTPUT (6)
            * CONFIGURATION_SIGNAL_INPUT (7)
    """

    VALUE_LOW = 0
    VALUE_HIGH = 1
    CONFIGURATION_INPUT = 0
    CONFIGURATION_OUTPUT = 1
    CONFIGURATION_RCSERVO_INPUT = 2
    CONFIGURATION_RCSERVO_OUTPUT = 3
    CONFIGURATION_HIGHZ = 4
    CONFIGURATION_INPUT_PULL_UP = 0
    CONFIGURATION_INPUT_NO_PULL = 4
    CONFIGURATION_INPUT_PULL_DOWN = 5
    CONFIGURATION_SIGNAL_OUTPUT = 6
    CONFIGURATION_SIGNAL_INPUT = 7
    CONFIGURATION_SIGNAL_COUNTER_INPUT = 8

    def __init__(self, module, index):
        """Digital Entity initializer"""
        super(Digital, self).__init__(module, _BS_C.cmdDIGITAL, index)

    def setConfiguration(self, configuration):
        """ Set the digital configuration.

            Param:
                configuration (int):
                    * Digital Input: CONFIGURATION_INPUT = 0
                    * Digital Output: CONFIGURATION_OUTPUT = 1
                    * RCServo Input: CONFIGURATION_RCSERVO_INPUT = 2
                    * RCServo Output: CONFIGURATION_RCSERVO_OUTPUT = 3
                    * High Z State: CONFIGURATION_HIGHZ = 4
                    * Digital Input with pull up: CONFIGURATION_INPUT_PULL_UP = 0 (Default)
                    * Digital Input with no pull up or pull down: CONFIGURATION_INPUT_NO_PULL = 4
                    * Digital Input with pull down: CONFIGURATION_INPUT_PULL_DOWN = 5
                    * Digital Signal Output: CONFIGURATION_SIGNAL_OUTPUT = 6
                    * Digital Signal Input: CONFIGURATION_SIGNAL_INPUT = 7


            Return:
                Result.error:
                    Return NO_ERROR on success, or one of the common
                    sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.digitalConfiguration, configuration)

    def getConfiguration(self):
        """ Get the digital configuration.

            If the configuration is 1 the digital is configured as an output, if
            the configuration is 0, the digital is set as an input.

            return:
                Result:
                    Result object, containing NO_ERROR and digital configuration
                    or a non zero Error code.
        """
        return self.get_UEI(_BS_C.digitalConfiguration)

    def setState(self, state):
        """ Set the digital state.

            Param:
                state (int):
                    Set 1 for logic high, set 0 for logic low. configuration
                    must be set to output.

            Return:
                Result.error:
                    Return NO_ERROR on success, or one of the common
                    sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.digitalState, state)

    def getState(self):
        """ Get the digital state.

            A return of 1 indicates the digitial is above the logic high threshold.
            A return of 0 indicates the digital is below the logic low threshold.

            return:
                Result:
                    Result object, containing NO_ERROR and digital state
                    or a non zero Error code.
        """
        return self.get_UEI(_BS_C.digitalState)

    def setStateAll(self, state):
        """ Sets the digital state of all digitals based on the bit mapping.
            Number of digitals varies across BrainStem modules. Refer to then
            datasheet for the capabilities of your module.

            Param:
                state (uint):
                    The state to be set for all digitals in a bit mapped
                    representation. 0 is logic low, 1 is logic high. Where
                    bit 0 = digital 0, bit 1 = digital 1 etc.
                    Configuration must be set to output.

            Return:
                Result.error:
                    Return NO_ERROR on success, or one of the common
                    sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.digitalStateAll, state)

    def getStateAll(self):
        """ Gets the digital state of all digitals in a bit mapped representation.
            Number of digitals varies across BrainStem modules. Refer to then
            datasheet for the capabilities of your module.

            return:
                Result:
                    Result object, containing NO_ERROR and the digital state
                    of all digitals where bit 0 = digital 0 and bit 1 = digital 1 etc.
                    0 = logic low and 1 = logic high.
                    A non zero Error code is returned on error.
        """
        return self.get_UEI(_BS_C.digitalStateAll)


class Equalizer(Entity):
    """ Equalizer Class provides receiver and transmitter gain/boost/emphasis
        settings for some of Acroname's products.  Please see product documentation
        for further details.
    """

    def __init__(self, module, index):
        """ Signal Entity initializer """
        super(Equalizer, self).__init__(module, _BS_C.cmdEQUALIZER, index)

    def setReceiverConfig(self, channel, config):
        """ Sets the receiver configuration for a given channel.

            :param channel: The equalizer receiver channel.
            :param config: Configuration to be applied to the receiver.
            :return: Result.error Return NO_ERROR on success, or one of the common
                    sets of return error codes on failure.
        """
        return self.set_UEI8_with_subindex(_BS_C.equalizerReceiverConfig, channel, config)

    def getReceiverConfig(self, channel):
        """ Gets the receiver configuration for a given channel.

            :param channel: The equalizer receiver channel.
            :return: Result object, containing NO_ERROR and the receiver configuration of the supplied channel
                            or a non zero Error code.
        """
        return self.get_UEI_with_param(_BS_C.equalizerReceiverConfig, channel)

    def setTransmitterConfig(self, config):
        """ Sets the transmitter configuration

            :param config: Configuration to be applied to the transmitter.
            :return: Result.error Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.equalizerTransmitterConfig, config)

    def getTransmitterConfig(self):
        """ Gets the transmitter configuration

            :return: Result object, containing NO_ERROR and the current transmitter config
                     or a non zero Error code.
        """
        return self.get_UEI(_BS_C.equalizerTransmitterConfig)


class I2C(Entity):
    """ The I2C class is the interface the I2C busses on BrainStem modules.

        The class provides a way to send read and write commands to I2C devices
        on the entitie's bus.

        Useful Constants:
            * I2C_DEFAULT_SPEED  (0)
            * I2C_SPEED_100Khz   (1)
            * I2C_SPEED_400Khz   (2)
            * I2C_SPEED_1000Khz  (3)

    """
    I2C_DEFAULT_SPEED = 0
    I2C_SPEED_100Khz = 1
    I2C_SPEED_400Khz = 2
    I2C_SPEED_1000Khz = 3

    def __init__(self, module, index):
        """ I2C entity initializer"""
        super(I2C, self).__init__(module, _BS_C.cmdI2C, index)
        self._busSpeed = self.I2C_DEFAULT_SPEED

    def getSpeed(self):
        """ Get the current speed setting of the I2C object.

            Return:
                returns a Result object containing one of the constants
                representing the I2C objects current speed setting.
        """

        return Result(Result.NO_ERROR, self._busSpeed)

    def setSpeed(self, value):
        """ Set the current speed setting of the I2C object.

            Param:
                value (int): The constant representing the bus speed setting to apply or this object.

            Return:
                returns NO_ERROR on success or PARAMETER_ERROR on failure.
        """
        if value in (0, 1, 2, 3):
            self._busSpeed = value
            return Result.NO_ERROR
        else:
            return Result.PARAMETER_ERROR

    def write(self, address, length, *args):
        """ Send I2C write command, on the I2C BUS represented by the entity.

            Param:
                address (int): The I2C address (7bit <XXXX-XXX0>) of the device to write.
            Param:
                length (int): The length of the data to write in bytes.
            Param:
                data (\*int | list): variable number of args of either int in the range of 0 to
                                     255 or list|tuple of ints.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        try:
            data = convert_int_args_to_bytes(args)
        except ValueError:
            return Result.PARAMETER_ERROR

        if address % 2:
            return Result.PARAMETER_ERROR

        if length > _BS_C.MAX_PACKET_BYTES - 5:
            return Result.SIZE_ERROR

        d = struct.pack('BBBB', self.index, address, length, self._busSpeed)
        match = (self.index, address, 0)
        result = self.send_command(4 + length, d + data, match)
        if result.error == Result.NO_ERROR:
            # Look into packet...
            vals = str_or_bytes_to_bytearray(result.value)
            try:
                if (vals[4] & 0x80) > 0:
                    result._error = vals[4] ^ 0x80
            except IndexError:
                result._error = Result.IO_ERROR

        return result.error

    def read(self, address, length):
        """ Send I2C read command, on the I2C BUS represented by the entity.

            Param:
                address (int): The I2C address (7bit <XXXX-XXX0>) of the device to read.
            Param:
                length (int): The length of the data to read in bytes.

            Return:
                Result: Result object, containing NO_ERROR and read data or a non zero Error code.
        """

        if length > _BS_C.MAX_PACKET_BYTES - 5:
            return Result(Result.SIZE_ERROR, None)

        data = struct.pack('BBBB', self.index, address | 0x01, length, self._busSpeed)
        match = (self.index, address | 0x01, length)
        result = self.send_command(4, data, match)
        if result.error == Result.NO_ERROR:
            # Look into packet...
            vals = str_or_bytes_to_bytearray(result.value)
            # If theres an error we return that in the result, and set value to None.
            try:
                if (vals[4] & 0x80) > 0:
                    result._error = vals[4] ^ 0x80
                    result._value = None
                else:
                    result._value = vals[5:5+vals[3]]
            except IndexError:
                result._error = Result.IO_ERROR
                result._value = None

        return result

    def setPullup(self, bEnable):
        """ Set software controlled I2C pullup state.

            Sets the software controlled pullup on the bus for stems with
            software controlled pullup capabilities. Check the device datasheet
            for more information.
            This setting is saved by a system.save.

            Param:
                bEnable (bool): The desired state of the pullup.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        state = 1 if bEnable else 0
        d = struct.pack('BBB', self.index, _BS_C.i2cSetPullup, state)
        match = (self.index, _BS_C.i2cSetPullup)
        result = self.send_command(3, d, match)
        if result.error == Result.NO_ERROR:
            # Look into packet...
            vals = str_or_bytes_to_bytearray(result.value)
            try:
                if (vals[4] & 0x80) > 0:
                    result._error = vals[4] ^ 0x80
            except IndexError:
                result._error = Result.IO_ERROR

        return result.error


class Mux(Entity):
    """ Access MUX specialized entities on certain BrainStem modules.

        A MUX is a multiplexer that takes one or more similar inputs
        (bus, connection, or signal) and allows switching to one or more outputs.
        An analogy would be the switchboard of a telephone operator.  Calls (inputs)
        come in and by re-connecting the input to an output, the operator
        (multiplexor) can direct that input to on or more outputs.

        One possible output is to not connect the input to anything which
        essentially disables that input's connection to anything.

        Not every MUX has multiple inputs.  Some may simply be a single input that
        can be enabled (connected to a single output) or disabled
        (not connected to anything).

        Useful Constants:
            * UPSTREAM_STATE_ONBOARD (0)
            * UPSTREAM_STATE_EDGE (1)
            * UPSTREAM_MODE_AUTO (0)
            * UPSTREAM_MODE_ONBOARD (1)
            * UPSTREAM_MODE_EDGE (2)
            * DEFAULT_MODE (UPSTREAM_MODE_AUTO)
    """

    UPSTREAM_STATE_ONBOARD = 0
    UPSTREAM_STATE_EDGE = 1
    UPSTREAM_MODE_AUTO = 0
    UPSTREAM_MODE_ONBOARD = 1
    UPSTREAM_MODE_EDGE = 2
    DEFAULT_MODE = UPSTREAM_MODE_AUTO

    def __init__(self, module, index):
        """ Mux entity initializer"""
        super(Mux, self).__init__(module, _BS_C.cmdMUX, index)

    def setEnable(self, bEnable):
        """ Enables or disables the mux based on the param.

            Param:
                bEnable (bool): True = Enable, False = Disable

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.muxEnable, bEnable)

    def getEnable(self):
        """ Gets the enable/disable status of the mux.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.get_UEI(_BS_C.muxEnable)

    def setChannel(self, channel):
        """ Enables the specified channel of the mux.

            Param:
                channel (int): The channel of the mux to enable.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.muxChannel, channel)

    def getChannel(self):
        """ Gets the current selected channel.

            Param:
                channel (int): The channel of the mux to enable.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """

        return self.get_UEI(_BS_C.muxChannel)

    def getVoltage(self, channel):
        """ Gets the voltage of the specified channel.

            On some modules this is a measured value so may not exactly match what was
            previously set via the setVoltage interface. Refer to the module datasheet to
            to determine if this is a measured or stored value.

            return:
                Result: Return result object with NO_ERROR set and the current
                mux voltage setting in the Result.value or an Error.
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.muxVoltage, channel))

    def getConfiguration(self):
        """ Gets the configuration of the Mux.

            return:
                Result: Return result object with NO_ERROR set and the current
                mux voltage setting in the Result.value or an Error.
        """
        return self.get_UEI(_BS_C.muxConfig)

    def setConfiguration(self, config):
        """ Sets the configuration of the mux.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.muxConfig, config)

    def getSplitMode(self):
        """ Gets the bit packed mux split configuration.

            return:
                Result: Return result object with NO_ERROR set and the current
                mux voltage setting in the Result.value or an Error.
        """
        return self.get_UEI(_BS_C.muxSplit)

    def setSplitMode(self, splitMode):
        """ Sets the mux split configuration

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.muxSplit, splitMode)

class Pointer(Entity):
    """ Access the reflex scratchpad from a host computer.

        The Pointers access the pad which is a shared memory area on a BrainStem module.
        The interface allows the use of the brainstem scratchpad from the host, and provides
        a mechanism for allowing the host application and brainstem relexes to communicate.

        The Pointer allows access to the pad in a similar manner as a file pointer accesses
        the underlying file. The cursor position can be set via setOffset. A read of a character
        short or int can be made from that cursor position. In addition the mode of the pointer
        can be set so that the cursor position automatically increments or set so that it does not
        this allows for multiple reads of the same pad value, or reads of multi-record values, via
        and incrementing pointer.

        Useful Constants:
          * POINTER_MODE_STATIC (0)
          * POINTER_MODE_INCREMENT (1)

    """

    POINTER_MODE_STATIC = 0
    POINTER_MODE_INCREMENT = 1

    def __init__(self, module, index):
        """ Pointer entity initializer"""
        super(Pointer, self).__init__(module, _BS_C.cmdPOINTER, index)

    def setOffset(self, offset):
        """ Set the pointer offset for this pointer.

            Param:
                offset (char): The byte offset within the pad (0 - 255).

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI16(_BS_C.pointerOffset, offset)

    def getOffset(self):
        """ Get the pointer offset for this pointer.

            Return:
                Result: Result object, containing NO_ERROR and the current offset
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.pointerOffset)

    def setMode(self, mode):
        """ Set the pointer offset for this pointer.

            Param:
                mode (char): The mode. One of POINTER_MODE_STATIC or POINTER_MODE_INCREMENT

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.pointerMode, mode)

    def getMode(self):
        """ Get the pointer offset for this pointer.

            Return:
                Result: Result object, containing NO_ERROR and the current mode
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.pointerMode)

    def setTransferStore(self, handle):
        """ Set store slot handle for the pad to store and store to pad transfer.

            Param:
                handle (char): The handle. Open slot handle id.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.pointerTransferStore, handle)

    def getTransferStore(self):
        """ Get the open slot handle for this pointer.

            Return:
                Result: Result object, containing NO_ERROR and the handle
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.pointerTransferStore)

    def setChar(self, charVal):
        """ Set a value at the current cursor position within the pad.

            If the mode is increment this write will increment the cursor by 1 byte.

            Param:
                charVal (char): The value to set into the pad at the current
                             pointer position.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.pointerChar, charVal)

    def getChar(self):
        """ Get the value of the pad at the current cursor position.

            If the mode is increment this read will increment the cursor by 1 byte.

            Return:
                Result: Result object, containing NO_ERROR and the value
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.pointerChar)

    def setShort(self, shortVal):
        """ Set a value at the current cursor position within the pad.

            If the mode is increment this write will increment the cursor by 2 bytes.

            Param:
                shortVal (short): The value to set into the pad at the current
                             pointer position.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI16(_BS_C.pointerShort, shortVal)

    def getShort(self):
        """ Get the value of the pad at the current cursor position.

            If the mode is increment this read will increment the cursor by 2 bytes.

            Return:
                Result: Result object, containing NO_ERROR and the value
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.pointerShort)

    def setInt(self, intVal):
        """ Set a value at the current cursor position within the pad.

            If the mode is increment this write will increment the cursor by 4 bytes.

            Param:
                short (short): The value to set into the pad at the current
                               pointer position.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.pointerInt, intVal)

    def getInt(self):
        """ Get the value of the pad at the current cursor position.

            If the mode is increment this read will increment the cursor by 4 bytes.

            Return:
                Result: Result object, containing NO_ERROR and the value
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.pointerInt)

    def transferToStore(self, length):
        """ Transfer length bytes from the pad cursor position into the open store handle.

            If the mode is increment the transfer will increment the cursor by length bytes.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI16(_BS_C.pointerTransferToStore, length)

    def transterFromStore(self, length):
        """ Transfer length bytes from the open store handle to the cursor position in the pad.

            If the mode is increment the transfer will increment the cursor by length bytes.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI16(_BS_C.pointerTransferFromStore, length)


class Port(Entity):
    """
        The Port Entity provides software control over the most basic items related to a
        USB Port. This includes everything from the complete enable and disable of the
        entire port to the individual control of specific pins. Voltage and Current
        measurements are also included for devices which support the Port Entity.

    """

    def __init__(self, module, index):
        """ Port entity initializer"""
        super(Port, self).__init__(module, _BS_C.cmdPORT, index)

    def getVbusVoltage(self):
        """
        Gets the Vbus Voltage.

        Returns:
            Result (object):
                value: The voltage in microvolts (1 == 1e-6V) currently present on Vbus.
                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.portVbusVoltage))

    def getVbusCurrent(self):
        """
        Gets the Vbus Current.

        Returns:
            Result (object):
                value: The current in microamps (1 == 1e-6A) currently present on VBUS.
                error: Non-zero BrainStem error code on failure.
           """
        return _BS_SignCheck(self.get_UEI(_BS_C.portVbusCurrent))

    def getVconnVoltage(self):
        """
        Gets the Vconn Voltage.

        Returns:
            Result (object):
                value: The voltage in microvolts (1 == 1e-6v) currently present on Vconn.
                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.portVconnVoltage))

    def getVconnCurrent(self):
        """
        Gets the Vconn Current.

        Returns:
            Result (object):
                value: The current in microamps (1 == 1e-6A) currently present on Vconn.
                error: Non-zero BrainStem error code on failure.
           """
        return _BS_SignCheck(self.get_UEI(_BS_C.portVconnCurrent))


    def setEnabled(self, enable):
        """
        Enables or disables the entire port.

        Args:
            enable (bool) -
                * 1 = Enable the port
                * 0 = Disable the port

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portPortEnabled, enable)

    def getEnabled(self):
        """
        Gets the current enable value of the port.

        Returns:
            Result (object):
                value:
                    * 1 = Fully enabled port
                    * 0 = One or more disabled sub-components.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portPortEnabled)

    def setDataEnabled(self, enable):
        """
        Enables or disables the data lines. Sub-component (Data) of setEnable.

        Args:
            enable (bool) -
                * 1 = Enable data
                * 0 = Disable data

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portDataEnabled, enable)

    def getDataEnabled(self):
        """
        Gets the current enable value of the data lines.
        Sub-component (Data) of getEnable.

        Returns:
            Result (object):
                value:
                    * 1 = Data enabled
                    * 0 = Data disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataEnabled)

    def setDataHSEnabled(self, enable):
        """
        Enables or disables the High Speed (HS) data lines.
        Sub-component of setDataEnable.

        Args:
            enable (bool) -
                * 1 = Enable data
                * 0 = Disable data.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portDataHSEnabled, enable)

    def getDataHSEnabled(self):
        """
        Gets the current enable value of the High Speed (HS) data lines.
        Sub-component of getDataEnable.

        Returns:
            Result (object):
                value:
                    * 1 = Data enabled
                    * 0 = Data disabled

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataHSEnabled)

    def setDataHS1Enabled(self, enable):
        """
        Enables or disables the High Speed 1 side (HS1) data lines.
        Sub-component of setDataHSEnable.

        Args:
            enable (bool) -
                * 1 = Enable data
                * 0 = Disable data

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portDataHS1Enabled, enable)

    def getDataHS1Enabled(self):
        """
        Gets the current enable value of the High Speed 1 side (HS1) data lines.:
        Sub-component of getDataHSEnable.

        Returns:
            Result (object):
                value:
                    * 1 = Data enabled;
                    * 0 = Data disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataHS1Enabled)

    def setDataHS2Enabled(self, enable):
        """
        Enables or disables the High Speed 2 side (HS2) data lines.
        Sub-component of setDataHSEnable.

        Args:
            enable (bool) -
                * 1 = Enable data
                * 0 = Disable data.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portDataHS2Enabled, enable)

    def getDataHS2Enabled(self):
        """
        Gets the current enable value of the High Speed B side (HSB) data lines.:
        Sub-component of getDataHSEnable.

        Returns:
            Result (object):
                value:
                    * 1 = Data enabled
                    * 0 = Data disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataHS2Enabled)

    def setDataSSEnabled(self, enable):
        """
        Enables or disables the Super Speed (SS) data lines.
        Sub-component of setDataEnable.

        Args:
            enable (bool) -
                * 1 = Enable data
                * 0 = Disable data.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portDataSSEnabled, enable)

    def getDataSSEnabled(self):
        """
        Gets the current enable value of the Super Speed (SS) data lines.
        Sub-component of getDataEnable.

        Returns:
            Result (object):
                value:
                    * 1 = Data enabled;
                    * 0 = Data disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataSSEnabled)

    def setDataSS1Enabled(self, enable):
        """
        Enables or disables the Super Speed 1 side (SS1) data lines.
        Sub-component of setDataEnable.

        Args:
            enable (bool) -
                * 1 = Enable data
                * 0 = Disable data.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portDataSS1Enabled, enable)

    def getDataSS1Enabled(self):
        """
        Gets the current enable value of the Super Speed 1 side (SS1) data lines.:
        Sub-component of getDataSSEnable.

        Returns:
            Result (object):
                value:
                    * 1 = Data enabled
                    * 0 = Data disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataSS1Enabled)

    def setDataSS2Enabled(self, enable):
        """
        Enables or disables the Super Speed 2 side (SS2) data lines.
        Sub-component of setDataSSEnable.

        Args:
            enable (bool) -
                * 1 = Enable data
                * 0 = Disable data.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portDataSS2Enabled, enable)

    def getDataSS2Enabled(self):
        """
        Gets the current enable value of the Super Speed 2 side (SS2) data lines.
        Sub-component of getDataSSEnable.

        Returns:
            Result (object):
                value:
                    * 1 = Data enabled;
                    * 0 = Data disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataSS2Enabled)

    def setVconnEnabled(self, enable):
        """
        Enables or disables the Vconn lines.
        Sub-component (Vconn) of setEnabled.

        Args:
            enable (bool) -
                * 1 = Enable Vconn lines
                * 0 = Disable Vconn lines.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portVconnEnabled, enable)

    def getVconnEnabled(self):
        """
        Gets the current enable value of the Vconn lines.
        Sub-component (Vconn) of getEnabled.

        Returns:
            Result (object):
                value:
                    * 1 = Vconn enabled
                    * 0 = Vconn disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portVconnEnabled)

    def setVconn1Enabled(self, enable):
        """
        Enables or disables the Vconn1 lines.
        Sub-component of setVconnEnabled.

        Args:
            enable (bool) -
                * 1 = Enable Vconn1 lines
                * 0 = Disable Vconn1 lines.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portVconn1Enabled, enable)

    def getVconn1Enabled(self):
        """
        Gets the current enable value of the Vconn1 lines.
        Sub-component of getVconnEnabled.

        Returns:
            Result (object):
                value:
                    * 1 = Vconn1 enabled
                    * 0 = Vconn1 disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portVconn1Enabled)

    def setVconn2Enabled(self, enable):
        """
        Enables or disables the Vconn2 lines.
        Sub-component of setVconnEnabled.

        Args:
            enable (bool) -
                * 1 = Enable Vconn2 lines
                * 0 = Disable Vconn2 lines

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portVconn2Enabled, enable)

    def getVconn2Enabled(self):
        """
        Gets the current enable value of the Vconn2 lines.
        Sub-component of getVconnEnabled.

        Returns:
            Result (object):
                value:
                    * 1 = Vconn2 enabled
                    * 0 = Vconn2 disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portVconn2Enabled)

    def setCCEnabled(self, enable):
        """
        Enables or disables the CC lines.
        Sub-component (CC) of setEnabled.

        Args:
            enable (bool) -
                * 1 = Enable CC lines
                * 0 = Disable CC lines.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portCCEnabled, enable)

    def getCCEnabled(self):
        """
        Gets the current enable value of the CC lines.
        Sub-component (CC) of getEnabled.

        Returns:
            Result (object):
                value (int):
                    * 1 = CC enabled
                    * 0 = CC disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portCCEnabled)

    def setCC1Enabled(self, enable):
        """
        Enables or disables the CC1 lines.
        Sub-component (CC1) of setEnabled.

        Args:
            enable (bool) -
                * 1 = Enable CC1 lines
                * 0 = Disable CC1 lines.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portCC1Enabled, enable)

    def getCC1Enabled(self):
        """
        Gets the current enable value of the CC1 lines.
        Sub-component (CC1) of getEnabled.

        Returns:
            Result (object):
                value:
                    * 1 = CC1 enabled
                    * 0 = CC1 disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portCC1Enabled)

    def setCC2Enabled(self, enable):
        """
        Enables or disables the CC2 lines.
        Sub-component (CC2) of setEnabled.

        Args:
            enable (bool) -
                * 1 = Enable CC2 lines
                * 0 = Disable CC2 lines.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portCC2Enabled, enable)

    def getCC2Enabled(self):
        """
        Gets the current enable value of the CC2 lines.
        Sub-component (CC2) of getEnabled.

        Returns:
            Result (object):
                value:
                    * 1 = CC2 enabled
                    * 0 = CC2 disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portCC2Enabled)

    def setVoltageSetpoint(self, value):
        """
        Sets the current voltage setpoint value of the port

        Args:
            value (int) -
                The voltage setpoint in uV

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.portVoltageSetpoint, value)

    def getVoltageSetpoint(self):
        """
        Gets the current voltage setpoint value of the port.

        Returns:
            Result (object):
                value:
                    The voltage setpoint in uV

                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.portVoltageSetpoint))

    def setPowerEnabled(self, enable):
        """
        Enables or Disables the power lines.
        Sub-component (Power) of setEnable.

        Args:
            enable (bool) -
                * 1 = Enable power
                * 0 = Disable disable.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portPowerEnabled, enable)

    def getPowerEnabled(self):
        """
        Gets the current enable value of the power lines.
        Sub-component (Power) of getEnable.

        Returns:
            Result (object):
                value:
                    * 1 = Power enabled
                    * 0 = Power disabled.

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portPowerEnabled)

    def getPowerMode(self):
        """
        Gets the Port Power Mode: Convenience Function of get/setPortMode

        Returns:
            Result (object):
                value: The current power mode. See product datasheet for details.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portPowerMode)

    def setPowerMode(self, powerMode):
        """
        Sets the Port Power Mode: Convenience Function of get/setPortMode

        Args:
            powerMode (int): Power mode to be set. See product datasheet for details.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portPowerMode, powerMode)

    def getDataRole(self):
        """
        Gets the Port Data Role.

        Returns:
            Result (object):
                value: The current data role. See product datasheet for details.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataRole)

    def getDataSpeed(self):
        """
        Gets the speed of the enumerated device.

        Returns:
            Result (object):
                value: Bit mapped value representing the devices speed.
                See product datasheet for details.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataSpeed)

    def getMode(self):
        """
        Gets current mode of the port

        Returns:
            Result (object):
                value: Bit mapped value representing the ports mode.
                See product datasheet for details.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portPortMode)

    def setMode(self, mode):
        """
        Sets the mode of the port.

        Args:
            mode (int): Port mode to be set. See product datasheet for details.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.portPortMode, mode)

    def getState(self):
        """
        A bit mapped representation of the current state of the port.
        Reflects what he port IS which may differ from what was requested.

        Returns:
            Result (object):
                value: Bit mapped value representing the ports state.
                See product datasheet for details.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portPortState)

    def getErrors(self):
        """
        Returns any errors that are present on the port.
        Calling this function will clear the current errors.
        If the error persists it will be set again.

        Returns:
            Result (object):
                value: Bit mapped value representing the errors of the port
                See product datasheet for details.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portErrors)

    def getCurrentLimit(self):
        """ Gets the current limit of the port.

        Returns:
            Result (object):
                value: limit of the port in microAmps (uA)
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portCurrentLimit)

    def setCurrentLimit(self, limit):
        """
        Sets the current limit of the port.

        Args:
            limit (int): limit to be applied in microAmps (uA)

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.portCurrentLimit, limit)

    def getCurrentLimitMode(self):
        """
        Gets the current limit mode.
        The mode determines how the port will react to an over current condition.

        Returns:
            Result (object):
                value: An enumerated representation of the active current limit mode.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portCurrentLimitMode)

    def setCurrentLimitMode(self, mode):
        """
        Sets the current limit mode.
        The mode determines how the port will react to an over current condition.

        Args:
            mode (int): An enumerated representation of the current limit mode.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portCurrentLimitMode, mode)

    def getAvailablePower(self):
        """
        Gets the current available power.
        This value is determined by the power manager which is responsible for budgeting the
        systems available power envelope.

        Returns:
            Result (object):
                value (int): Available power in milli-watts (mW)
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portAvailablePower)

    def getAllocatedPower(self):
        """
        Gets the currently allocated power
        This value is determined by the power manager which is responsible for budgeting the
        systems allocated power envelope.

        Returns:
            Result (object):
                value (int): Allocated power in milli-watts (mW)
                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.portAllocatedPower))

    def getPowerLimit(self):
        """
        Gets the power limit of the port.

        Returns:
            Result (object):
                value: Active power limit in milli-watts (mW)
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portPowerLimit)

    def setPowerLimit(self, limit):
        """
        Sets the power limit of the port.

        Args:
            limit (int): Limit to be applied in milli-watts (mW)

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.portPowerLimit, limit)

    def getPowerLimitMode(self):
        """
        Gets the power limit mode.
        The mode determines how the port will react to an over power condition.

        Returns:
            Result (object):
                value: An enumerated representation of the power limit mode
                Available modes are product specific. See the reference documentation.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portPowerLimitMode)

    def setPowerLimitMode(self, mode):
        """
        Sets the power limit mode.
        The mode determines how the port will react to an over power condition.

        Args:
            mode (int): An enumerated representation of the power limit mode to be applied.
            Available modes are product specific. See the reference documentation.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portPowerLimitMode, mode)

    def getDataHSRoutingBehavior(self):
        """
        Gets the HighSpeed Data Routing Behavior.
        The mode determines how the port will route the data lines.

        Returns:
            Result (object):
                value: An enumerated representation of the routing behavior.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataHSRoutingBehavior)

    def setDataHSRoutingBehavior(self, mode):
        """
        Sets the HighSpeed Data Routing Behavior.
        The mode determines how the port will route the data lines.

        Args:
            mode (int): An enumerated representation of the routing behavior.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portDataHSRoutingBehavior, mode)

    def getDataSSRoutingBehavior(self):
        """
        Gets the SuperSpeed Data Routing Behavior.
        The mode determines how the port will route the data lines.

        Returns:
            Result (object):
                value: An enumerated representation of the routing behavior.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portDataSSRoutingBehavior)

    def setDataSSRoutingBehavior(self, mode):
        """
        Sets the SuperSpeed Data Routing Behavior.
        The mode determines how the port will route the data lines.

        Args:
            mode (int): An enumerated representation of the routing behavior.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portDataSSRoutingBehavior, mode)


    def getName(self):
        """
        Gets a user defined name of the port.
        Helpful for identifying ports/devices in a static environment.

        Returns:
            Result (object):
                value: The current name of the port on success.
                error: Non-zero BrainStem error code on failure.
        """
        return self.bytes_to_string(self.get_UEIBytes(_BS_C.portName))

    def setName(self, name):
        """
        Sets a user defined name of the port.
        Helpful for identifying ports/devices in a static environment.

        Args:
            name (string): User defined name to be set.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEIBytes(_BS_C.portName, name)

    def getVbusAccumulatedPower(self):
        """
        Gets the accumulated Vbus Power.

        Returns:
            Result (object):
                value: The accumulated power in mWattHours (1 == 1e-3 Wh) currently consumed on VBUS.
                error: Non-zero BrainStem error code on failure.
           """
        return _BS_SignCheck(self.get_UEI(_BS_C.portVbusAccumulatedPower))

    def resetVbusAccumulatedPower(self):
        """
        Resets the Vbus accumulated power.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.call_UEI(_BS_C.portResetVbusAccumulatedPower)

    def getVconnAccumulatedPower(self):
        """
        Gets the accumulated Vconn Power.

        Returns:
            Result (object):
                value: The accumulated power in mWattHours (1 == 1e-3 Wh) currently consumed on Vconn.
                error: Non-zero BrainStem error code on failure.
           """
        return _BS_SignCheck(self.get_UEI(_BS_C.portVconnAccumulatedPower))

    def resetVconnAccumulatedPower(self):
        """
        Resets the Vconn accumulated power.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.call_UEI(_BS_C.portResetVconnAccumulatedPower)

    def getHSBoost(self):
        """
        Gets the ports USB 2.0 High Speed Boost Settings
        The setting determines how much additional drive the USB 2.0 signal
        will have in High Speed mode.

        Returns:
            Result (object):
                value: An enumerated representation of the boost range.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.portHSBoost)

    def setHSBoost(self, boost):
        """
        Sets the ports USB 2.0 High Speed Boost Settings
        The setting determines how much additional drive the USB 2.0 signal
        will have in High Speed mode.

        Args:
            boost (int): An enumerated representation of the boost range.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.portHSBoost, boost)

    def resetEntityToFactoryDefaults(self):
        """
        Resets the PortClass Entity to it factory default configuration.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.call_UEI(_BS_C.portResetEntityToFactoryDefaults)


class PowerDelivery(Entity):
    """
        Power Delivery or PD is a power specification which allows more charging
        options and device behaviors within the USB interface.  This Entity will
        allow you to directly access the vast landscape of PD.
    """

    def __init__(self, module, index):
        """ PowerDelivery entity initializer"""
        super(PowerDelivery, self).__init__(module, _BS_C.cmdPOWERDELIVERY, index)

    def getConnectionState(self):
        """
        Gets the current state of the connection in the form of an enumeration.

        Returns:
            Result (object):
                value (int): An enumerated representation of the current state.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryConnectionState)

    def getNumberOfPowerDataObjects(self, partner, powerRole):
        """
        Gets the number of Power Data Objects (PDOs) for a given partner and power role.

        Args:
            partner (int) - Indicates which side of the PD connection is in question.
                - Local = 0 = powerdeliveryPartnerLocal
                - Remote = 1 = powerdeliveryPartnerRemote

            powerRole (int) - Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink

        Returns:
            Result (object):
                value (int): The number of of Power Data Objects (PDO)
                error: Non-zero BrainStem error code on failure.
        """
        e = PowerDelivery._checkPowerRole(powerRole)
        if e == Result.NO_ERROR:
            return self.get_UEI_with_param(_BS_C.powerdeliveryNumberOfPowerDataObjects,
                                           PowerDelivery._packRule(partner, powerRole, 0))
        else:
            return Result(e, 0)

    def getPowerDataObject(self, partner, powerRole, ruleIndex):
        """
        Gets the number of Power Data Objects (PDOs) for a given partner and power role.

        Args:
            partner (int) - Indicates which side of the PD connection is in question.
                - Local = 0 = powerdeliveryPartnerLocal
                - Remote = 1 = powerdeliveryPartnerRemote

            powerRole (int) - Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink

            ruleIndex (int) - The index of the PDO in question. Valid index are 1-7.

        Returns:
            Result (object):
                value (int): Power Data Object (PDO) for the given partner and power role.
                error: Non-zero BrainStem error code on failure.
        """
        e = PowerDelivery._checkPowerRole(powerRole)
        if e == Result.NO_ERROR:
            return self.get_UEI_with_param(_BS_C.powerdeliveryPowerDataObject,
                                           PowerDelivery._packRule(partner, powerRole, ruleIndex))
        else:
            return Result(e, 0)

    def setPowerDataObject(self, powerRole, ruleIndex, pdo):
        """
        Sets the Power Data Object (PDO) of the local partner for a given power role and index.

        Args:
            powerRole (int) - Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink

            ruleIndex (int): The index of the PDO in question. Valid index are 1-7.
            pdo (int): Power Data Object to be set.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        e = PowerDelivery._checkPowerRole(powerRole)
        if e == Result.NO_ERROR:
            return self.set_UEI32_with_subindex(
                _BS_C.powerdeliveryPowerDataObject,
                PowerDelivery._packRule(_BS_C.powerdeliveryPartnerLocal, powerRole, ruleIndex),
                pdo)
        else:
            return e

    def resetPowerDataObjectToDefault(self, powerRole, ruleIndex):
        """
        Resets the Power Data Object (PDO) of the Local partner for a given power role and index.

        Args:
            powerRole (int) - Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink

            ruleIndex (int): The index of the PDO in question. Valid index are 1-7.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        e = PowerDelivery._checkPowerRole(powerRole)
        if e == Result.NO_ERROR:
            return self.set_UEI8(_BS_C.powerdeliveryResetPowerDataObjectToDefault,
                                 PowerDelivery._packRule(_BS_C.powerdeliveryPartnerLocal, powerRole, ruleIndex))
        else:
            return e

    def getPowerDataObjectList(self):
        """
        Gets all Power Data Objects (PDO) for a given partner and power role.
        Equivalent to calling PowerDelivery.getPowerDataObject() on all
        partners, power roles, and index's.

        Returns:
            Result (object):
                value (tuple(int)): All Power Data Objects (PDOs)
                On success the length should be 28 (7 rules * 2 partners * 2 power roles)
                The order of which is:
                    - Rules 1-7 Local Source
                    - Rules 1-7 Local Sink
                    - Rules 1-7 Remote Source
                    - Rules 1-7 Remote Sink

                error: Non-zero BrainStem error code on failure.
        """
        return self.check_UEIBytes(self.get_UEIBytes(_BS_C.powerdeliveryPowerDataObjectList),4)

    def getPowerDataObjectEnabled(self, powerRole, ruleIndex):
        """
        Gets the enabled state of the Local Power Data Object (PDO) for a given power role and index.
        Enabled refers to whether the PDO will be advertised when a PD connection is made.
        This does not indicate the currently active rule index. This information can be found in
        Request Data Object (RDO).

        Args:
            powerRole (int) - Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink

            ruleIndex (int): The index of the PDO in question. Valid index are 1-7.

        Returns:
            Result (object):
                value (bool): Represents the enabled state.
                error: Non-zero BrainStem error code on failure.
        """
        e = PowerDelivery._checkPowerRole(powerRole)
        if e == Result.NO_ERROR:
            return self.get_UEI_with_param(
                _BS_C.powerdeliveryPowerDataObjectEnabled,
                PowerDelivery._packRule(_BS_C.powerdeliveryPartnerLocal, powerRole, ruleIndex))
        else:
            return Result(e, 0)

    def setPowerDataObjectEnabled(self, powerRole, ruleIndex, enable):
        """
        Sets the enabled state of the Local Power Data Object (PDO) for a given powerRole and index.
        Enabled refers to whether the PDO will be advertised when a PD connection is made.
        This does not indicate the currently active rule index. This information can be found in
        Request Data Object (RDO).

        Args:
            powerRole (int) - Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink

            ruleIndex (int): The index of the PDO in question. Valid index are 1-7.
            enable (bool): The enabled state to be set.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8_with_subindex(
            _BS_C.powerdeliveryPowerDataObjectEnabled,
            PowerDelivery._packRule(_BS_C.powerdeliveryPartnerLocal, powerRole, ruleIndex),
            enable)

    def getPowerDataObjectEnabledList(self, powerRole):
        """
        Gets all Power Data Object enables for a given power role.
        Equivalent of calling PowerDelivery.getPowerDataObjectEnabled() for all indexes.

        Args:
            powerRole (int) - Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource (1) Source
                - Sink = 2 = powerdeliveryPowerRoleSink (2) Sink

        Returns:
            Result (object):
                value (bool): Bit mapped representation of the enabled PDOs for a given power role
                Values align with a given rule index (bits 1-7, bit 0 is invalid).
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI_with_param(_BS_C.powerdeliveryPowerDataObjectEnabledList,
                                       PowerDelivery._packRule(_BS_C.powerdeliveryPartnerLocal, powerRole, 0))

    def getRequestDataObject(self, partner):
        """
        Gets the current Request Data Object (RDO) for a given partner.

        RDOs:
            - Are provided by the sinking device.
            - Exist only after a successful PD negotiation (Otherwise zero).
            - Only one RDO can exist at a time. i.e. Either the Local or Remote partner RDO

        Args:
            partner (int) - Indicates which side of the PD connection is in question.
                - Local = 0 = powerdeliveryPartnerLocal
                - Remote = 1 = powerdeliveryPartnerRemote

        Returns:
            Result (object):
                value (int): Value of the request RDO. (Zero indicates the RDO is not active)
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI_with_param(_BS_C.powerdeliveryRequestDataObject,
                                       PowerDelivery._packRule(partner, _BS_C.powerdeliveryPowerRoleSink, 0))

    @deprecated
    def setRequestDataObject(self, partner, rdo):
        """
        Sets the current Request Data Object (RDO) for a given partner.
        (Only the local partner can be changed.)

        RDOs:
            - Are provided by the sinking device.
            - Exist only after a successful PD negotiation (Otherwise zero).
            - Only one RDO can exist at a time. i.e. Either the Local or Remote partner RDO

        Args:
            partner (int): Indicates which side of the PD connection is in question.
                Local = 0 = powerdeliveryPartnerLocal
            rdo (int): RDO to be applied.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32_with_subindex(_BS_C.powerdeliveryRequestDataObject,
                                            PowerDelivery._packRule(partner,
                                                                    _BS_C.powerdeliveryPowerRoleSink,
                                                                    0),
                                            rdo)

    def setRequestDataObject(self, rdo):
        """
        Sets the current Request Data Object (RDO) for a given partner.
        (Only the local partner can be changed.)

        RDOs:
            - Are provided by the sinking device.
            - Exist only after a successful PD negotiation (Otherwise zero).
            - Only one RDO can exist at a time. i.e. Either the Local or Remote partner RDO

        Args:
            rdo (int): RDO to be applied.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32_with_subindex(_BS_C.powerdeliveryRequestDataObject,
                                            PowerDelivery._packRule(_BS_C.powerdeliveryPartnerLocal,
                                                                    _BS_C.powerdeliveryPowerRoleSink,
                                                                    0),
                                            rdo)

    def getPowerRole(self):
        """
        Gets the power role that is currently being advertised by the local partner. (CC Strapping).

        Returns:
            Result (object):
                value (int): The current power role
                    - Disabled = 0 = powerdeliveryPowerRoleDisabled
                    - Source = 1= powerdeliveryPowerRoleSource
                    - Sink = 2 = powerdeliveryPowerRoleSink
                    - Source/Sink = 3 = powerdeliveryPowerRoleSourceSink (Dual Role Port)

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryPowerRole)

    def setPowerRole(self, powerRole):
        """
        Sets the power role to be advertised by the Local partner. (CC Strapping).

        Args:
            powerRole (int) - Power role to be set.
                - Disabled = 0 = powerdeliveryPowerRoleDisabled
                - Source = 1= powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
                - Source/Sink = 3 = powerdeliveryPowerRoleSourceSink (Dual Role Port)

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.powerdeliveryPowerRole, powerRole)

    def getPowerRolePreferred(self):
        """
        Gets the preferred power role currently being advertised by the Local partner. (CC Strapping).

        Returns:
            Result (object):
                value (int): The current power role
                    - Disabled = 0 = powerdeliveryPowerRoleDisabled
                    - Source = 1= powerdeliveryPowerRoleSource
                    - Sink = 2 = powerdeliveryPowerRoleSink

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryPowerRolePreferred)

    def setPowerRolePreferred(self, powerRole):
        """
        Set the preferred power role to be advertised by the Local partner (CC Strapping).

        Args:
            powerRole (int) - Power role to be set.
                - Disabled = 0 = powerdeliveryPowerRoleDisabled
                - Source = 1= powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.powerdeliveryPowerRolePreferred, powerRole)

    def getCableVoltageMax(self):
        """
        Gets the maximum voltage capability reported by the e-mark of the attached cable.

        Returns:
            Result (object):
                value (int): An enumerated representation of voltage
                    - Unknown/Unattached (0)
                    - 20 Volts DC (1)
                    - 30 Volts DC (2)
                    - 40 Volts DC (3)
                    - 50 Volts DC (4)

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryCableVoltageMax)

    def getCableCurrentMax(self):
        """
        Gets the maximum current capability report by the e-mark of the attached cable

        Returns:
            Result (object):
                value (int): An enumerated representation of current
                    - Unknown/Unattached (0)
                    - 3 Amps (1)
                    - 5 Amps (2)

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryCableCurrentMax)

    def getCableSpeedMax(self):
        """
        Gets the maximum data rate capability reported by the e-mark of the attached cable.

        Returns:
            Result (object):
                value (int): An enumerated representation of the cables max speed
                    - Unknown/Unattached (0)
                    - USB 2.0 (1)
                    - USB 3.2 gen 1 (2)
                    - USB 3.2 / USB 4 gen 2 (3)
                    - USB 4 gen 3 (4)

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryCableSpeedMax)

    def getCableType(self):
        """
        Gets the cable type reported by the e-mark of the attached cable.

        Returns:
            Result (object):
                value (int): An enumerated representation of the cables max speed
                    - Invalid, no e-mark and not Vconn powered (0)
                    - Passive cable with e-mark (1)
                    - Active cable (2)

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryCableType)

    def getCableOrientation(self):
        """
        Gets the current orientation being used for PD communication

        Returns:
            Result (object):
                value (int): An enumerated representation of the cables max speed
                    - Unconnected = 0
                    - CC1 (1)
                    - CC2 (2)

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryCableOrientation)

    def request(self, request):
        """
        Requests an action of the Remote partner.
        Actions are not guaranteed to occur.

        Args:
            request (int) - Request to be issued to the remote partner
                - pdRequestHardReset (0)
                - pdRequestSoftReset (1)
                - pdRequestDataReset (2)
                - pdRequestPowerRoleSwap (3)
                - pdRequestPowerFastRoleSwap (4)
                - pdRequestDataRoleSwap (5)
                - pdRequestVconnSwap (6)
                - pdRequestSinkGoToMinimum (7)
                - pdRequestRemoteSourcePowerDataObjects (8)
                - pdRequestRemoteSinkPowerDataObjects (9)

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.powerdeliveryRequestCommand, request)

    def requestStatus(self):
        """
        Gets the status of the last request command sent.

        Returns:
            Result (object):
                value (int): the request status
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerDeliveryRequestStatus)

    def getOverride(self):
        """Gets the current enabled overrides

        Returns:
            Result (object):
                value (int): Bit mapped representation of the current override configuration.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryOverride)

    def setOverride(self, overrides):
        """Sets the current overrides.

        Args:
            overrides (int): Overrides to be set in a bit mapped representation.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.powerdeliveryOverride, overrides)

    def resetEntityToFactoryDefaults(self):
        """
        Resets the PowerDelivery Entity to it factory default configuration.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.call_UEI(_BS_C.powerdeliveryResetEntityToFactoryDefaults)

    def getFlagMode(self, flag):
        """
        Gets the current mode of the local partner flag/advertisement.
        These flags are apart of the first Local Power Data Object and must be managed in order to
        accurately represent the system to other PD devices. This API allows overriding of that feature.
        Overriding may lead to unexpected behaviors.

        Args:
            flag (int): Flag/Advertisement to be modified

        Returns:
            Result (object):
                value (int): The current mode of the provided flag
                    - Disabled (0)
                    - Enable (1)
                    - Auto (2) default

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI_with_param(_BS_C.powerdeliveryFlagMode, flag)

    def setFlagMode(self, flag, mode):
        """
        Sets how the local partner flag/advertisement is managed.
        These flags are apart of the first Local Power Data Object and must be managed in order to
        accurately represent the system to other PD devices. This API allows overriding of that feature.
        Overriding may lead to unexpected behaviors.

        Args:
            flag (int): Flag/Advertisement to be modified
            mode (int) - Mode to be set
                - Disabled (0)
                - Enable (1)
                - Auto (2) default

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8_with_subindex(_BS_C.powerdeliveryFlagMode, flag, mode)

    def getPeakCurrentConfiguration(self):
        """
        Gets the Peak Current Configuration for the Local Source.
        The peak current configuration refers to the allowable tolerance/overload
        capabilities in regards to the devices max current.  This tolerance includes
        a maximum value and a time unit.

        Returns:
            Result (object):
                value (int): An enumerated value referring to the current configuration.
                    -  Allowable values are 0 - 4

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryPeakCurrentConfiguration)

    def setPeakCurrentConfiguration(self, config):
        """
        Sets the Peak Current Configuration for the Local Source.
        The peak current configuration refers to the allowable tolerance/overload
        capabilities in regards to the devices max current.  This tolerance includes
        a maximum value and a time unit.

        Args:
            config (int): An enumerated value referring to the configuration to be set
                -  Allowable values are 0 - 4

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.powerdeliveryPeakCurrentConfiguration, config)

    def getFastRoleSwapCurrent(self):
        """
        Gets the Fast Role Swap Current
        The fast role swap current refers to the amount of current required by the
        Local Sink in order to successfully preform the swap.

        Returns:
            Result (object):
                value (int): An enumerated value referring to current swap value
                    - 0A (0)
                    - 900mA (1)
                    - 1.5A (2)
                    - 3A (3)

                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.powerdeliveryFastRoleSwapCurrent)

    def setFastRoleSwapCurrent(self, current):
        """
        Sets the Fast Role Swap Current
        The fast role swap current refers to the amount of current required by the
        Local Sink in order to successfully preform the swap.

        Args:
            current (int):An enumerated value referring to value to be set.
                - 0A (0)
                - 900mA (1)
                - 1.5A (2)
                - 3A (3)

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.powerdeliveryFastRoleSwapCurrent, current)

    @staticmethod
    def _checkPowerRole(powerRole):
        if powerRole != _BS_C.powerdeliveryPowerRoleSource and \
           powerRole != _BS_C.powerdeliveryPowerRoleSink:
            return Result.PARAMETER_ERROR
        else:
            return Result.NO_ERROR

    @staticmethod
    def _packRule(partner, powerRole, ruleIndex):
        return (((((powerRole-1) & 0x1) << 1) | (partner & 0x1)) << 6) | (ruleIndex & 0x3F)


class Rail(Entity):
    """ Provides power rail functionality on certain modules.

        This entity is only available on certain modules. The RailClass can
        be used to control power to downstream devices, I has the ability to
        take current and voltage measurements, and depending on hardware, may
        have additional modes and capabilities.

        Useful Constants:
            * KELVIN_SENSING_OFF (0)
            * KELVIN_SENSING_ON (1)
            * OPERATIONAL_MODE_AUTO (0)
            * OPERATIONAL_MODE_LINEAR (1)
            * OPERATIONAL_MODE_SWITCHER (2)
            * OPERATIONAL_MODE_SWITCHER_LINEAR (3)
            * DEFAULT_OPERATIONAL_MODE (OPERATIONAL_MODE_AUTO)
            * OPERATIONAL_STATE_INITIALIZING (0)
            * OPERATIONAL_STATE_ENABLED (1)
            * OPERATIONAL_STATE_FAULT (2)
            * OPERATIONAL_STATE_HARDWARE_CONFIG (8)
            * OPERATIONAL_STATE_LINEAR (0)
            * OPERATIONAL_STATE_SWITCHER (1)
            * OPERATIONAL_STATE_LINEAR_SWITCHER (2)
            * OPERATIONAL_STATE_OVER_VOLTAGE_FAULT (16)
            * OPERATIONAL_STATE_UNDER_VOLTAGE_FAULT (17)
            * OPERATIONAL_STATE_OVER_CURRENT_FAULT (18)
            * OPERATIONAL_STATE_OVER_POWER_FAULT (19)
            * OPERATIONAL_STATE_REVERSE_POLARITY_FAULT (20)
            * OPERATIONAL_STATE_OVER_TEMPERATURE_FAULT (21)
            * OPERATIONAL_STATE_OPERATING_MODE (24)
            * OPERATIONAL_STATE_CONSTANT_CURRENT (0)
            * OPERATIONAL_STATE_CONSTANT_VOLTAGE (1)
            * OPERATIONAL_STATE_CONSTANT_POWER (2)
            * OPERATIONAL_STATE_CONSTANT_RESISTANCE (3)
    """
    KELVIN_SENSING_OFF = 0
    KELVIN_SENSING_ON = 1
    OPERATIONAL_MODE_AUTO            = 0
    OPERATIONAL_MODE_LINEAR          = 1
    OPERATIONAL_MODE_SWITCHER        = 2
    OPERATIONAL_MODE_SWITCHER_LINEAR = 3
    DEFAULT_OPERATIONAL_MODE         = OPERATIONAL_MODE_AUTO
    OPERATIONAL_STATE_INITIALIZING           = 0
    OPERATIONAL_STATE_ENABLED                = 1
    OPERATIONAL_STATE_FAULT                  = 2
    OPERATIONAL_STATE_HARDWARE_CONFIG        = 8
    OPERATIONAL_STATE_LINEAR                 = 0
    OPERATIONAL_STATE_SWITCHER               = 1
    OPERATIONAL_STATE_LINEAR_SWITCHER        = 2
    OPERATIONAL_STATE_OVER_VOLTAGE_FAULT     = 16
    OPERATIONAL_STATE_UNDER_VOLTAGE_FAULT    = 17
    OPERATIONAL_STATE_OVER_CURRENT_FAULT     = 18
    OPERATIONAL_STATE_OVER_POWER_FAULT       = 19
    OPERATIONAL_STATE_REVERSE_POLARITY_FAULT = 20
    OPERATIONAL_STATE_OVER_TEMPERATURE_FAULT = 21
    OPERATIONAL_STATE_OPERATING_MODE         = 24
    OPERATIONAL_STATE_CONSTANT_CURRENT       = 0
    OPERATIONAL_STATE_CONSTANT_VOLTAGE       = 1
    OPERATIONAL_STATE_CONSTANT_POWER         = 2
    OPERATIONAL_STATE_CONSTANT_RESISTANCE    = 3

    def __init__(self, module, index):
        """Rail initializer"""
        super(Rail, self).__init__(module, _BS_C.cmdRAIL, index)

    def getCurrent(self):
        """Get the rail current.

            Return:
                Result: Result object, containing NO_ERROR and the current in microamps
                        or a non zero Error code.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railCurrent))

    def setCurrentSetpoint(self, microamps):
        """ Set the rail supply current.

            Rail current control capabilities vary between modules. Refer to the
            module datasheet for definition of the rail current capabilities.

            args:
                microamps (int): The current in micro-amps (1 == 1e-6A) to be supply by the rail.

            return:
                Result.error: Return NO_ERROR on success, or one of the common
                              sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.railCurrentSetpoint, microamps)

    def getCurrentSetpoint(self):
        """ Get the rail setpoint current.

            Rail current control capabilities vary between modules. Refer to the
            module datasheet for definition of the rail current capabilities.

            return:
                Result: Return result object with NO_ERROR set and the current
                rail current setting in the Result.value or an Error.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railCurrentSetpoint))

    def setCurrentLimit(self, microamps):
        """Set the rail current limit setting.

           Check product datasheet to see if this feature is available.

           args:
                microamps (int): The current in micro-amps (1 == 1e-6A).

           Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.railCurrentLimit, microamps)

    def getCurrentLimit(self):
        """ Get the rail current limit setting.

            Check product datasheet to see if this feature is available.

            args:
                microamps (int): The current in micro-amps (1 == 1e-6A).

            return:
                Result: Return result object with NO_ERROR set and the current
                        limit setting in the Result.value or an Error condition.
        """
        return self.get_UEI(_BS_C.railCurrentLimit)

    def getTemperature(self):
        """ Get the rail temperature.

            return:
                Result: Return result object with NO_ERROR set and the rail temperature
                in the Result.value or an Error condition.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railTemperature))

    def getEnable(self):
        """ Get the state of the rail switch.

            Not all rails can be switched on and off. Refer to the
            module datasheet for capability specification of the rails.

            return:
                Result: Return result object with NO_ERROR set and the current
                rail enable state in the Result.value or an Error condition.
        """
        return self.get_UEI(_BS_C.railEnable)

    def setEnable(self, bEnable):
        """ Set the state of the rail switch.

            Not all rails can be switched on and off. Refer to the
            module datasheet for capability specification of the rails.

            args:
                bEnable (bool): true: enable and connect to the supply rail voltage;
                                false: disable and disconnect from the supply rail voltage

            return:
                Result.error: Return NO_ERROR on success, or one of the common
                              sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.railEnable, bEnable)

    def getVoltage(self):
        """ Get the rail supply voltage.

            Rail voltage control capabilities vary between modules. Refer to the
            module datasheet for definition of the rail voltage capabilities.

            On some modules this is a measured value so may not exactly match what was
            previously set via the setVoltage interface. Refer to the module datasheet to
            to determine if this is a measured or stored value.

            return:
                Result: Return result object with NO_ERROR set and the current
                rail voltage setting in the Result.value or an Error.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railVoltage))

    def setVoltageSetpoint(self, microvolts):
        """ Set the rail supply voltage.

            Rail voltage control capabilities vary between modules. Refer to the
            module datasheet for definition of the rail voltage capabilities.

            args:
                microvolts (int): The voltage in micro-volts (1 == 1e-6V) to be supply by the rail.

            return:
                Result.error: Return NO_ERROR on success, or one of the common
                              sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.railVoltageSetpoint, microvolts)

    def getVoltageSetpoint(self):
        """ Get the rail setpoint voltage.

            Rail voltage control capabilities vary between modules. Refer to the
            module datasheet for definition of the rail voltage capabilities.

            return:
                Result: Return result object with NO_ERROR set and the current
                rail voltage setting in the Result.value or an Error.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railVoltageSetpoint))

    def setVoltageMinLimit(self, microvolts):
        """Set the rail voltage minimum limit setting.

           Check product datasheet to see if this feature is available.

           args:
                microvolts (int): The voltage minimum in micro-volts (1 == 1e-6V).

           Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.railVoltageMinLimit, microvolts)

    def getVoltageMinLimit(self):
        """ Get the rail voltage minimum limit setting.

            Check product datasheet to see if this feature is available.

            args:
                microvolts (int): The voltage minimum in micro-volts (1 == 1e-6V).

            return:
                Result: Return result object with NO_ERROR set and the voltage minimum
                        limit setting in the Result.value or an Error condition.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railVoltageMinLimit))

    def setVoltageMaxLimit(self, microvolts):
        """Set the rail voltage maximum limit setting.

           Check product datasheet to see if this feature is available.

           args:
                microvolts (int): The voltage maximum in micro-volts (1 == 1e-6V).

           Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.railVoltageMaxLimit, microvolts)

    def getVoltageMaxLimit(self):
        """ Get the rail voltage maximum limit setting.

            Check product datasheet to see if this feature is available.

            args:
                microvolts (int): The voltage maximum in micro-volts (1 == 1e-6V).

            return:
                Result: Return result object with NO_ERROR set and the voltage minimum
                        limit setting in the Result.value or an Error condition.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railVoltageMaxLimit))

    def getPower(self):
        """Get the rail power.

            Return:
                Result: Result object, containing NO_ERROR and the power in milliwatts
                        or a non zero Error code.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railPower))

    def setPowerSetpoint(self, milliwatts):
        """ Set the rail supply power.

            Rail power control capabilities vary between modules. Refer to the
            module datasheet for definition of the rail power capabilities.

            args:
                milliwatts (int): The power in milli-watts (1 == 1e-3W) to be supply by the rail.

            return:
                Result.error: Return NO_ERROR on success, or one of the common
                              sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.railPowerSetpoint, milliwatts)

    def getPowerSetpoint(self):
        """ Get the rail setpoint power.

            Rail power control capabilities vary between modules. Refer to the
            module datasheet for definition of the rail power capabilities.

            return:
                Result: Return result object with NO_ERROR set and the power
                rail power setting in the Result.value or an Error.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railPowerSetpoint))

    def setPowerLimit(self, milliwatts):
        """Set the rail power limit setting.

           Check product datasheet to see if this feature is available.

           args:
                milliwatts (int): The power in milli-watts (1 == 1e-3W).

           Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.railPowerLimit, milliwatts)

    def getPowerLimit(self):
        """ Get the rail power limit setting.

            Check product datasheet to see if this feature is available.

            args:
                milliwatts (int): The power in milli-watts (1 == 1e-3W).

            return:
                Result: Return result object with NO_ERROR set and the power
                        limit setting in the Result.value or an Error condition.
        """
        return self.get_UEI(_BS_C.railPowerLimit)

    def getResistance(self):
        """Get the rail resistance.

            Return:
                Result: Result object, containing NO_ERROR and the resistance in milliohms
                        or a non zero Error code.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railResistance))

    def setResistanceSetpoint(self, milliohms):
        """ Set the rail load resistance.

            Rail resistance control capabilities vary between modules. Refer to the
            module datasheet for definition of the rail resistance capabilities.

            args:
                milliohms (int): The resistance in milli-ohms (1 == 1e-3Ohms) to be applied to the rail.

            return:
                Result.error: Return NO_ERROR on success, or one of the common
                              sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.railResistanceSetpoint, milliohms)

    def getResistanceSetpoint(self):
        """ Get the rail setpoint resistance.

            Rail resistance control capabilities vary between modules. Refer to the
            module datasheet for definition of the rail resistance capabilities.

            return:
                Result: Return result object with NO_ERROR set and the resistance
                rail resistance setting in the Result.value or an Error.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.railResistanceSetpoint))

    def setKelvinSensingEnable(self, bEnable):
        """ Enable or Disable kelvin sensing on the module.

            Refer to the module datasheet for definition of the rail kelvin sensing capabilities.

            args:
                bEnable (bool): enable or disable kelvin sensing.

            return:
                Result.error: Return NO_ERROR on success, or one of the common
                              sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.railKelvinSensingEnable, bEnable)

    def getKelvinSensingEnable(self):
        """ Determine whether kelvin sensing is enabled or disabled.

            Refer to the module datasheet for definition of the rail kelvin
            sensing capabilities.

            args:
                bEnable (bool): Kelvin sensing is enabled or disabled.

            return:
                Result: Return result object with NO_ERROR set and the current
                rail kelvin sensing mode setting in the Result.value or an Error.
        """
        return self.get_UEI(_BS_C.railKelvinSensingMode)

    def getKelvinSensingState(self):
        """ Determine whether kelvin sensing has been disabled by the system.

            Refer to the module datasheet for definition of the rail kelvin
            sensing capabilities.

            return:
                Result: Return result object with NO_ERROR set and the current
                rail kelvin sensing state setting in the Result.value or an Error.
        """
        return self.get_UEI(_BS_C.railKelvinSensingState)

    def setOperationalMode(self, mode):
        """ Set the operational mode of the rail.

            Refer to the module datasheet for definition of the rail operational capabilities.

            args:
                mode (int): The operational mode to employ.

            return:
                Result.error: Return NO_ERROR on success, or one of the common
                          sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.railOperationalMode, mode)

    def getOperationalMode(self):
        """ Determine the current operational mode of the system.

            Refer to the module datasheet for definition of the rail operational
            mode capabilities.

            return:
                Result: Return result object with NO_ERROR set and the current
                rail operational mode setting in the Result.value or an Error.
        """
        return self.get_UEI(_BS_C.railOperationalMode)

    def getOperationalState(self):
        """ Determine the current operational state of the system.

        Refer to the module datasheet for definition of the rail operational states.

        return:
            Result: Return result object with NO_ERROR set and the current
            rail operational state in the Result.value or an Error.
        """
        return self.get_UEI(_BS_C.railOperationalState)

    def clearFaults(self):
        """ Clears the current fault state of the rail.

        Refer to the module datasheet for definition of the rail faults.

        return:
            Result: Return result object with NO_ERROR set or an Error.
        """
        return self.call_UEI(_BS_C.railClearFaults)


class RCServo(Entity):
    """ Provides RCServo functionality on certain modules.

        This entity is only available on certain modules. The RCServoClass can
        be used to interpret and control RC Servo signals and motors via the digital
        pins.

        Useful Constants:
            * SERVO_DEFAULT_POSITION (128)
            * SERVO_DEFAULT_MIN (64)
            * SERVO_DEFAULT_MAX (192)
    """

    SERVO_DEFAULT_POSITION = 128
    SERVO_DEFAULT_MIN = 64
    SERVO_DEFAULT_MAX = 192

    def __init__(self, module, index):
        super(RCServo, self).__init__(module, _BS_C.cmdSERVO, index)

    def setEnable(self, enable):
        """ Enable the servo channel.

            Param:
                enable (bool): The state to be set. 0 is disabled, 1 is enabled

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.servoEnable, enable)

    def getEnable(self):
        """ Get the enable status of the servo channel.

            If the enable status is 0 the servo channel is disabled, if the status
            is 1 the channel is enabled.

            Return:
                Result: Result object, containing NO_ERROR and servo enable status
                        or a non zero Error code.
        """

        return self.get_UEI(_BS_C.servoEnable)

    def setPosition(self, position):
        """ Set the position of the servo channel.

            Param:
                position (int): The position to be set. With the default configuration
                64 = a 1ms pulse and 192 = a 2ms pulse.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.servoPosition, position)

    def getPosition(self):
        """ Get the position of the servo channel.

            Default configuration: 1ms = 64 and 2ms = 192

            Return:
                Result: Result object, containing NO_ERROR and the servo position
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.servoPosition)

    def setReverse(self, reverse):
        """ Se the output to be reverse on the servo channel.

            Param:
                reverse (bool): Reverse mode: 0 = not reversed, 1 = reversed.
                ie: setPosition of 64 would actually apply 192 tot he servo output;
                however, getPosition will return 64.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.servoReverse, reverse)

    def getReverse(self):
        """ Get the reverse status of the channel.

            0 = not reversed, 1 = reversed

            Return:
                Result: Result object, containing NO_ERROR and the reverse status
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.servoReverse)


class Relay(Entity):
    """ The RelayClass is the interface to relay entities on BrainStem modules.

        Relay entities may be enabled (set) or disabled (cleared low).
        Other capabilities may be available, please see the product
        datasheet.

        Useful Constants:
            * VALUE_LOW (0)
            * VALUE_HIGH (1)
    """

    VALUE_LOW = 0
    VALUE_HIGH = 1

    def __init__(self, module, index):
        """Relay Entity initializer"""
        super(Relay, self).__init__(module, _BS_C.cmdRELAY, index)

    def setEnable(self, bEnable):
        """ Enables or disables the relay based on bEnable.

            Param:
                bEnable (int): Set 1 for enable, set 0 for disable.

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.relayEnable, bEnable)

    def getEnable(self):
        """ Get the relay enable state.

            A return of 1 indicates the relay is enabled.
            A return of 0 indicates the relay is disabled.

            return:
                Result: Result object, containing NO_ERROR and digital state
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.relayEnable)

    def getVoltage(self):
        """ Get the scaled micro volt value with refrence to ground.

            Get a 32 bit signed integer (in micro Volts) based on the boards
            ground and refrence voltages.

            Note:
                Not all modules provide 32 bits of accuracy; Refer to the module's
                datasheet to determine the analog bit depth and reference voltage.

            return:
                Result: Result object, containing NO_ERROR and microVolts value
                        or a non zero Error code.

        """
        return _BS_SignCheck(self.get_UEI(_BS_C.relayVoltage))


class Signal(Entity):
    """ The Signal Class is the interface to digital pins configured to produce square wave signals.

        This class is designed to allow for square waves at various frequencies and duty cycles. Control
        is defined by specifying the wave period as (T3Time) and the active portion of the cycle as (T2Time).
        See the entity overview section of the reference for more detail regarding the timiing.

    """

    def __init__(self, module, index):
        """ Signal Entity initializer """
        super(Signal, self).__init__(module, _BS_C.cmdSIGNAL, index)

    def setEnable(self, enable):
        """
        Enable/Disable the signal output.

        :param enable: True to enable, false to disable
        :return: Result.error Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.signalEnable, enable)

    def getEnable(self):
        """ Get the Enable/Disable of the signal.

        :return: Result object, containing NO_ERROR and boolean value True for enabled False for disabled
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.signalEnable)

    def setInvert(self, invert):
        """ Invert the signal output.

            Normal mode is High on t0 then low at t2.
            Inverted mode is Low at t0 on period start and high at t2.

            :param invert: True to invert, false for normal mode.
            :return: Result.error Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.signalInvert, invert)

    def getInvert(self):
        """ Get the invert status of the signal.

            :return: Result object, containing NO_ERROR and boolean value True for inverted False for normal
                     or a non zero Error code.
        """
        return self.get_UEI(_BS_C.signalInvert)

    def setT3Time(self, t3_nsec):
        """ Set the signal period or T3 in nanoseconds.

            :param t3_nsec: Tnteger not larger than unsigned 32 bit max value representing the wave period in nanoseconds.
            :return: Result.error Return NO_ERROR on success, or one of the common
                     sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.signalT3Time, t3_nsec)

    def getT3Time(self):
        """ Get the current wave period (T3) in nanoseconds.

            :return: Result object, containing NO_ERROR and an integer value not larger than the max unsigned 32bit value.
                     or a non zero Error code.
        """
        return self.get_UEI(_BS_C.signalT3Time)

    def setT2Time(self, t2_nsec):
        """ Set the signal active period or T2 in nanoseconds.

            :param t2_nsec: Tnteger not larger than unsigned 32 bit max value representing the wave active period in nanoseconds.
            :return: Result.error Return NO_ERROR on success, or one of the common
                     sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.signalT2Time, t2_nsec)

    def getT2Time(self):
        """ Get the current wave active period (T2) in nanoseconds.

            :return: Result object, containing NO_ERROR and an integer value not larger than the max unsigned 32bit value.
                     or a non zero Error code.
        """
        return self.get_UEI(_BS_C.signalT2Time)


class Store(Entity):
    """ Access the store on a BrainStem Module.

        The store provides a flat file system on modules that have storage capacity.
        Files are referred to as slots and they have simple zero-based numbers
        for access. Store slots can be used for generalized storage and commonly
        contain compiled reflex code (files ending in .map) or templates used by the
        system. Slots simply contain bytes with no expected organization but
        the code or use of the slot may impose a structure.

        Stores have fixed indices based on type. Not every module contains a
        store of each type. Consult the module datasheet for details on which
        specific stores are implemented, if any, and the capacities of
        implemented stores.

        Useful Constants:
            * INTERNAL_STORE (0)
            * RAM_STORE (1)
            * SD_STORE (2)
            * EEPROM_STORE (3)
    """

    INTERNAL_STORE = 0
    RAM_STORE = 1
    SD_STORE = 2
    EEPROM_STORE = 3

    def __init__(self, module, index):
        """Store initializer"""
        super(Store, self).__init__(module, _BS_C.cmdSTORE, index)

    def getSlotState(self, slot):
        """ Get slot state.

            Slots which contain reflexes may be "enabled," i.e. the reflexes
            contained in the slot are active.

            args:
                slot (int): The slot number.

            return: Result:
                Return result object with NO_ERROR set and the current state of the slot in the Result.value or an Error.
        """
        return self.get_UEI_with_param(_BS_C.storeSlotState, slot)

    def loadSlot(self, slot, data, _=None):
        """ Load the slot.

            args:
                slot (int): The slot number.
                data (str, bytes): The data.
                _ (int): (length Deprecated) Unused parameter, and will be removed in next minor release.

            return: Result.error:
                Return NO_ERROR on success, or one of the common sets of return error codes on failure.
        """
        if self.module.link is None:
            return Result.CONNECTION_ERROR

        capacity = self.getSlotCapacity(slot)
        if capacity.error != Result.NO_ERROR:
            return capacity.error

        data = str_or_bytes_to_bytearray(data)
        length = len(data)

        if length > capacity.value:
            return Result.SIZE_ERROR

        try:
            with self._open(slot, _BS_C.slotOpenWrite) as handle:
                count = 0
                match = ([_BS_C.slotWrite, _BS_C.slotWrite | _BS_C.bitSlotError], handle)
                result = Result(_BS_C.aErrNone, None)
                while count < length:
                    packet = struct.pack('BB', _BS_C.slotWrite, handle)
                    block = length - count

                    if block > (_BS_C.MAX_PACKET_BYTES - 3):  # 3 = (cmdSLOT, slotWrite, handle)
                        block = (_BS_C.MAX_PACKET_BYTES - 3)

                    blocksum = 0
                    for i in data[count:count + block]:
                        blocksum += i
                    blocksum &= 255

                    packet = packet + bytes(data[count:(count + block)])

                    result._error = self.module.link.send_command_packet(self.module.address,
                                                                         _BS_C.cmdSLOT,
                                                                         len(packet), packet)
                    if result.error != Result.NO_ERROR:
                        break

                    result = self.module.link.receive_command_packet(self.module.address,
                                                                     _BS_C.cmdSLOT,
                                                                     match, 1000)

                    if result.error != Result.NO_ERROR:
                        break

                    vals = str_or_bytes_to_bytearray(result.value, 0, 4)
                    if (vals[1] & _BS_C.bitSlotError) > 0:
                        result._error = vals[3]
                        result._value = None
                    elif blocksum != vals[3]:
                        result._error = Result.IO_ERROR
                        result._value = None
                    else:
                        count = count + block

        except _ResourceException:
            result = Result(_BS_C.aErrResource, None)
        except TypeError:
            result = Result(_BS_C.aErrParam, None)

        return result.error

    def unloadSlot(self, slot):
        """ Unload the slot data.

            args:
                slot (int): The slot number.

            return: Result:
                    Either Returns Result object with NO_ERROR set
                    and its value attribute set with an object of type bytes containing the unloaded data.
                    Or a Result object with a non-zero error.
        """
        result = self.getSlotSize(slot)
        size = result.value if result.error == Result.NO_ERROR else 0

        try:
            with self._open(slot, _BS_C.slotOpenRead) as handle:
                count = 0
                data = struct.pack('BB', _BS_C.slotRead, handle)
                match = ([_BS_C.slotRead, _BS_C.slotRead | _BS_C.bitSlotError], handle)
                result_data = b''
                while result.error == Result.NO_ERROR and count < size:
                    if self.module.link is None:
                        result = Result(_BS_C.aErrConnection, None)
                        break
                    else:
                        error = self.module.link.send_command_packet(self.module.address, _BS_C.cmdSLOT, 2, data)
                        if error == Result.NO_ERROR:
                            result = self.module.link.receive_command_packet(self.module.address,
                                                                             _BS_C.cmdSLOT,
                                                                             match, 1000)

                        if result.error == Result.NO_ERROR:
                            vals = str_or_bytes_to_bytearray(result.value, 0, 4)
                            length = result._length
                            if (vals[1] & _BS_C.bitSlotError) > 0:
                                result._error = vals[3]
                                result._value = None
                            else:
                                count = count + (length - 3)
                                result_data = result_data + result.value[3:length]

                result = Result(result.error, result_data)
        except _ResourceException:
            result = Result(_BS_C.aErrResource, None)

        return result

    def slotEnable(self, slot):
        """ Enable the slot """
        return self.set_UEI8(_BS_C.storeSlotEnable, slot)

    def slotDisable(self, slot):
        """ Disable the slot"""
        return self.set_UEI8(_BS_C.storeSlotDisable, slot)

    def getSlotCapacity(self, slot):
        """ Get the slot capacity.

            Returns the Capacity of the slot, i.e. The number of bytes it can hold.

            return: Result:
                Either the capacity of the slot in Result.value or an error.
        """
        result = Result(_BS_C.aErrNone, None)
        # [slotCapacity, store, slot]
        data = struct.pack('BBB', _BS_C.slotCapacity, self.index, slot)
        match = ([_BS_C.slotCapacity, _BS_C.slotCapacity | _BS_C.bitSlotError], self.index, slot)
        if self.module.link is None:
            return Result(_BS_C.aErrConnection, None)
        else:
            result._error = self.module.link.send_command_packet(self.module.address, _BS_C.cmdSLOT, 3, data)
            if result.error == Result.NO_ERROR:
                result = self.module.link.receive_command_packet(self.module.address, _BS_C.cmdSLOT, match)
        if result.error == Result.NO_ERROR:
            # Look into packet...
            vals = str_or_bytes_to_bytearray(result.value)
            # If theres an error we return that in the result, and set value to None.
            try:
                if (vals[1] & _BS_C.bitSlotError) > 0:
                    result._error = vals[4]
                    result._value = None
                else:
                    result._value = (vals[4] << 8) + vals[5]

            except IndexError:
                result._error = Result.IO_ERROR
                result._value = None

        return result

    def getSlotSize(self, slot):
        """ Get the slot size.

            Returns the size of the data currently filling the slot in bytes.

            return: Result:
                Either the size of the slot in Result.value or an error.
        """
        result = Result(_BS_C.aErrNone, None)
        # [slotSize, store, slot]
        data = struct.pack('BBB', _BS_C.slotSize, self.index, slot)
        match = ([_BS_C.slotSize, _BS_C.slotSize | _BS_C.bitSlotError], self.index, slot)
        if self.module.link is None:
            return Result(_BS_C.aErrConnection, None)
        else:
            result._error = self.module.link.send_command_packet(self.module.address, _BS_C.cmdSLOT, 3, data)
            if result.error == Result.NO_ERROR:
                result = self.module.link.receive_command_packet(self.module.address, _BS_C.cmdSLOT, match)
        if result.error == Result.NO_ERROR:
            # Look into packet...
            vals = str_or_bytes_to_bytearray(result.value)
            # If theres an error we return that in the result, and set value to None.
            try:
                if (vals[1] & _BS_C.bitSlotError) > 0:
                    result._error = vals[4]
                    result._value = None
                else:
                    result._value = (vals[4] << 8) + vals[5]

            except IndexError:
                result._error = Result.IO_ERROR
                result._value = None

        return result

    def getSlotLocked(self, slot):
        """ Gets the current lock state of the slot
            Allows for write protection on a slot.

        Args:
            slot (int): The slot number

        Returns:
            Result (object):
                value: The current locked state of the provided slot.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI_with_param(_BS_C.storeLock, slot)

    def setSlotLocked(self, slot, lock):
        """ Sets the locked state of the slot
            Allows for write protection on a slot.

        Args:
            slot (int): The slot number
            lock (bool): Locked state to set.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.storeLock, slot, lock)

    @contextmanager
    def _open(self, slot, rw_access):
        handle = None
        try:
            result = self._openSlot(slot, rw_access)
            if result.error == Result.NO_ERROR:
                handle = result.value
                yield result.value
            else:
                raise _ResourceException("Error: %d", result.error)
        finally:
            if handle is not None:
                self._closeSlot(handle)

    def _openSlot(self, slot, rw_access):
        result = Result(_BS_C.aErrNone, None)
        # [slotOpenRead| slotOpenWrite, store, slot]
        data = struct.pack('BBB', rw_access, self.index, slot)
        match = ([rw_access, rw_access | _BS_C.bitSlotError], self.index, slot)
        if self.module.link is None:
            return Result(_BS_C.aErrConnection, None)
        else:
            result._error = self.module.link.send_command_packet(self.module.address, _BS_C.cmdSLOT, 3, data)
            if result.error == Result.NO_ERROR:
                result = self.module.link.receive_command_packet(self.module.address, _BS_C.cmdSLOT, match)
        if result.error == Result.NO_ERROR:
            # Look into packet...
            vals = str_or_bytes_to_bytearray(result.value)
            # If theres an error we return that in the result, and set value to None.
            try:
                if (vals[1] & _BS_C.bitSlotError) > 0:
                    result._error = vals[4]
                    result._value = None
                else:
                    result._value = vals[4]

            except IndexError:
                result._error = Result.IO_ERROR
                result._value = None

        return result

    def _closeSlot(self, handle):
        result = Result(_BS_C.aErrNone, None)
        # [slotClose, handle]
        data = struct.pack('BB', _BS_C.slotClose, handle)
        match = ([_BS_C.slotClose, _BS_C.slotClose | _BS_C.bitSlotError], handle)
        if self.module.link is None:
            return Result(_BS_C.aErrConnection, None)
        else:
            result._error = self.module.link.send_command_packet(self.module.address, _BS_C.cmdSLOT, 2, data)
            if result.error == Result.NO_ERROR:
                result = self.module.link.receive_command_packet(self.module.address, _BS_C.cmdSLOT, match)
        if result.error == Result.NO_ERROR:
            # Look into packet...
            vals = str_or_bytes_to_bytearray(result.value)
            # If theres an error we return that in the result, and set value to None.
            try:
                if (vals[1] & _BS_C.bitSlotError) > 0:
                    result._error = vals[3]
                    result._value = None
                else:
                    result._value = True

            except IndexError:
                result._error = Result.IO_ERROR
                result._value = None

        return result


class Temperature(Entity):
    """ Provide interface to temperature sensor.

        This entitiy is only available on certain modules, and provides a
        temperature reading in microcelsius.
    """

    def __init__(self, module, index):
        """Temperature object initializer"""
        super(Temperature, self).__init__(module, _BS_C.cmdTEMPERATURE, index)

    def getValue(self):
        """ Get the current temperature in micro-C.

        Returns:
            Result (object):
                value: The temperature in micro-C (uC)
                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.temperatureMicroCelsius))

    def getValueMin(self):
        """ Get the module's minimum temperature in micro-C since the last power cycle.

        Returns:
            Result (object):
                value: The minimum temperature in micro-C (uC)
                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.temperatureMinimumMicroCelsius))

    def getValueMax(self):
        """ Get the module's maximum temperature in micro-C since the last power cycle.

        Returns:
            Result (object):
                value: The maximum temperature in micro-C (uC)
                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.temperatureMaximumMicroCelsius))

    def reset(self):
        """ Get the module's maximum temperature in micro-C since the last power cycle.

        Returns:
            Result (object):
                value: The maximum temperature in micro-C (uC)
                error: Non-zero BrainStem error code on failure.
        """
        return _BS_SignCheck(self.get_UEI(_BS_C.temperatureMaximumMicroCelsius))

    def resetEntityToFactoryDefaults(self):
        """Resets the TemperatureClass Entity to it factory default configuration.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.call_UEI(_BS_C.portResetEntityToFactoryDefaults)


class Timer(Entity):
    """ Schedules events to occur at future times.

        Reflex routines can be written which will be executed upon expiration
        of the timer entity. The timer can be set to fire only once, or to
        repeat at a certain interval.

        Useful Constants:
            * SINGLE_SHOT_MODE (0)
            * REPEAT_MODE (1)
            * DEFAULT_MODE (SINGLE_SHOT_MODE)

    """

    SINGLE_SHOT_MODE = 0
    REPEAT_MODE = 1
    DEFAULT_MODE = SINGLE_SHOT_MODE

    def __init__(self, module, index):
        """Timer object initializer"""
        super(Timer, self).__init__(module, _BS_C.cmdTIMER, index)

    def getExpiration(self):
        """ Get the currently set expiration time in microseconds.

            This is not a "live" timer. That is, it shows the expiration time
            originally set with setExpiration; it does not "tick down" to show
            the time remaining before expiration.

            return:
                Result: Return result object with NO_ERROR set and the timer
                expiration in uSeconds in the Result.value or an Error.
        """
        return self.get_UEI(_BS_C.timerExpiration)

    def setExpiration(self, usecDuration):
        """ Set the expiration time for the timer entity.

            When the timer expires, it will fire the associated timer[index]() reflex.

            args:
                usecDuration (int): The duration before timer expiration in microseconds.

            return:
                Result.error: Return NO_ERROR on success, or one of the common
                          sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.timerExpiration, usecDuration)

    def getMode(self):
        """ Get the mode of the timer.

            Valid timer modes are single mode and repeat mode.

            return:
                Result: Return result object with NO_ERROR set and the timer mode
                either single (0) or repeat (1) in the Result.value or an Error.
        """
        return self.get_UEI(_BS_C.timerMode)

    def setMode(self, mode):
        """ Set the mode of the timer.

            args:
                mode (int): The mode of the timer. aTIMER_MODE_REPEAT or aTIMER_MODE_SINGLE.

            return:
                Result.error: Return NO_ERROR on success, or one of the common
                          sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.timerMode, mode)


class UART(Entity):
    """ Provides UART entity access on certain BrainStem modules.

        A UART is a "Universal Asynchronous Reciever/Transmitter".  Many times
        referred to as a COM (communication), Serial, or TTY (teletypewriter) port.

        The UART Class allows the enabling and disabling of the UART data lines
    """

    def __init__(self, module, index):
        """ UART entity initializer"""
        super(UART, self).__init__(module, _BS_C.cmdUART, index)

    def setEnable(self, bEnable):
        """ Enable the UART.

            Param:
                bEnable (bool): True = Enable, False = Disable

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.uartEnable, bEnable)

    def getEnable(self):
        """ Get the enable status of the UART.

            Return:
                Result: Result object, containing NO_ERROR and the UART state
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.uartEnable)

    def setBaudRate(self, rate):
        """ Set the Baud rate of the UART.

            Param:
                rate (int):

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI32(_BS_C.uartBaudRate, rate)

    def getBaudRate(self):
        """ Get the Baud rate of the UART.

            Return:
                Result: Result object, containing NO_ERROR and the UART baud rate
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.uartBaudRate)

    def setProtocol(self, protocol):
        """ Set the protocol format of the UART.

            Param:
                protocol (int):

            Return:
                Result.error: Return NO_ERROR on success, or one of the common
                sets of return error codes on failure.
        """
        return self.set_UEI8(_BS_C.uartProtocol, protocol)

    def getProtocol(self):
        """ Get the protocol format of the UART.

            Return:
                Result: Result object, containing NO_ERROR and the UART protocol
                        or a non zero Error code.
        """
        return self.get_UEI(_BS_C.uartProtocol)


class USB(Entity):
    """ USBClass provides methods to interact with a USB hub and USB switches.

        Different USB hub products have varying support; check the
        datasheet to understand the capabilities of each product.

        Useful Constants:
            * UPSTREAM_MODE_AUTO (2)
            * UPSTREAM_MODE_PORT_0 (0)
            * UPSTREAM_MODE_PORT_1 (1)
            * UPSTREAM_MODE_NONE (255)
            * DEFAULT_UPSTREAM_MODE (UPSTREAM_MODE_AUTO)

            * UPSTREAM_STATE_PORT_0 (0)
            * UPSTREAM_STATE_PORT_1 (1)

            * BOOST_0_PERCENT (0)
            * BOOST_4_PERCENT (1)
            * BOOST_8_PERCENT (2)
            * BOOST_12_PERCENT (3)

            * PORT_MODE_SDP (0)
            * PORT_MODE_CDP (1)
            * PORT_MODE_CHARGING (2)
            * PORT_MODE_PASSIVE (3)
            * PORT_MODE_USB2_A_ENABLE (4)
            * PORT_MODE_USB2_B_ENABLE (5)
            * PORT_MODE_VBUS_ENABLE (6)
            * PORT_MODE_SUPER_SPEED_1_ENABLE (7)
            * PORT_MODE_SUPER_SPEED_2_ENABLE (8)
            * PORT_MODE_USB2_BOOST_ENABLE (9)
            * PORT_MODE_USB3_BOOST_ENABLE (10)
            * PORT_MODE_AUTO_CONNECTION_ENABLE (11)
            * PORT_MODE_CC1_ENABLE (12)
            * PORT_MODE_CC2_ENABLE (13)
            * PORT_MODE_SBU_ENABLE (14)
            * PORT_MODE_CC_FLIP_ENABLE (15)
            * PORT_MODE_SS_FLIP_ENABLE (16)
            * PORT_MODE_SBU_FLIP_ENABLE (17)
            * PORT_MODE_USB2_FLIP_ENABLE (18)
            * PORT_MODE_CC1_INJECT_ENABLE (19)
            * PORT_MODE_CC2_INJECT_ENABLE (20)

            * PORT_SPEED_NA (0)
            * PORT_SPEED_HISPEED (1)
            * PORT_SPEED_SUPERSPEED (2)
    """

    UPSTREAM_MODE_AUTO = 2
    UPSTREAM_MODE_PORT_0 = 0
    UPSTREAM_MODE_PORT_1 = 1
    UPSTREAM_MODE_NONE = 255
    DEFAULT_UPSTREAM_MODE = UPSTREAM_MODE_AUTO

    UPSTREAM_STATE_PORT_0 = 0
    UPSTREAM_STATE_PORT_1 = 1

    BOOST_0_PERCENT = 0
    BOOST_4_PERCENT = 1
    BOOST_8_PERCENT = 2
    BOOST_12_PERCENT = 3

    PORT_MODE_SDP = 0
    PORT_MODE_CDP = 1
    PORT_MODE_CHARGING = 2
    PORT_MODE_PASSIVE = 3
    PORT_MODE_USB2_A_ENABLE = 4
    PORT_MODE_USB2_B_ENABLE = 5
    PORT_MODE_VBUS_ENABLE = 6
    PORT_MODE_SUPER_SPEED_1_ENABLE = 7
    PORT_MODE_SUPER_SPEED_2_ENABLE = 8
    PORT_MODE_USB2_BOOST_ENABLE = 9
    PORT_MODE_USB3_BOOST_ENABLE = 10
    PORT_MODE_AUTO_CONNECTION_ENABLE = 11
    PORT_MODE_CC1_ENABLE = 12
    PORT_MODE_CC2_ENABLE = 13
    PORT_MODE_SBU_ENABLE = 14
    PORT_MODE_CC_FLIP_ENABLE = 15
    PORT_MODE_SS_FLIP_ENABLE = 16
    PORT_MODE_SBU_FLIP_ENABLE = 17
    PORT_MODE_USB2_FLIP_ENABLE = 18
    PORT_MODE_CC1_INJECT_ENABLE = 19
    PORT_MODE_CC2_INJECT_ENABLE = 20

    PORT_SPEED_NA = 0
    PORT_SPEED_HISPEED = 1
    PORT_SPEED_SUPERSPEED = 2

    def __init__(self, module, index):
        """USBClass initializer"""
        super(USB, self).__init__(module, _BS_C.cmdUSB, index)

    def setPortEnable(self, channel):
        """Enable both power and data lines for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbPortEnable, channel)

    def setPortDisable(self, channel):
        """Disable both power and data lines for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbPortDisable, channel)

    def setDataEnable(self, channel):
        """Enable just the data lines for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbDataEnable, channel)

    def setDataDisable(self, channel):
        """Disable just the data lines for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbDataDisable, channel)

    def setHiSpeedDataEnable(self, channel):
        """Enable Hi-Speed (USB2.0) data transfer for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbHiSpeedDataEnable, channel)

    def setHiSpeedDataDisable(self, channel):
        """Disable Hi-Speed (USB2.0) data transfer for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbHiSpeedDataDisable, channel)

    def setSuperSpeedDataEnable(self, channel):
        """Enable SuperSpeed (USB3.0) data transfer for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbSuperSpeedDataEnable, channel)

    def setSuperSpeedDataDisable(self, channel):
        """Disable SuperSpeed (USB3.0) data transfer for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbSuperSpeedDataDisable, channel)

    def setPowerEnable(self, channel):
        """Enable just the power line for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbPowerEnable, channel)

    def setPowerDisable(self, channel):
        """Disable just the power line for a USB port.

        Args:
            channel (int): The USB port number

        Returns (int):
            Non-zero BrainStem error code on failure.
        """

        return self.set_UEI8(_BS_C.usbPowerDisable, channel)

    def getPortCurrent(self, channel):
        """Get the current through the power line for a port.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.usbPortCurrent, channel))

    def getPortVoltage(self, channel):
        """Get the voltage on the power line for a port.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.usbPortVoltage, channel))

    def getHubMode(self):
        """Get a bit mapped representation of the hub mode.
            Usually represents the port data and power lines enable/disable
            state in one bit packed result.
            See the product datasheet for state mapping.

        Returns: Result object
        """
        return self.get_UEI(_BS_C.usbHubMode)

    def setHubMode(self, mode):
        """Set a bit mapped representation of the hub mode.
            Usually represents the port data and power lines enable/disable.
            See the product datasheet for state mapping.

        Args:
            mode (int): The hub state

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.usbHubMode, mode)

    def clearPortErrorStatus(self, channel):
        """Clear the error status for the given channel.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return self.set_UEI8(_BS_C.usbPortClearErrorStatus, channel)

    def getUpstreamMode(self):
        """Get the upstream switch mode for the USB upstream ports.

        Returns: Result object
        """
        return self.get_UEI(_BS_C.usbUpstreamMode)

    def setUpstreamMode(self, mode):
        """Set the upstream switch mode for the USB upstream ports

        Args:
            mode (int):
                * Auto: UPSTREAM_MODE_AUTO = 2
                * Port 0: UPSTREAM_STATE_PORT_0 = 0
                * Port 1: UPSTREAM_STATE_PORT_1 = 1

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbUpstreamMode, mode)

    def getUpstreamState(self):
        """Get the upstream switch state for the USB upstream ports.

        Returns: Result object
            Result value 2 if no ports plugged in; 0 if port0 is active,
            1 if port1 is active.
        """
        return self.get_UEI(_BS_C.usbUpstreamState)

    def setEnumerationDelay(self, ms_delay):
        """Set the interport enumeration delay in milliseconds.
            This setting must be saved with a stem.system.save() call for it to be active.
            This setting is persistent across hub power down. Resetting the hub will
            return this setting to the default value of 0ms.

        Args:
            ms_delay (int): Interport delay in milliseconds

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.usbHubEnumerationDelay, ms_delay)

    def getEnumerationDelay(self):
        """Get the interport enumeration delay in milliseconds.

        Returns: Result object
        """
        return self.get_UEI(_BS_C.usbHubEnumerationDelay)

    def setPortCurrentLimit(self, channel, microAmps):
        """Set the current limit for the port. If the set limit is not achievable,
            devices will round down to the nearest available current limit setting.
            This setting can be saved with a stem.system.save() call to make it persistent.

        Args:
            channel (int): Port index.
            microAmps (int): The current limit setting in microAmps (1A=10e6)

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32_with_subindex(_BS_C.usbPortCurrentLimit, channel, microAmps)

    def getPortCurrentLimit(self, channel):
        """Get the current limit for the port.

        Returns: Result object
        """
        return self.get_UEI_with_param(_BS_C.usbPortCurrentLimit, channel)

    def setPortMode(self, channel, mode):
        """Set the mode for the Port.
            The mode is a bitmapped representation of the capabilities of the
            usb port. These capabilities change for each of the BrainStem devices
            which implement the usb entity. See your device reference page for a complete
            list of capabilities. Some devices use a common bit mapping for port
            mode at \ref usbPortMode

        Args:
            channel (int): Port Index.
            mode (int): The port mode setting as packed bit field.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32_with_subindex(_BS_C.usbPortMode, channel, mode)

    def getPortMode(self, channel):
        """Get the mode for the Port.
            The mode is a bitmapped representation of the capabilities of the
            usb port. These capabilities change for each of the BrainStem devices
            which implement the usb entity. See your device reference page for a complete
            list of capabilities. Some devices use a common bit mapping for port
            mode at \ref usbPortMode

           Returns: Result object
        """
        return self.get_UEI_with_param(_BS_C.usbPortMode, channel)

    def getPortState(self, channel):
        """Get the state for the Port.

           Returns: Result object
        """
        return self.get_UEI_with_param(_BS_C.usbPortState, channel)

    def getPortError(self, channel):
        """Get the error for the Port.

           Returns: Result object
        """
        return self.get_UEI_with_param(_BS_C.usbPortError, channel)

    def setUpstreamBoostMode(self, setting):
        """Set the upstream boost mode.
            Boost mode increases the drive strength of the USB data signals (power signals
            are not changed). Boosting the data signal strength may help to overcome
            connectivity issues when using long cables or connecting through "pogo" pins.
            Possible modes are 0 - no boost, 1 - 4%% boost, 2 - 8%% boost,
            3 - 12%% boost. This setting is not applied until a stem.system.save() call
            and power cycle of the hub. Setting is then persistent until changed or the hub
            is reset. After reset, default value of 0%% boost is restored.

        Args:
            setting (int): Upstream boost setting 0, 1, 2, or 3.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbUpstreamBoostMode, setting)

    def getUpstreamBoostMode(self):
        """Get the upstream boost mode.

        Returns: Result object
            Result value 0 - no boost, 1 - 4%% boost, 2 - 8%% boost, 3 - 12%% boost.
        """
        return self.get_UEI(_BS_C.usbUpstreamBoostMode)

    def setDownstreamBoostMode(self, setting):
        """Set the downstream boost mode.
            Boost mode increases the drive strength of the USB data signals (power signals
            are not changed). Boosting the data signal strength may help to overcome
            connectivity issues when using long cables or connecting through "pogo" pins.
            Possible modes are 0 - no boost, 1 - 4%% boost, 2 - 8%% boost,
            3 - 12%% boost. This setting is not applied until a stem.system.save() call
            and power cycle of the hub. Setting is then persistent until changed or the hub
            is reset. After reset, default value of 0%% boost is restored.

        Args:
            setting (int): Downstream boost setting 0, 1, 2, or 3.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbDownstreamBoostMode, setting)

    def getDownstreamBoostMode(self):
        """Get the downstream boost mode.

        Returns: Result object
            Result value 0 - no boost, 1 - 4%% boost, 2 - 8%% boost, 3 - 12%% boost.
        """
        return self.get_UEI(_BS_C.usbDownstreamBoostMode)

    def getDownstreamDataSpeed(self, channel):
        """Get the downstream port data speed.

        Returns: Result object
            Result value:
                * N/A: PORT_SPEED_NA = 0
                * Hi Speed: PORT_SPEED_HISPEED = 1
                * SuperSpeed: PORT_SPEED_SUPERSPEED = 2
        """
        return self.get_UEI_with_param(_BS_C.usbDownstreamDataSpeed, channel)

    def setConnectMode(self, channel, mode):
        """
        Set The connection mode for the Switch.

        Args:
            channel (int): Upstream port to be applied.
            mode (int): 0 = Manual mode, 1 = Auto mode.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8_with_subindex(_BS_C.usbConnectMode, channel, mode)

    def getConnectMode(self, channel):
        """
        Get The connection mode for the Switch.

        Args:
            channel (int): Upstream port to be applied.

        Returns:
            Result (object):
                value (int): The connect mode
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI_with_param(_BS_C.usbConnectMode, channel)

    def setCC1Enable(self, channel, enable):
        """Enable CC1 lines for a Type C USB port

        Args:
            channel (int): The USB port number
            enable (int): enable (0 = disable, 1 = enable)

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8_with_subindex(_BS_C.usbCC1Enable, channel, enable)

    def setCC2Enable(self, channel, enable):
        """Enable CC2 lines for a Type C USB port

        Args:
            channel (int): The USB port number
            enable (int): enable [0 = disable, 1 = enable]

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8_with_subindex(_BS_C.usbCC2Enable, channel, enable)

    def setSBUEnable(self, channel, enable):
        """Enable SBU1/SBU2 lines for a Type C USB port based on usbPortMode settings.

        Args:
            channel (int): The USB port number
            enable (int): enables SBU1/SBU2 [0 = disable, 1 = enable]

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8_with_subindex(_BS_C.usbSBUEnable, channel, enable)

    def getCC1Current(self, channel):
        """Get the current through the CC1 line for a port.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.usbCC1Current, channel))

    def getCC2Current(self, channel):
        """Get the current through the CC2 line for a port.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.usbCC2Current, channel))

    def getCC1Voltage(self, channel):
        """Get the voltage on the CC1 line for a port.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.usbCC1Voltage, channel))

    def getCC2Voltage(self, channel):
        """Get the voltage on the CC2 line for a port.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.usbCC2Voltage, channel))

    def setCableFlip(self, channel, enable):
        """Enables a cable orientation flip within the S85 switch.

        Args:
            channel (int): The USB port number
            enable (int): enables cable flip. [0 = disable, 1 = enable]

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8_with_subindex(_BS_C.usbCableFlip, channel, enable)

    def getCableFlip(self, channel):
        """Get the status of cable orientation flip within the S85 switch.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.usbCableFlip, channel))

    def setAltModeConfig(self, channel, configuration):
        """Sets alt mode configuration for defined USB channel.
            See the product datasheet for device specific details

        Args:
            channel (int): The USB channel
            configuration (uint): The configuration to set

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32_with_subindex(_BS_C.usbAltMode, channel, configuration)

    def getAltModeConfig(self, channel):
        """Gets alt mode configuration for defined USB channel.
            See the product datasheet for device specific details.

        Args:
            channel (int): The USB channel

        Returns: Result object
        """
        return self.get_UEI_with_param(_BS_C.usbAltMode, channel)

    def getSBU1Voltage(self, channel):
        """Get the voltage on the SBU1 line for a port.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.usbSBU1Voltage, channel))

    def getSBU2Voltage(self, channel):
        """Get the voltage on the SBU2 line for a port.

        Args:
            channel (int): The USB port number

        Returns: Result object
        """
        return _BS_SignCheck(self.get_UEI_with_param(_BS_C.usbSBU2Voltage, channel))


class USBSystem(Entity):
    """
        The USBSystem class provides high level control of the lower level Port Class.
    """
    def __init__(self, module, index):
        """ USBSystem entity initializer"""
        super(USBSystem, self).__init__(module, _BS_C.cmdUSBSYSTEM, index)

    def getUpstream(self):
        """ Gets the current upstream port.

        Returns:
            Result (object):
                value: Index of upstream port.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.usbsystemUpstreamPort)

    def setUpstream(self, port):
        """
        Sets the upstream port.

        Args:
            port (int): Upstream port to be applied.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbsystemUpstreamPort, port)

    def getEnumerationDelay(self):
        """
        Gets the inter-port enumeration delay in milli-seconds (mS).
        Delay is applied upon hub enumeration.

        Returns:
            Result (object):
                value (int): Current inter-port delay in milli-seconds (mS).
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.usbsystemEnumerationDelay)

    def setEnumerationDelay(self, delay):
        """
        Set the inter-port enumeration delay in milliseconds.
        This setting should be saved with a stem.system.save() call.
        Delay is applied upon hub enumeration.

        Args:
            delay (int): Delay in milli-seconds (mS) to be applied between
                port enables.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.usbsystemEnumerationDelay, delay)

    def getDataRoleList(self):
        """
        Gets the data role of all ports with a single call
        Equivalent to calling Port.getDataRole() on each individual port.

        Returns:
            Result (object):
                value (int): Bit packed representation of the data role for all ports.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.usbsystemDataRoleList)

    def getEnabledList(self):
        """
        Gets the current enabled status of all ports with a single call.
        Equivalent to calling PortClass::setEnabled() on each port.

        Returns:
            Result (object):
                value (int): Bit packed representation of the enabled status for all ports.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.usbsystemEnabledList)

    def setEnabledList(self, enabledList):
        """
        Sets the enabled status of all ports with a single call.
        Equivalent to calling PortClass::setEnabled() on each port.

        Args:
            enabledList (int): Bit packed representation of the enabled status
                for all ports to be applied.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI32(_BS_C.usbsystemEnabledList, enabledList)

    def getModeList(self):
        """
        Gets the current mode of all ports with a single call.
        Equivalent to calling PortClass:getMode() on each port.

        Returns:
            Result (object):
                value (tuple(int)): List of modes of each port.
                error: Non-zero BrainStem error code on failure.
        """
        return self.check_UEIBytes(self.get_UEIBytes(_BS_C.usbsystemModeList),4)

    def setModeList(self, modeList):
        """
        Sets the mode of all ports with a single call.
        Equivalent to calling PortClass::setMode() on each port

        Args:
            modeList (tuple(int)): List of modes to be set for each port.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return Result.UNIMPLEMENTED_ERROR

    def getStateList(self):
        """
        Gets the state for all ports with a single call.
        Equivalent to calling PortClass::getState() on each port.

        Returns:
            Result (object):
                value (tuple(int)): List of states for each port.
                error: Non-zero BrainStem error code on failure.
        """
        return self.check_UEIBytes(self.get_UEIBytes(_BS_C.usbsystemModeList),4)

    def getPowerBehavior(self):
        """
        Gets the behavior of the power manager.
        The power manager is responsible for budgeting the power of the system.
        i.e. What happens when requested power greater than  available power.

        Returns:
            Result (object):
                value (int): An enumerated representation of the current behavior.
                error: Non-zero BrainStem error code on failure.
        """
        return self.check_UEIBytes(self.get_UEIBytes(_BS_C.usbsystemPowerBehavior),4)

    def setPowerBehavior(self, behavior):
        """
        Sets the behavior of how available power is managed.
        i.e. What happens when requested power is greater than available power.

        Args:
            behavior (int): An enumerated representation of the behavior to be set.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbsystemPowerBehavior, behavior)

    def getPowerBehaviorConfig(self):
        """
        Gets the current power behavior configuration
        Certain power behaviors use a list of ports to determine priority when budgeting power.

        Returns:
            Result (object):
                value (tuple(int)): A list of ports which indicate priority sequencing.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEIBytes(_BS_C.usbsystemPowerBehaviorConfig)

    def setPowerBehaviorConfig(self, config):
        """
        Sets the current power behavior configuration
        Certain power behaviors use a list of ports to determine priority when budgeting power.

        Args:
            config (tuple(int)): List of ports which indicate priority sequencing.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return Result.UNIMPLEMENTED_ERROR

    def getDataRoleBehavior(self):
        """
        Gets the behavior of how upstream and downstream ports are determined.
        i.e. How do you manage requests for data role swaps and new upstream connections.

        Returns:
            Result (object):
                value (int): An enumerated representation of the current behavior.
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.usbsystemDataBehavior)

    def setDataRoleBehavior(self, behavior):
        """
        Sets the behavior of how upstream and downstream ports are determined.
        i.e. How do you manage requests for data role swaps and new upstream connections.

        Args:
            behavior (int): An enumerated representation of the behavior to be set.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbsystemDataBehavior, behavior)

    def getDataRoleBehaviorConfig(self):
        """
        Gets the current data role behavior configuration
        Certain data role behaviors use a list of ports to determine priority host priority.

        Returns:
            Result (object):
                value (tuple(int)): A list of ports which indicate priority sequencing.
                error: Non-zero BrainStem error code on failure.
        """
        return self.check_UEIBytes(self.get_UEIBytes(_BS_C.usbsystemDataBehaviorConfig),4)

    def setDataRoleBehaviorConfig(self, config):
        """
        Sets the current data role behavior configuration
        Certain data role behaviors use a list of ports to determine host priority.

        Args:
            config (tuple(int)): List of ports which indicate priority sequencing.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return Result.UNIMPLEMENTED_ERROR

    def getSelectorMode(self):
        """
        Gets the current mode of the selector input.
        This mode determines what happens and in what order when the external
        selector input is used.

        Returns:
            Result (object):
                value (int): The current mode
                error: Non-zero BrainStem error code on failure.
        """
        return self.get_UEI(_BS_C.usbsystemSelectorMode)

    def setSelectorMode(self, mode):
        """
        Sets the current mode of the selector input.
        This mode determines what happens and in what order when the external
        selector input is used.

        Args:
            mode (mode): Mode to be set.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.set_UEI8(_BS_C.usbsystemSelectorMode, mode)

    def resetEntityToFactoryDefaults(self):
        """
        Resets the USBSystemClass Entity to it factory default configuration.

        Returns (int):
            Non-zero BrainStem error code on failure.
        """
        return self.call_UEI(_BS_C.usbsystemResetEntityToFactoryDefaults)


# For Handling negative values.
def _BS_SignCheck(result):
        if result.error == Result.NO_ERROR:
            result._value = -0x100000000 + result.value if result.value & 0x80000000 else result.value
        return result
