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
