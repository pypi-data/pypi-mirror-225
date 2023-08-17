#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""c3pcontrol - remote control of the CRONUS-3P optical parametric amplifier.

Copyright 2020-2023 Light Conversion
Contact: support@lightcon.com
"""
import json
import time
import datetime
from enum import IntEnum
import numpy as np
from ..common._http_methods import HTTP_methods
from ..common._logging import init_logger


class C3PState(IntEnum):
    UnknownState = -3
    Fail = -2
    SoftFail = -1
    Idle = 0
    Preparation = 1
    MovingMotorsToInitialPosition = 2
    AdjustingOutputBeam = 3
    Success = 4


class C3PControl(HTTP_methods):
    """CRONUS-3P remote control interface class."""
    silent = True
    verbose = False
    connected = False
    logger = None
    type = 'cronus-3p'
    has_gdd_control = True

    def __init__(
            self, ip_address, port=35120, dev_sn=None, version='v0'):
        """Initialization."""
        self.logger = init_logger('c3p', 'cronus_3p.log')
        self.url = 'http://{}:{}/{}/{}/'.format(ip_address, port, dev_sn,
                                                version)
        self.logger.info("Connecting to CRONUS-3P device "
                         "SN {:s} at {:s}:{:d}".format(
                            dev_sn, ip_address, port))
        try:
            self.connected = self._open('Help/API').find('Beam') != -1
        except Exception as excpt:
            self.logger.error(
                "Could not connect to CRONUS-3P. Make sure the IP address, "
                "the REST port and the device SN are correct, the host is "
                "reachable, and that the LightComposer app is running with "
                "admin privileges. Exception reason: ", excpt)
            raise Exception("Cannot connect to CRONUS-3P")
        if self.connected:
            self.logger.info("CRONUS-3P control at {:} established".format(
                self.url))

    def __del__(self):
        self.logger.info("Stopping remote control")

    # === Status ===

    def get_status(self):
        """Get laser system status."""
        return self._get('Main/Status')

    def get_pump_laser_status(self):
        """Get pump laser satus."""
        return self._get('PumpLaser/Status')

    def get_info(self):
        """Get laser info."""
        return self._get('Main/Info')

    def wavelength_setting_state_str_to_enum(self, state_str):
        """Convert wavelength setting state string to enum."""
        c3p_state_strings = [
            'UnknownState', 'Fail', 'SoftFail',
            'Idle', 'Preparation', 'MovingMotorsToInitialPosition',
            'AdjustingOutputBeam', 'Success']

        if state_str not in c3p_state_strings:
            print("Unrecognized state string '{:s}'".format(state_str))
            return C3PState.UnknownState
        else:
            return C3PState(c3p_state_strings.index(state_str) - 3)

    def get_wavelength_setting_state(self):
        """Get wavelength setting state."""
        return self.wavelength_setting_state_str_to_enum(
            self.get_status()['WavelengthSettingState'])

    def print_status(self):
        """Print status."""
        status = self.get_status()

        print('Wavelength: {:.0f} nm'.format(status['Wavelength']))
        print('GDD: {:.0f} fs^2'.format(status['GDD']))

        print('Wavelength set result: ' + status['WavelengthSettingState'])

        print('Shutter: ' + 'Open' if status['IsPrimaryShutterOpen'] else
              'False')

        print('Beam tracking:')
        beam_tr = status['BeamPositions'][0]
        print('\tNear: power={:.3f}, x={:.3f}, y={:.3f}'.format(
            beam_tr['Intensity'], beam_tr['X'], beam_tr['Y']))
        beam_tr = status['BeamPositions'][1]
        print('\tFar : power={:.3f}, x={:.3f}, y={:.3f}'.format(
            beam_tr['Intensity'], beam_tr['X'], beam_tr['Y']))

    # === Wavelength ===

    def get_wavelength(self):
        """Get wavelength in nm."""
        return self._get('Main/Status')['Wavelength']

    def set_wavelength(self, wavl, retry=True, num_retries=3, **kwargs):
        """Set wavelength in nm."""
        for attempt_ind in range(num_retries):
            try:
                return self._set_wavelength(wavl, **kwargs)
            except Exception as excpt:
                print("Could not set wavelength. Reason: ", excpt)
                if retry:
                    print("Trying again, attempt {:d}/{:d}".format(
                        attempt_ind, num_retries))
                if attempt_ind == num_retries:
                    print("Could not set wavelength after multiple retries")
                    raise excpt

    def _set_wavelength(
            self, wavl, gdd=None, skip_if_set=True, wait_until_done=False,
            with_beam_tracking=False, open_shutters=False, verbose=None):
        """Set wavelength with optional beam tracking."""
        if verbose is None:
            verbose = self.verbose

        if open_shutters:
            if verbose:
                print('Opening shutters...')
            self.open_all_shutters()

        old_wavl = self.get_wavelength()

        if self.has_gdd_control and gdd is not None:
            old_gdd = self.get_gdd()

        if skip_if_set and np.abs((old_wavl - wavl)) < 1:
            if not self.has_gdd_control or gdd is None:
                print("Wavelength already set")
                return
            elif np.abs((old_gdd - gdd)) < 100:
                print("Wavelength and GDD already set")
                return

        if verbose:
            if self.has_gdd_control and gdd is not None:
                print("Setting wavelength to {:.0f} nm and GDD "
                      "to {:.0f} fs2...".format(wavl, gdd),
                      end='', flush=True)
            else:
                print("Setting wavelength to {:.0f} nm...".format(wavl),
                      end='', flush=True)

        timestamp = datetime.datetime.now()
        timestamp_str = timestamp.strftime('%Y-%m-%d_%H%M%S')

        gdd_setting_enabled = False
        skip_gdd_setting_outside_range = True
        if self.has_gdd_control and gdd is not None:
            if wavl < 1250 or wavl > 1800:
                gdd_setting_enabled = False
            else:
                gdd_range = self.get_gdd_range()
                if gdd >= gdd_range[0] and gdd <= gdd_range[1]:
                    gdd_setting_enabled = True
                elif skip_gdd_setting_outside_range:
                    gdd_setting_enabled = True
                    print("Requested GDD is outside available range, setting "
                          "wavelength only")
                else:
                    gdd_setting_enabled = False

        if gdd_setting_enabled:
            self._put('Main/WavelengthAndGDD', json.dumps(
                {'Wavelength': float(wavl), 'GDD': float(gdd)}))
        else:
            self._put('Main/Wavelength', json.dumps(
                {'Wavelength': float(wavl)}))

        if wait_until_done:
            time.sleep(0.05)
            set_state = self.get_wavelength_setting_state()
            while set_state not in [C3PState.Success, C3PState.Fail]:
                if False:
                    print("Set state: " + set_state)
                time.sleep(0.05)
                set_state = self.get_wavelength_setting_state()
            if verbose:
                if set_state == C3PState.Success and \
                        self.get_wavelength() == wavl:
                    print('OK')
                elif set_state == C3PState.Fail:
                    raise RuntimeError("Failed to set wavelength with 'Fail' "
                                       "state")
                else:
                    print('Unspecified problem occurred')
        elif verbose:
            print('\n')

    def wait_until_wavelength_set(self):
        """Wait until wavelength setting procedure is completed."""
        while self.get_wavelength_setting_state() != 'Success':
            time.sleep(0.05)

    # === GDD ===

    def get_gdd(self):
        """Get GDD in fs^2."""
        # return self._get('GDD')['GDD']
        return self._get('Main/Status').get('GDD')

    def set_gdd(
            self, gdd, skip_if_set=True, wait_until_done=False,
            open_shutters=False, verbose=None):
        """Set GDD."""
        if verbose is None:
            verbose = self.verbose

        if not self.has_gdd_control:
            return False

        if open_shutters:
            if verbose:
                print('Opening shutters...')
            self.open_all_shutters()

        old_gdd = self.get_gdd()

        if skip_if_set and np.abs((old_gdd - gdd)) < 10:
            print("GDD already set")
            return True

        if verbose:
            print("Setting GDD to {:.0f} fs^2...".format(gdd), end='',
                  flush=True)

        timestamp = datetime.datetime.now()
        timestamp_str = timestamp.strftime('%Y-%m-%d_%H%M%S')

        # self._put('GDD', json.dumps({'GDD': float(gdd)}))
        self._put('Main/GDD', json.dumps({'GDD': float(gdd)}))

        if wait_until_done:
            time.sleep(0.05)
            set_state = self.get_wavelength_setting_state()
            while set_state not in [C3PState.Success, C3PState.Fail]:
                if False:
                    print("Set state: " + set_state)
                time.sleep(0.05)
                set_state = self.get_wavelength_setting_state()
            if verbose:
                if set_state == C3PState.Success and self.get_gdd() == gdd:
                    print('OK')
                elif set_state == C3PState.Fail:
                    # Hacky retry
                    print("Failed to set GDD, retrying with a wait...")
                    self._put('Main/GDD', json.dumps({'GDD': float(gdd)}))
                    time.sleep(3)
                    set_state = self.get_wavelength_setting_state()
                    if set_state == C3PState.Success:
                        print("OK")
                        return True
                    print("Failed")
                    return False
                else:
                    print('Unspecified problem occurred')
                    return False
        elif verbose:
            print('\n')
        return True

    def get_gdd_range(self, wavl=None):
        """Get GDD range in fs^2."""
        if wavl is None:
            response = self._get('Main/CurrentGDDRange')
            return [response.get('Min'), response.get('Max')]
        else:
            response = self._post('Main/GDDRange', {'Interaction': 'IDL',
                                                    'Wavelength': float(wavl)})
            return [response.get('Min'), response.get('Max')]

    # === Beam steering ===

    def has_beam_steering(self):
        """Check whether laser system has beam steering."""
        return self.get_info().get('HasOutputBeamStabilization', False)

    def is_beam_steering_active(self):
        """Check whether beam steering is active."""
        return self.get_status()['IsBeamSteeringActive']

    def get_beam_steering_pos(self):
        """Get the position of beam steering motors."""
        return self.get_status().get('BeamMirrorActualPositions')

    def get_beam_position(self):
        """Get beam position."""
        return self.get_status().get('BeamPositions')

    def get_beam_position_total(self):
        """Get beam position total signal."""
        status = self.get_status()
        qd1_ampl = status['BeamPositions'][0]['Intensity']
        qd2_ampl = status['BeamPositions'][1]['Intensity']

        return [qd1_ampl, qd2_ampl]

    def set_beam_pos(self, mirror_id=1, xpos=0, ypos=0, wait_until_done=False,
                     extra_wait_time=0.05):
        """Move beam steering mirror."""
        self._put('Beam/MoveBeam/{:d}'.format(mirror_id), json.dumps(
                  {'X': float(xpos), 'Y': float(ypos)}))

        if wait_until_done:
            print("Waiting for mirror to move...", end='', flush=True)
            t_start = time.time()
            while True:
                if time.time() - t_start > 5:
                    print("Problem\nMove taking longer than 5 s, reissuing "
                          "move command...")
                    self._put('Beam/MoveBeam/{:d}'.format(mirror_id),
                              json.dumps({'X': float(xpos), 'Y': float(ypos)}))
                    t_start = time.time()

                pos = self.get_beam_steering_pos()[mirror_id-1]
                if np.abs((pos['X'] - xpos)) < 0.01 \
                        and np.abs((pos['Y'] - ypos)) < 0.01:
                    break
                time.sleep(extra_wait_time)
            print('OK')

    def center_beam(self, wait_until_done=True):
        """Activate beam steering procedure to center the beam."""
        if wait_until_done:
            logger.info("Initiating beam steering...")
        else:
            logger.info("Beam steering initiated (no wait)")

        self._put('CenterBeam', '')

        if wait_until_done:
            while not self.is_beam_steering_active():
                time.sleep(0.01)

            while self.is_beam_steering_active():
                time.sleep(0.01)

            logger.info("Beam steering completed")

    # === Shutters

    def is_outputy_shutter_open(self):
        return self.get_status()['IsPrimaryShutterOpen']

    def open_all_shutters(self, wait_to_stabilize=True, verbose=None,
                          max_wait=3):
        """Open all shutters."""
        if verbose is None:
            verbose = self.verbose

        if verbose:
            print("Opening shutters...")

        ret_val = self._put('Main/OpenShutters', '')
        t_start = time.time()

        time.sleep(1)

        while not self.get_status()['Shutters']['IsShutterOpen']:
            if time.time() - t_start > max_wait:
                raise RuntimeError("Could not open shutters in the allocated "
                                   "maximum time ({:d} seconds)".format(
                                       max_wait))
            time.sleep(0.1)

        if wait_to_stabilize:
            if verbose:
                print("Waiting for system to stabilize")
            time.sleep(2)

        return ret_val

    def close_all_shutters(self, wait_to_stabilize=False, verbose=None):
        """Close all shutters."""
        if verbose is None:
            verbose = self.verbose

        if verbose:
            print("Closing shutters...")

        ret_val = self._put('Main/CloseShutters', '')

        if wait_to_stabilize:
            if verbose:
                print("Waiting for system to stabilize")
            time.sleep(2)

        return ret_val
