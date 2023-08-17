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

from tpds.pubkey_validation import DevicePubkeyValidation
from tpds.resource_generation import TFLXResources, TFLXSlotConfig
from tpds.flash_program import FlashProgram
from tpds.secure_element import ECC608A
from tpds.tp_utils.tp_settings import TPSettings
from tpds.tp_utils.tp_print import print
from tpds.tp_utils.tp_keys import TPAsymmetricKey
from tpds.tp_utils.tp_utils import sign_on_host


class PubKeyRotation():
    """Rotates a Public Key securely.
    """
    def __init__(
                self, boards, auth_key_slot, rotating_key_slot):
        """Constructs required attributes

        Args:
            auth_key_slot (int): Slot number that holds Authority Key pair.
            rotating_key_slot (int): Slot number that holds Rotating Public Key pair.
        """
        self.auth_key_slot = auth_key_slot
        self.rotating_key_slot = rotating_key_slot
        self.boards = boards

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
        """Method generates required resources to run this usecase.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        self.__connect_to_SE(b)

        print('Generating crypto assets for Usecase...', canvas=b)
        resources = TFLXResources()
        slot_config = TFLXSlotConfig().tflex_slot_config
        pubkey_rotation_slots = [self.auth_key_slot, self.rotating_key_slot]
        pub_rotation_slots = {
            key: slot_config[key] for key in slot_config.keys()
            & pubkey_rotation_slots}

        for slot, tflex_slot_config in pub_rotation_slots.items():
            if tflex_slot_config.get('type') == 'public':
                if 'pubinvalid' in tflex_slot_config:
                    resources.process_pubinvalid_slot(tflex_slot_config.get(
                        'auth_key'), slot)
                    pass
                else:
                    assert resources.load_public_key(
                        slot) == cal.Status.ATCA_SUCCESS, \
                        "Loading public key into slot{} failed"\
                        .format(slot)
        print('OK', canvas=b)

    def generate_new_public_key(self, b=None):
        """Generate a new public key that is to be rotated with.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        print('Generate new rotating public key pair...', end='', canvas=b)
        rotate_private_key = Path(
            'slot_{}_ecc_private_key.pem'.format(
                self.rotating_key_slot))
        self.rotating_key = TPAsymmetricKey()
        self.rotating_key.get_private_pem(rotate_private_key)
        print('OK', canvas=b)

    def authorize_new_public_key(self, b=None):
        """Authorizing the new public Key that has been generated.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        print('Authorizing new public key...', end='', canvas=b)
        # Generate/Use Auth key pair
        auth_private_key = Path(
            'slot_{}_ecc_private_key.pem'.format(self.auth_key_slot))
        self.auth_key = TPAsymmetricKey(auth_private_key)
        self.auth_key.get_private_pem(auth_private_key)

        # Perform new key authorization
        self.key_validate = DevicePubkeyValidation(
            self.auth_key_slot, self.rotating_key_slot)
        self.key_validate.authorize_public_key(
                self.auth_key.get_private_key(),
                self.rotating_key.get_public_key_bytes())

        # Generate variables required for public key rotation embedded project
        key_rotation = DevicePubkeyValidation(
                                self.auth_key_slot, self.rotating_key_slot)
        key_rotation.save_resources(
                                self.auth_key.get_private_key(),
                                self.rotating_key.get_private_key(),
                                'pubkey_rotation.h')
        print('OK', canvas=b)

    def generate_and_authorize_newpublic_key(self, b=None):
        self.generate_new_public_key(b)
        self.authorize_new_public_key(b)

    def invalidate_existing_public_key(self, b=None):
        """Invalidating the existing public key inorder to rotate with a new public key.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        print('Invalidating existing public key...', end='', canvas=b)
        if self.key_validate.is_pubkey_validated():
            # invalidate first if it is in validated state
            slot_pub_key = bytearray(64)
            assert cal.atcab_read_pubkey(
                self.rotating_key_slot,
                slot_pub_key) == cal.Status.ATCA_SUCCESS, \
                "Reading public key from slot {} failed".format(
                    self.rotating_key_slot)
            key_invalidation = DevicePubkeyValidation(
                self.auth_key_slot, self.rotating_key_slot)
            key_invalidation.pubkey_invalidate(
                self.auth_key.get_private_key(), slot_pub_key)
        print('OK', canvas=b)

    def write_and_validate_public_key(self, b=None):
        """Writing and Validating the new public Key.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        # write key into slot
        print('Write new public key and validate it...', end='', canvas=b)
        assert cal.atcab_write_pubkey(
            self.rotating_key_slot, self.rotating_key.get_public_key_bytes()) \
            == cal.Status.ATCA_SUCCESS, \
            "Writing public key into slot {} failed".format(
                self.rotating_key_slot)

        assert cal.atcab_nonce(
            self.key_validate.nonce) == cal.Status.ATCA_SUCCESS, \
            'Loading Nonce failed'

        assert cal.atcab_genkey_base(
            0x10, self.rotating_key_slot,
            other_data=b'\x00'*3) == cal.Status.ATCA_SUCCESS, \
            'Genkey digest calculation on device failed'

        is_validated = cal.AtcaReference(False)
        assert cal.atcab_verify_validate(
            self.rotating_key_slot, self.key_validate.signature,
            self.key_validate.sign_internal_other_data, is_validated) \
            == cal.Status.ATCA_SUCCESS, \
            'Slot verification for validate failed'

        assert bool(is_validated.value), \
            'Verify validate command is success, but validation failed'
        print('OK', canvas=b)

    def verify_rotated_key(self, rotating_priv_key, b=None):
        """Verifying new rotated public Key

        Args:
            rotating_priv_key (key): New public key after writing and validated.
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        print('Verify rotated key...', end='', canvas=b)
        is_verified = cal.AtcaReference(False)
        message = os.urandom(32)
        signature = sign_on_host(message, rotating_priv_key)

        assert cal.atcab_verify_stored(
            message, signature, self.rotating_key_slot, is_verified) \
            == cal.Status.ATCA_SUCCESS, \
            'Verify command failed'

        assert bool(is_verified.value), 'Verify command is success, \
        but verification failed'
        print('OK', canvas=b)

    def verify_newpublic_key(self, b=None):
        self.verify_rotated_key(self.rotating_key.get_private_key(), b)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    pass
