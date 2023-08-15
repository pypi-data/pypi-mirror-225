import os
import stackprinter
from filelock import FileLock, SoftFileLock

# pylint: disable=broad-except

__all__ = [
    "try_filelock",
    "TryFileLock"
]


def try_filelock(
    fn,
    target_file,
    is_soft=False,
    timeout=20,
):
    lock_obj = SoftFileLock if is_soft else FileLock
    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with lock_obj(f"{target_file}._lock", timeout) as flock:
            if flock.is_locked:
                fn()
            else:
                print(f"try_filelock Timeout!!! {target_file}")
    except TimeoutError:
        print(f"TryFileLock timeout!!! {target_file}")
    except Exception as exc:
        stackprinter.show(exc, style="darkbg2")

class TryFileLock:
    def __init__(self, target_file, is_soft=False, timeout=20):
        self.target_file = target_file
        self.is_soft = is_soft
        self.timeout = timeout
        self.lock_obj = SoftFileLock if is_soft else FileLock
        self.lock = None

    def __enter__(self):
        try:
            os.makedirs(os.path.dirname(self.target_file), exist_ok=True)
            self.lock = self.lock_obj(f"{self.target_file}._lock", self.timeout)
            self.lock.acquire()
            flag = self.lock.is_locked
            if flag:
                return self
            else:
                print(f"TryFileLock can not acquire lock {self.target_file}")
                return None
        # handle timeout error
        except TimeoutError:
            # raise TimeoutError(f"TryFileLock timeout!!! {self.target_file}")
            print(f"TryFileLock timeout!!! {self.target_file}")
            return None
        except Exception as exc:
            stackprinter.show(exc, style="darkbg2")
            raise RuntimeError(f"TryFileLock error!!!")

    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_tb
        if exc_type is not None:
            print(f"TryFileLock error!!! {exc_type} {exc_val}")
        if self.lock is not None and self.lock.is_locked:
            self.lock.release()