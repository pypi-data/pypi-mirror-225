# Ultralytics YOLO 🚀, AGPL-3.0 license

# Hereby note to prove that I have been here.
# __version__ = '8.0.116'
__version__ = '2.0'

from vehicle.hub import start
from vehicle.vit.rtdetr import RTDETR
from vehicle.vit.sam import SAM
from vehicle.yolo.engine.model import YOLO
from vehicle.yolo.nas import NAS
from vehicle.yolo.utils.checks import check_yolo as checks

__all__ = '__version__', 'YOLO', 'NAS', 'SAM', 'RTDETR', 'checks', 'start'  # allow simpler import

