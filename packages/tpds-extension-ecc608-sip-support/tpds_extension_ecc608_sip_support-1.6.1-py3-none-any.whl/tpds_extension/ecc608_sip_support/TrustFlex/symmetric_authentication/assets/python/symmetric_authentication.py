# -*- coding: utf-8 -*-
# 2018 to present - Copyright Microchip Technology Inc. and its subsidiaries.

# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.

# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR
# PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL,
# PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY
# KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP
# HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.

import os
import cryptoauthlib as cal
from pathlib import Path
from tpds.resource_generation import TFLXResources, TFLXSlotConfig
from tpds.flash_program import FlashProgram
from tpds.secure_element import ECC608A
from tpds.tp_utils.tp_settings import TPSettings
from tpds.tp_utils.tp_print import print
from tpds.tp_utils.tp_keys import TPSymmetricKey
from tpds.tp_utils.tp_utils import pretty_print_hex


class SymmetricAuthentication():
    """Authenticates a connected accessory device using Symmetric Key.
    """
    def __init__(self, boards, symm_key_slot):
        self.boards = boards
        self.shared_secret_slot = symm_key_slot
        self.mac_mode = 0x41

    def __connect_to_SE(self, b=None):
        print('Connecting to Secure Element: ', canvas=b)
        if self.boards is None:
            print('Prototyping board MUST be selected!', canvas=b)
            return
        assert self.boards.get_selected_board(), \
            'Select board to run an Usecase'

        kit_parser = FlashProgram(board_name='EV76R77A')
        print(kit_parser.check_board_status())
        assert kit_parser.is_board_connected(), \
            'Check the Kit parser board connections'
        factory_hex = self.boards.get_kit_hex()
        if not kit_parser.is_factory_programmed():
            assert factory_hex, \
                'Factory hex is unavailable to program'
            print('Programming factory hex...', canvas=b)
            tp_settings = TPSettings()
            path = os.path.join(
                tp_settings.get_tpds_core_path(),
                'assets', 'Factory_Program.X',
                factory_hex)
            print(f'Programming {path} file')
            kit_parser.load_hex_image_with_ipe(path)
        self.element = ECC608A(address=0xC0)
        print('OK', canvas=b)
        print('Device details: {}'.format(self.element.get_device_details()))
        self.ser_num = self.element.get_device_serial_number().hex().upper()

    def generate_resources(self, b=None):
        self.__connect_to_SE(b)

        print('Generating crypto assets for Usecase...', canvas=b)
        resources = TFLXResources()
        tflex_slot_config = TFLXSlotConfig().tflex_slot_config

        symm_slot = self.shared_secret_slot
        symm_key_slot_config = tflex_slot_config.get(symm_slot)
        assert symm_key_slot_config.get('type') == 'secret', \
            "Invalid Slot, It is expected to be secret"

        enc_slot = symm_key_slot_config.get('enc_key', None)
        enc_key = Path('slot_{}_secret_key.pem'.format(
                enc_slot)) if enc_slot else None

        # Load encrypted Key
        if enc_key is not None:
            secret_key = Path('slot_{}_secret_key.pem'.format(enc_slot))
            assert resources.load_secret_key(
                    enc_slot, enc_key, None,
                    None) == cal.Status.ATCA_SUCCESS, \
                "Loading encrypted key into slot{} failed".format(enc_slot)

        # Load symmetric Key
        secret_key = Path('slot_{}_secret_key.pem'.format(symm_slot))
        assert resources.load_secret_key(
                symm_slot, secret_key, enc_slot,
                enc_key) == cal.Status.ATCA_SUCCESS, \
            "Loading secret key into slot{} failed".format(symm_slot)
        print('OK', canvas=b)

    def initiate_accessory_auth(self, b=None):
        print('Generating challenge input value...', canvas=b)
        self.num_in = os.urandom(20)
        print("Nonce Input value:")
        print(pretty_print_hex(self.num_in, li=10, indent=''))
        print('OK', canvas=b)

    def get_mac_from_accessory_device(self, b=None):
        print('Getting MAC from accesory device...', canvas=b)
        self.rand_out = self.element.get_device_random_nonce(self.num_in)
        self.device_mac = self.element.get_device_mac_response(
                                            self.shared_secret_slot,
                                            0,
                                            self.mac_mode)
        print("MAC Received from Accessory device:")
        print(pretty_print_hex(self.device_mac, indent=''))
        print('OK', canvas=b)

    def compare_host_mac_with_accessory_mac(self, b=None):
        print('In real application, accessory SE MAC has to be verified on',
              canvas=b)
        print('host SE (attached on MCU) by issuing checkmac command.',
              canvas=b)
        print('But in this demo, accessory MAC is verified by Host PC',
              canvas=b)
        self.calculate_mac_on_host(b)

        if self.host_mac == self.device_mac:
            print('Accessory device authenticated successfully!', canvas=b)
        else:
            print('Accessory device not authenticated...', canvas=b)

    def calculate_mac_on_host(self, b=None):
        print('Calculating MAC on Host PC...', canvas=b)
        host = self.element.host_calc_nonce(
                                            self.num_in,
                                            self.rand_out['rand_out'])
        symm_key = TPSymmetricKey(
            key='slot_{}_secret_key.pem'.format(
                                            self.shared_secret_slot))
        resp = self.element.host_calc_mac_resp(
                                            symm_key.key_bytes,
                                            host['nonce'],
                                            self.mac_mode,
                                            self.shared_secret_slot)
        self.host_mac = resp['response']
        print('MAC calculated on host device:')
        print(pretty_print_hex(self.host_mac, indent=''))
        print('OK', canvas=b)
