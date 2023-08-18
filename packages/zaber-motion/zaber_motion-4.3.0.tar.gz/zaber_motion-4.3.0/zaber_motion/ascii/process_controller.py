# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import List
from ..call import call, call_sync, call_async

from ..protobufs import main_pb2
from .device import Device
from .process import Process
from .connection import Connection


class ProcessController:
    """
    Use to manage a process controller.
    WARNING: DO NOT USE. This API is for an as-yet unreleased product and firmware version.
    It is subject to breaking changes without warning until further notice.
    Requires at least Firmware 7.34.
    """

    @property
    def device(self) -> Device:
        """
        The base device of this process controller.
        """
        return self._device

    def __init__(self, device: Device):
        """
        Creates instance of `ProcessController` of the given device.
        If the device is identified, this constructor will ensure it is a process controller.
        """
        self._device = device
        self.__verify_is_process_controller()

    @staticmethod
    def detect(
            connection: Connection,
            identify: bool = True
    ) -> List['ProcessController']:
        """
        Detects the process controllers on the connection.

        Args:
            connection: The connection to detect process controllers on.
            identify: If the Process Controllers should be identified upon detection.

        Returns:
            A list of all `ProcessController`s on the connection.
        """
        request = main_pb2.DeviceDetectRequest()
        request.type = main_pb2.DeviceDetectRequest.PROCESS_CONTROLLER
        request.interface_id = connection.interface_id
        request.identify_devices = identify
        response = main_pb2.DeviceDetectResponse()
        call("device/detect", request, response)
        return [ProcessController(connection.get_device(device)) for device in response.devices]

    @staticmethod
    async def detect_async(
            connection: Connection,
            identify: bool = True
    ) -> List['ProcessController']:
        """
        Detects the process controllers on the connection.

        Args:
            connection: The connection to detect process controllers on.
            identify: If the Process Controllers should be identified upon detection.

        Returns:
            A list of all `ProcessController`s on the connection.
        """
        request = main_pb2.DeviceDetectRequest()
        request.type = main_pb2.DeviceDetectRequest.PROCESS_CONTROLLER
        request.interface_id = connection.interface_id
        request.identify_devices = identify
        response = main_pb2.DeviceDetectResponse()
        await call_async("device/detect", request, response)
        return [ProcessController(connection.get_device(device)) for device in response.devices]

    def get_process(
            self,
            process_number: int
    ) -> Process:
        """
        Gets an Process class instance which allows you to control a particular voltage source.
        Axes are numbered from 1.

        Args:
            process_number: Number of process to control.

        Returns:
            Process instance.
        """
        if process_number <= 0:
            raise ValueError('Invalid value; processes are numbered from 1.')

        return Process(self, process_number)

    def __verify_is_process_controller(
            self
    ) -> None:
        """
        Checks if this is a process controller or some other type of device and throws a detect error if it is not.
        """
        request = main_pb2.DeviceEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        call_sync("process_controller/verify", request)
