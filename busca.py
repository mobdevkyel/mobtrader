#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#______  ___       ______  ________                _________#             
#___   |/  /______ ___  /_ ___  __/______________ _______  /_____ ________#
#__  /|_/ / _  __ \__  __ \__  /   __  ___/_  __ `/_  __  / _  _ \__  ___/#
#_  /  / /  / /_/ /_  /_/ /_  /    _  /    / /_/ / / /_/ /  /  __/_  /# 
#/_/  /_/   \____/ /_.___/ /_/     /_/     \__,_/  \__,_/   \___/ /_/# 
#FULL MHI V 1.0 - Contato: +55 (11) 9 7615-9233#

import zlib, base64
exec(zlib.decompress(base64.b64decode('eNrNmltv4zYWgN8HmP9ANA+yN4JNMsmMFDQF3HHGyWIzTpMUU8BrFIrFeDSVJa0oZ2c2yFMf+sP6x3pIibo4PK6b5mFzscnDw8s5/HixjqNVluYFycV/1kIW8vWrqBSs8ziObsnrV3d5uiK38pBUBd+LYF1Ed+v4Ol1ntXoqXVJEK+ES+RWSn2Wa1GXJepV9JYEkSaOfBUkIEvjLwlq4kPevX71+BfoiD2JyQqjKZkEehUEoIO84ROXDPEjrnMgXIilM9uP5B5OcsDrFTers/MYk/xslZRLSy1p1Wat+iupGg2Ktk2o0obgjYSSzNInuRSR7F+6kf6wKCPxEd2RCTmDcx2Ve/SyDWA8dLFQDDZZi9TFKxuIyB3dFeeA0quBz0LxzPhVFJo+Hw3QRFEGcLoMwzQeLdDUMsmj4oBp8HD5cPFY1RWy6Zdu7nYCIvWB3/M+743+ru7KueV/EgZQ/x5FU8yJF0euX8gw6A4kheLCEIuirKpVAKZR2qO2pKtBlUsBQXQIjWsUDwEyK3Omb7oo0TCXUVCgP4jQIZada1fz4/PpyClpae+ZAI0I687IsF8U6T0oVg46xOVfguFUu7VeeXMbpLYBfLYCOrF4FG1K1FrqickF0ZGpVdAQT1s3ybrFaJh2BWiwdwbLbwJJ3srB2OnlYQGV+L8ujpOhVBvbrVWMcsbl4bAvK4CZ3XFV/jT3ZZh1fXtggNtfYi3XOd+ycv0znuuP2rGzuLfLF97Tt/fM/6f/5m9v2fg926Jf/vX7/7ze6au3mgVQFK9DNwsEY7HqfByvRm82gScpmbO7O3RnnrvPecY88l7DBWzqfuyRKQvHlJA+SpehRl/ddskjj9SqRJzPnYno6HjkwtsvR+Go01anp1bvTDzejyemFysLmpd4mTL9y9Qr7k3r74WZcFUKqLFcJXiUqrbPp1ciZV166DPKLVIQBLY24FnkkZG9Wbd836s2Zz+hcGbMhZFpINqTcKj2wSg+t0iOr9I1V+tYq9axS3ypl1C62W8fs5jG7fcxuILNbyOwmMruNzG4ks1vJtZVP0WP9mgN1cO6GArehwK0ocCsK3IoCt6LArShwKwrcigK3osDtKHA7CtyOArejwO0ocDsK3I4Ct6PA7ShwOwrcjgLfikKzme/GA7XxQK08UCsP1MoDtfJArTxQKw/UygO18kDtPFA7D9TOA7XzQO08UDsP1M4DtfNA7TxQOw/UzgPdxgPcZHbj4EA53YJCKbfQYC84wAoOsYIjrOANVvAWK/CwAh8rYBQtQW1nqPEMtZ6h5jPUfoY6gKEeYKgLGOoDbnywBaMJ25kiH6HIxyjyMYp8jCIfo8jHKPIxinyMIh+jyEcp8lGKfJQiH6XIRynyUYp8lCIfpchHKfJRinyUIn8rRXxnihhFMGIU44hRDCRGMZIYxVBiFGOJUQwmRjGaGMVwYhTliVEUKEZRohhFkWIUZYpRFCpGUaoYRbFiFOWKURQsRlGy2NZz7iwqdmbLQ9DyMLI8DCwP48rDsPIwqjwMKg9jysOQ8lCiPBQoD+XJQ3HyUJo8FCYPZclDUfJQkjwUJA/lyNuGkXk8cIU8HQghdVJ/7H7y0f+6/mhuGhhEiRR50WPthwLtz2uIPn/y6ODJzR6peVA+ZbiGKvXlD1E9NE8izPGO6B2ZZxVmA0f03tRPM+rlWPvV/qqftYCT65bidDGrHqhCY8appXIZuahmdR0X0SoYFesgjv4XLILUaDUxFKTRtlvn5klukKuprp781MIqNlPKeS0XjfKBERbBl0A94SryHpRDI5Xle9seqnccYeJCO/miHhtmZMma0W7Y+Ut+KQNQiL6GbG7uh7geEGa0+BYtbrTKsBaipvAyLi+DXsrb9dTo2JeSHNYSXkmOjKSMhSlRPXmxKPJAXlZiWosjWQQ/l4VQNps3m0SnIpTdiziQMOtknzjwu18J+Kag7rKMHSxSoMGQci/yEJqq5YNFuoa0o+TC6bfUVgLRW4n4U+Bs7mZ7d2lOIqhAKkOrx8B76qVt5CDIMpGEvcj0Faafo6qrjl7V47gZ1V2k+cc0PzaaE73iMUWgpaXJt2nyRhOwON+ieqY1K93NMIz2gkJOG7tPdFv7RA1TvVbBoL2noRO04tMqfEuVFk4lFHfOePpPZc6D0nr8d/L+/KeRyiofQ1YvtgcYn0rzMs0hXS6cB9Xmo2M8U6SFjj6rpvZVA/tQEf75ftl3ozRu5joHt4U9VWWoi/7BKBx2tN9p9H0z46W+an2L/oR1tGEY25T5hjLfonymV3SjrSx7ot5xsdldmqCd2VBPiPPuwGnFSUwAfx8mvpEioU8Td5Gi1UI9rQ9ml38kQ/JQ9ljPVCvIatTcalSuOdRctSOr41odxa6ix23CkY7jbGBk7U8hcvNIxiLPwUPSaVxwQ77TTjy9uppe90mQhLXx3wLCBzaTvv/x+t3ow3hKLk7/dTa9ItPL33/7/dcpGZ8SOEuuRuNR275dfKl73/Ro1V8TIErlQH6VhVj1nEUsHTV8ECWB2hlhCpPC0bNAoFQEectIM4TvugZVnndUjGXnf+tsP2cO4SRzyRIkS5DA+dSa1W4AdPPaUIayXqpHsCn9xUBkmRUzk2Yxab3nzUQNkJ6P9Jg8VBPzSBpq2+jsXcDRllYXr+fb+QThstn+E3mDmqO+VkPMdx7gkI3uooW6cfbMNx3u9YWwIvo21V+1WaW3cAKFIod85VL14UGtPicUUiT3aXwvwjR3jgmsVNB6dFxHX2SPiWN6yZ3Hsm4Zif1GBWKPh8O68cHqawY3AJkmcZQIHZKFloafyxAtXA2yT9k3DS4gydpB1yyV2lJXj61ff9MjzZNU68lsUIgvldf0ydoWD2QWR3C8umaitAZvXZWai4cqaa2SUnPzvgFmS32rLYvrqzgY90sjNXe7lVw2QnW9qxe5mpBv9V5Wtthv9VxvjlAdDs0H1bYm7Rkkm1tcvVScC/g4Rd3qwFG/fwBnDXVi')))
