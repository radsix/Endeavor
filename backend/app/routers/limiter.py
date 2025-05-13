from slowapi import Limiter
from slowapi.util import get_remote_address

# controls the amount of time passed before sending another request for create, update, and destroy
limiter = Limiter(key_func=get_remote_address)
lim_rate = "1/second"