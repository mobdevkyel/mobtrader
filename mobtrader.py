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
