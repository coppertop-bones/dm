

from coppertop.pipe import *
import dm.pp
from _.dm.pp import PP

from coppertop._testing_ import take2
take2._take >> typeOf >> PP

from coppertop._testing_ import take1
take1._take >> typeOf >> PP

from _.coppertop._testing_.take1 import _take as fred    # pylist*T ^ pylist
fred >> typeOf >> PP

from _.coppertop._testing_.take2 import _take as joe    # pylist*T ^ pylist
joe >> typeOf >> PP

from _.coppertop._testing_.take1 import _take as sally    # pydict*T ^ pydict
sally >> typeOf >> PP

from _.coppertop._testing_.take2 import _take as sally    # pydict*T ^ pydict
sally >> typeOf >> PP

from _.coppertop._testing_.take1 import _take
_take >> typeOf >> PP

from _.coppertop._testing_.take2 import _take     # pydict*T ^ pydict
_take >> typeOf >> PP

