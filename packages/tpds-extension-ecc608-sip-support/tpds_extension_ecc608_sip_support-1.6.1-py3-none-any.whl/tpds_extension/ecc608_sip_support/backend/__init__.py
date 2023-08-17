import os
from tpds.devices import TpdsDevices, TpdsBoards

# Add the Part information
TpdsDevices().add_device_info(os.path.join(os.path.dirname(__file__), 'parts'))

# Add the Board information
TpdsBoards().add_board_info(os.path.join(os.path.dirname(__file__), 'boards'))
