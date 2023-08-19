#!/usr/bin/env python
# -*- coding=utf-8 -*-

# ------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2010-2021 Denis MACHARD
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -------------------------------------------------------------------

import sys

from ea.testexecutorlib import TestValidatorsLib as TestValidatorsLib
from ea.testexecutorlib import TestTemplatesLib as TestTemplatesLib
from ea.testexecutorlib import TestOperatorsLib as TestOperatorsLib
from ea.testexecutorlib import TestAdapterLib as TestAdapterLib

def curl_http(more=None):
	"""
	Construct a template for a HTTP packet
	"""
	tpl = TestTemplatesLib.TemplateLayer('CURL_HTTP')

	# add additional keys
	if more is not None:
		tpl.addMore(more=more)
		
	return tpl

def response(version=None, code=None, phrase=None, headers=None, body=None):
	"""
	"""
	tpl = TestTemplatesLib.TemplateLayer('CURL_HTTP_RESPONSE')
	
	if phrase is not None:
		tpl.addKey(name='phrase', data=phrase)
	if code is not None:
		tpl.addKey(name='code', data=code)
	if version is not None:
		tpl.addKey(name='version', data=version)	

	if headers is not None:
		tpl.addKey(name='headers', data=headers )
	if body is not None:
		tpl.addKey(name='body', data=body)
	return tpl