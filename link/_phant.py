from phant import Phant
from settings import PHANT


def set_status(status):
    p = Phant(PHANT['PUBLIC_KEY'], 'status', private_key=PHANT['PRIVATE_KEY'])
    p.log(status)

# set_status("online")
