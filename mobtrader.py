

import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
