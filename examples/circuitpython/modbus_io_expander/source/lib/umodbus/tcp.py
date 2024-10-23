#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

# system packages
# import random
import board
import busio
import digitalio
import struct
import time

# custom packages
from . import functions
from . import const as Const
from .common import Request, CommonModbusFunctions
from .common import ModbusException
from .modbus import Modbus

# typing not natively supported on MicroPython
from .typing import Optional, Tuple, Union


class ModbusTCP(Modbus):
    """Modbus TCP Server class"""
    def __init__(self, socketpool, addr_list):
        super().__init__(
            # set itf to TCPServer object, addr_list to None
            TCPServer(socketpool),
            addr_list
        )

    def bind(self,
             local_ip: str = None,
             local_port: int = 502,
             max_connections: int = 10) -> None:
        """
        Bind IP and port for incomming requests

        :param      local_ip:         IP of this device listening for requests
        :type       local_ip:         str
        :param      local_port:       Port of this device
        :type       local_port:       int
        :param      max_connections:  Number of maximum connections
        :type       max_connections:  int
        """
        self._itf.bind(local_ip, local_port, max_connections)

    def get_bound_status(self) -> bool:
        """
        Get the IP and port binding status.

        :returns:   The bound status, True if already bound, False otherwise.
        :rtype:     bool
        """
        try:
            return self._itf.get_is_bound()
        except Exception:
            return False


class TCP(CommonModbusFunctions):
    """
    TCP Client class handling socket connections and parsing the Modbus data

    :param      slave_ip:    IP of this device listening for requests
    :type       slave_ip:    str
    :param      slave_port:  Port of this device
    :type       slave_port:  int
    :param      timeout:     Socket timeout in seconds
    :type       timeout:     float
    """
    def __init__(self,
                 sock,
                 slave_ip: str,
                 slave_port: int = 502,
                 timeout: float = 5.0):
        
        self._sock = sock
        self.trans_id_ctr = 0

        # print(socket.getaddrinfo(slave_ip, slave_port))
        # [(2, 1, 0, '192.168.178.47', ('192.168.178.47', 502))]
        self._sock.connect(socket.getaddrinfo(slave_ip, slave_port)[0][-1])

        self._sock.settimeout(timeout)

    def _create_mbap_hdr(self,
                         slave_addr: int,
                         modbus_pdu: bytes) -> Tuple[bytes, int]:
        """
        Create a Modbus header.

        :param      slave_addr:  The slave identifier
        :type       slave_addr:  int
        :param      modbus_pdu:  The modbus Protocol Data Unit
        :type       modbus_pdu:  bytes

        :returns:   Modbus header and unique transaction ID
        :rtype:     Tuple[bytes, int]
        """
        # only available on WiPy
        # trans_id = machine.rng() & 0xFFFF
        # use builtin function to generate random 24 bit integer
        # trans_id = random.getrandbits(24) & 0xFFFF
        # use incrementing counter as it's faster
        trans_id = self.trans_id_ctr
        self.trans_id_ctr += 1

        mbap_hdr = struct.pack(
            '>HHHB', trans_id, 0, len(modbus_pdu) + 1, slave_addr)

        return mbap_hdr, trans_id

    def _validate_resp_hdr(self,
                           response: bytearray,
                           trans_id: int,
                           slave_addr: int,
                           function_code: int,
                           count: bool = False) -> bytes:
        """
        Validate the response header.

        :param      response:       The response
        :type       response:       bytearray
        :param      trans_id:       The transaction identifier
        :type       trans_id:       int
        :param      slave_addr:     The slave identifier
        :type       slave_addr:     int
        :param      function_code:  The function code
        :type       function_code:  int
        :param      count:          The count
        :type       count:          bool

        :returns:   Modbus response content
        :rtype:     bytes
        """
        rec_tid, rec_pid, rec_len, rec_uid, rec_fc = struct.unpack(
            '>HHHBB', response[:Const.MBAP_HDR_LENGTH + 1])

        if (trans_id != rec_tid):
            raise ValueError('wrong transaction ID')

        if (rec_pid != 0):
            raise ValueError('invalid protocol ID')

        if (slave_addr != rec_uid):
            raise ValueError('wrong slave ID')

        if (rec_fc == (function_code + Const.ERROR_BIAS)):
            raise ValueError('slave returned exception code: {:d}'.
                             format(rec_fc))

        hdr_length = (Const.MBAP_HDR_LENGTH + 2) if count else \
            (Const.MBAP_HDR_LENGTH + 1)

        return response[hdr_length:]

    def _send_receive(self,
                      slave_addr: int,
                      modbus_pdu: bytes,
                      count: bool) -> bytes:
        """
        Send a modbus message and receive the reponse.

        :param      slave_addr:    The slave identifier
        :type       slave_addr:    int
        :param      modbus_pdu:  The modbus PDU
        :type       modbus_pdu:  bytes
        :param      count:       The count
        :type       count:       bool

        :returns:   Modbus data
        :rtype:     bytes
        """
        mbap_hdr, trans_id = self._create_mbap_hdr(slave_addr=slave_addr,
                                                   modbus_pdu=modbus_pdu)
        self._sock.send(mbap_hdr + modbus_pdu)

        response = self._sock.recv(256)
        modbus_data = self._validate_resp_hdr(response=response,
                                              trans_id=trans_id,
                                              slave_addr=slave_addr,
                                              function_code=modbus_pdu[0],
                                              count=count)

        return modbus_data


