#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""c2pcontrol - remote control of the CRONUS-2P optical parametric oscillator.

Copyright 2020-2023 Light Conversion
Contact: support@lightcon.com
"""
import json
from urllib.error import URLError
from ..common._http_methods import HTTP_methods
from ..common._logging import init_logger


class C2PControl(HTTP_methods):
    """REST API interaction with CRONUS-2P REST Server."""

    silent = True
    connected = False
    logger = None
    type = 'cronus2p'

    def __init__(self, ip_address='127.0.0.1', port=35100, version='v0'):
        self.logger = init_logger('c2p', 'cronus_2p.log')

        self.url = 'http://{}:{}/{}/Cronus/'.format(
            ip_address, port, version)
        self.logger.info("Connecting to CRONUS-2P at {:s}:{:d}".format(
            ip_address, port))

        status = self.get_status()

        if status and status.get('OK'):
            self.connected = True
            self.logger.info("Connection to CRONUS-2P established "
                             "at {}".format(self.url))

    def __del__(self):
        self.logger.info("Stopping remote control")

    def get_status(self):
        try:
            return self._get('Status')
        except URLError as excp:
            self.logger.error("Could not reach CRONUS-2P")
        except Exception as excp:
            self.logger.error("An unknown error has occurred. "
                              "Exception: {}".format(excp))

    def set_mode_run(self):
        self._put("ModeRun", '')

    def get_mode(self):
        return self._get("Mode")

    def get_pump_power(self):
        return float(self._get("PumpPower").get("Power"))*1E-3

    def _check_channel(self, channel=None):
        if channel is None:
            print("No channel specified")
            return False

        if channel < 1 or channel > 3:
            print("Channel must be 1 – 3")
            return False

        return True

    def _check_wavelength(self, channel=None, wavelength=None):
        rng = self.get_wavelength_range(channel)
        if wavelength < rng[0] or wavelength > rng[1]:
            print("Wavelenngth {:.1f} nm is out of range for Channel {:d} "
                  "({:.1f} - {:.1f})".format(
                        wavelength, channel, rng[0], rng[1]))
            return False
        return True

    def _check_gdd(self, channel=None, gdd=None):
        rng = self.get_current_gdd_range(channel)
        if gdd < rng[0] or gdd > rng[1]:
            print("GDD {:.1f} fs2 is out of range for Channel {:d} "
                  "({:.1f} - {:.1f})".format(gdd, channel, rng[0], rng[1]))
            return False
        return True

    def open_shutter(self, channel=None):
        if not self._check_channel(channel):
            return
        self._put("Ch{:d}".format(channel) + "/ShutterOpen", '')

    def close_shutter(self, channel=None):
        if not self._check_channel(channel):
            return
        self._put("Ch{:d}".format(channel) + "/ShutterClosed", '')

    def get_wavelength(self, channel=None):
        if not self._check_channel(channel):
            return
        return float(self._get("Ch{:d}".format(channel) + "/Wavelength").get(
            "Wavelength"))

    def set_wavelength(self, channel=None, wavelength=None, verbose=True):
        if not self._check_channel(channel):
            return
        if not self._check_wavelength(channel, wavelength):
            return
        self._put("Ch{:d}".format(channel) + "/Wavelength",
                  json.dumps({'Wavelength': wavelength}))

    def get_wavelength_range(self, channel=None):
        if not self._check_channel(channel):
            return
        response = self._get("Ch{:d}".format(channel) + "/WavelengthRange")
        return [float(response.get('Min')), float(response.get('Max'))]

    def get_gdd(self, channel=None):
        if not self._check_channel(channel):
            return
        response = self._get("Ch{:d}".format(channel) + "/GDD")
        return float(response.get('GDD'))

    def set_gdd(self, channel=None, gdd=None):
        if not self._check_channel(channel):
            return
        if not self._check_gdd(channel, gdd):
            return
        self._put("Ch{:d}".format(channel) + "/GDD", json.dumps({'GDD': gdd}))

    def get_current_gdd_range(self, channel=None):
        if not self._check_channel(channel):
            return
        response = self._get("Ch{:d}".format(channel) + "/CurrentGDDRange")
        return [float(response.get('Min')), float(response.get('Max'))]

    def get_gdd_range(self, channel=None, wavelength=None):
        if not self._check_channel(channel):
            return
        if not self._check_wavelength(channel, wavelength):
            return
        response = self._report("Ch{:d}".format(channel) + "/GDDRange",
                                json.dumps({'Wavelength': wavelength}))
        return [float(response.get('Min')), float(response.get('Max'))]
