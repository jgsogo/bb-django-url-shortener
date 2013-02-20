#!/usr/bin/env python
# encoding: utf-8

from math import pow
import random
import re
import logging

from django.test import TestCase

from shortener.utils.baseconv import BaseConverter

log = logging.getLogger(__name__)


class BaseconvTest(TestCase):
    """
    Test for lower-upper bounds from char length and reverse conversion
    """

    def _baseconv_test(self, str_code, max_chars=8):
        zero_alike = str_code[0]
        log.debug("Test baseconv with str_code '%s' (%s)" % (str_code, len(str_code)))
        bin = BaseConverter(str_code)
        base = len(str_code)
        lower_bound = 0
        for i in range(1, max_chars, 1):
            upper_bound = int(pow(base,i))
            log.debug("%s characters [%e, %e) => [%s, %s)" % (i, lower_bound, upper_bound, bin.from_decimal(lower_bound), bin.from_decimal(upper_bound-1)))
            self.assertEqual(i, len(bin.from_decimal(lower_bound)), "Mismatch char number")
            self.assertEqual(i+1, len(bin.from_decimal(upper_bound)), "Mismatch char number")
            #for n in range(lower_bound, upper_bound, 10):
            #    self.assertEqual(i, len(bin.from_decimal(n)), "Mismatch char number")
            lower_bound = upper_bound

        # test reversion
        for i in xrange(10):
            number = random.randint(0, upper_bound)
            log.debug("Test reverse conversion for number '%s'" % number)
            self.assertEqual(number, bin.to_decimal(bin.from_decimal(number)))
            char_str = ''.join(random.choice(str_code) for x in range(max_chars))
            char_str = re.sub("^%s+"%zero_alike, "", char_str) # Remove leading zeros
            log.debug("Test reverse conversion for char string '%s'" % char_str)
            self.assertEqual(char_str, bin.from_decimal(bin.to_decimal(char_str)))

    def test_bin(self):
        """
        Test binary conversion
        """
        # max length
        str_code = '01'
        self._baseconv_test(str_code, 9)

    def test_hex(self):
        """
        Test hexadecimal conversion
        """
        # max length
        str_code = '0123456789ABCDEF'
        self._baseconv_test(str_code, 9)

    def test_base62(self):
        """
        Test base62 conv
        """
        # max length
        str_code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
        self._baseconv_test(str_code, 9)