class TCPServer(object):
    """TCP Server class"""
    def __init__(self, sockpool):
        self._sockpool = sockpool
        self._socklist = list()
        self._socknum = 0
        self._current_sock = None
        self._local_ip = None
        self._local_port = 502
        self._is_bound = False
        self._link_timestamp = 0

    @property
    def is_bound(self) -> bool:
        """
        Get the IP and port binding status

        :returns:   True if bound to IP and port, False otherwise
        :rtype:     bool
        """
        return self._is_bound

    def get_is_bound(self) -> bool:
        """
        Get the IP and port binding status, legacy support.

        :returns:   True if bound to IP and port, False otherwise
        :rtype:     bool
        """
        return self._is_bound

    def bind(self,
             local_ip: str = None,
             local_port: int = 502,
             max_connections: int = 5):
        """
        Bind IP and port for incomming requests

        :param      local_ip:         IP of this device listening for requests
        :type       local_ip:         str
        :param      local_port:       Port of this device
        :type       local_port:       int
        :param      max_connections:  Number of maximum connections (Not used)
        :type       max_connections:  int
        """
        
        # Clear the socket list.
        for s in self._socklist:
            if s:
                s.close()
        self._socklist.clear()
        self._current_sock = None
        
        if max_connections < 1:
            return
        
        self._local_ip = local_ip
        self._local_port = local_port
        
        for i in range(max_connections):
            # Create a new socket, bind it and start listening.
            sock = self._sockpool.socket()
            sock.bind((self._local_ip, self._local_port))
            sock.listen()
            
            # Add the socket to socket list.
            self._socklist.append(sock)
        
        self._socknum = 0
        self._is_bound = True

    def _send(self, modbus_pdu: bytes, slave_addr: int) -> None:
        """
        Send Modbus Protocol Data Unit to slave

        :param      modbus_pdu:  The Modbus Protocol Data Unit
        :type       modbus_pdu:  bytes
        :param      slave_addr:  The slave address
        :type       slave_addr:  int
        """
        size = len(modbus_pdu)
        fmt = 'B' * size
        adu = struct.pack('>HHHB' + fmt, self._req_tid, 0, size + 1, slave_addr, *modbus_pdu)
        self._current_sock.send(adu)

    def send_response(self,
                      slave_addr: int,
                      function_code: int,
                      request_register_addr: int,
                      request_register_qty: int,
                      request_data: list,
                      values: Optional[list] = None,
                      signed: bool = True) -> None:
        """
        Send a response to a client.

        :param      slave_addr:             The slave address
        :type       slave_addr:             int
        :param      function_code:          The function code
        :type       function_code:          int
        :param      request_register_addr:  The request register address
        :type       request_register_addr:  int
        :param      request_register_qty:   The request register qty
        :type       request_register_qty:   int
        :param      request_data:           The request data
        :type       request_data:           list
        :param      values:                 The values
        :type       values:                 Optional[list]
        :param      signed:                 Indicates if signed
        :type       signed:                 bool
        """
        modbus_pdu = functions.response(function_code,
                                        request_register_addr,
                                        request_register_qty,
                                        request_data,
                                        values,
                                        signed)
        self._send(modbus_pdu, slave_addr)

    def send_exception_response(self,
                                slave_addr: int,
                                function_code: int,
                                exception_code: int) -> None:
        """
        Send an exception response to a client.

        :param      slave_addr:      The slave address
        :type       slave_addr:      int
        :param      function_code:   The function code
        :type       function_code:   int
        :param      exception_code:  The exception code
        :type       exception_code:  int
        """
        modbus_pdu = functions.exception_response(function_code,
                                                  exception_code)
        self._send(modbus_pdu, slave_addr)
        

    def get_request(self,
                    unit_addr_list: Optional[list] = None,
                    timeout: int = 0) -> Union[Request, None]:
        """
        Check for request within the specified timeout

        :param      unit_addr_list:  The unit address list
        :type       unit_addr_list:  Optional[list]
        :param      timeout:         The timeout
        :type       timeout:         int

        :returns:   A request object or None.
        :rtype:     Union[Request, None]

        :raises     Exception:       If no socket is configured and bound
        """
        self._current_sock = self._socklist[self._socknum]
        
        # Increase the socket number for next call.
        current_socknum = self._socknum
        self._socknum += 1
        if self._socknum >= len(self._socklist):
            self._socknum = 0
        
        if self._current_sock is None:
            raise Exception('Modbus TCP server not bound')
        
        
        
        # If link is down for >= 5 seconds, reset the socket.
        if not self._sockpool._interface.link_status:
            if time.monotonic() - self._link_timestamp >= 5:
                if not self._current_sock._socket_closed:
                    self._current_sock.close()
            return None
        
        # Record the timestamp.
        self._link_timestamp = time.monotonic()
        
        # Check if the socket is closed.
        # There is a bug in the socket library where the is_closed flag is not updated.
        # The workaround is to call the _connected to update the flag and close the socket if it's disconnected by client.
        try:
            is_connected = self._current_sock._connected
            is_closed = self._current_sock._socket_closed
        except Exception:
            is_connected = False
            is_closed = True
            
        if not is_connected:
            if is_closed:
                # Previous client is disconnected and socket is closed.
                # Create a new socket, bind it and start listening.
                self._current_sock = self._sockpool.socket()
                self._current_sock.bind((self._local_ip, self._local_port))
                self._current_sock.listen()
                
                # Replace the old one in socket list.
                self._socklist[current_socknum] = self._current_sock
            
            return None
        
        
        # Read the received data.
        try:
            self._current_sock.settimeout(timeout)
            req = self._current_sock.recv(260)
            
            if len(req) == 0:
                return None
            
            req_header_no_uid = req[:Const.MBAP_HDR_LENGTH - 1]
            self._req_tid, req_pid, req_len = struct.unpack('>HHH', req_header_no_uid)
            req_uid_and_pdu = req[Const.MBAP_HDR_LENGTH - 1:Const.MBAP_HDR_LENGTH + req_len - 1]
        except OSError as e:
            # MicroPython raises an OSError instead of socket.timeout
            # print("Socket OSError aka TimeoutError: {}".format(e))
            return None
        except Exception:
            # print("Modbus request error:", e)
            return None

        if (req_pid != 0):
            # print("Modbus request error: PID not 0")
            return None

        if ((unit_addr_list is not None) and (req_uid_and_pdu[0] not in unit_addr_list)):
            return None

        try:
            return Request(self, req_uid_and_pdu)
        except ModbusException as e:
            self.send_exception_response(req[0], e.function_code, e.exception_code)
            return None
