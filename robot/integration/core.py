from robot.integration.phant import Phant

def phant():
    from robot.integration.settings import PHANT
    p = Phant(PHANT['PUBLIC_KEY'], 'status', private_key=PHANT['PRIVATE_KEY'])
    p.log("online")
