from phant import Phant

def set_status(status):
    from settings import PHANT
    p = Phant(PHANT['PUBLIC_KEY'], 'status', private_key=PHANT['PRIVATE_KEY'])
    p.log(status)

set_status("online")
