#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#______  ___       ______  ________                _________#             
#___   |/  /______ ___  /_ ___  __/______________ _______  /_____ ________#
#__  /|_/ / _  __ \__  __ \__  /   __  ___/_  __ `/_  __  / _  _ \__  ___/#
#_  /  / /  / /_/ /_  /_/ /_  /    _  /    / /_/ / / /_/ /  /  __/_  /# 
#/_/  /_/   \____/ /_.___/ /_/     /_/     \__,_/  \__,_/   \___/ /_/# 
#FULL MHI V 1.0 - Contato: +55 (11) 9 7615-9233#

import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
