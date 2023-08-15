import os
import torch
import stackprinter
from filelock import FileLock, SoftFileLock
from .basic import get_rank, get_world_size, print0

# pylint: disable=broad-except

def try_filelock(
    fn,
    target_file,
    is_soft=False,
    timeout=20,
    device="cuda",
):
    lock_obj = SoftFileLock if is_soft else FileLock
    try:
        if get_rank() == 0:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            lock = lock_obj(f"{target_file}._lock", timeout)
            lock.acquire()
            flag = lock.is_locked
        else:
            flag = False
        # create a one element tensor and broadcast it from rank 0
        flag = torch.tensor(flag, device=device)
        if get_world_size() > 1:
            torch.distributed.broadcast(flag, src=0)
        if flag.item():
            fn()
        else:
            print0(f"try_filelock Timeout!!! {target_file}")
    except TimeoutError:
        print0(f"TryFileLock timeout!!! {target_file}")
    except Exception as exc:
        stackprinter.show(exc, style="darkbg2")
    finally:
        if get_rank() == 0 and lock.is_locked:
            lock.release()

class TryFileLock:
    def __init__(self, target_file, is_soft=False, timeout=20, device="cuda"):
        self.target_file = target_file
        self.is_soft = is_soft
        self.timeout = timeout
        self.lock_obj = SoftFileLock if is_soft else FileLock
        self.lock = None
        self.device = device

    def __enter__(self):
        try:
            if get_rank() == 0:
                os.makedirs(os.path.dirname(self.target_file), exist_ok=True)
                self.lock = self.lock_obj(f"{self.target_file}._lock", self.timeout)
                self.lock.acquire()
                flag = self.lock.is_locked
            else:
                flag = False
            # create a one element tensor and broadcast it from rank 0
            flag = torch.tensor(flag, device=self.device)
            if get_world_size() > 1:
                torch.distributed.broadcast(flag, src=0)
            if flag.item():
                return self
            else:
                print0(f"TryFileLock can not acquire lock {self.target_file}")
                return None
        # handle timeout error
        except TimeoutError:
            # raise TimeoutError(f"TryFileLock timeout!!! {self.target_file}")
            print0(f"TryFileLock timeout!!! {self.target_file}")
            return None
        except Exception as exc:
            stackprinter.show(exc, style="darkbg2")
            raise RuntimeError(f"TryFileLock error!!!")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_tb
        if exc_type is not None:
            print0(f"TryFileLock error!!! {exc_type} {exc_val}")
        if self.lock is not None and self.lock.is_locked:
            self.lock.release()