import ulogger


class Clock(ulogger.BaseClock):
    def __init__(self):
        pass
        
    def __call__(self) -> str:
        return '--' 
clock = Clock()
    
handlers = (
    ulogger.Handler(
        level=ulogger.INFO,
        colorful=True,
        fmt="&(time)% - &(level)% - &(name)%  - &(msg)%",
        clock=clock,
        direction=ulogger.TO_TERM,
    ),
    ulogger.Handler(
        level=ulogger.ERROR,
        fmt="&(time)% - &(level)% - &(name)%  - &(msg)%",
        clock=clock,
        direction=ulogger.TO_FILE,
        file_name="logging.log",
        max_file_size=1024 # max for 1k
    )
)

def get_logger(name: str):
    return ulogger.Logger(name, handlers)
all = (get_logger)