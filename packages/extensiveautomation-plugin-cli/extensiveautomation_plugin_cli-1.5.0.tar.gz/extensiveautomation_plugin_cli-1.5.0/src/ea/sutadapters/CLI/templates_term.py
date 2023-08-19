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

from ea.testexecutorlib import TestValidatorsLib as TestValidators
from ea.testexecutorlib import TestTemplatesLib as TestTemplates
from ea.testexecutorlib import TestOperatorsLib as TestOperators
from ea.testexecutorlib import TestAdapterLib as TestAdapter

def term():
	"""
	Construct a template for term
	"""
	tpl = TestTemplates.TemplateLayer('TERM')
	return tpl

def term_open(ip=None, port=None, login=None):
    """
    Construct a template for a term event
    """
    tpl = term()
    tpl.addKey(name='event', data="open")
    if ip is not None:
        tpl.addKey(name='ip', data=ip)
    if port is not None:
        tpl.addKey(name='port', data=port)
    if login is not None:
        tpl.addKey(name='login', data=login)
    return tpl

def term_opened(data=None):
	"""
	Construct a template for a term event
	"""
	tpl = term()
	tpl.addKey(name='event', data="opened")
	if data is not None:
		tpl.addKey(name='data', data=data)
	
	return tpl
def term_open_failed(data=None):
	"""
	Construct a template for a term event
	"""
	tpl = term()
	tpl.addKey(name='event', data="open-failed")
	if data is not None:
		tpl.addKey(name='data', data=data)
	
	return tpl
def term_close():
	"""
	Construct a template for a term event
	"""
	tpl = term()
	tpl.addKey(name='event', data="close")

	return tpl
	
def term_closed():
	"""
	Construct a template for a term event
	"""
	tpl = term()
	tpl.addKey(name='event', data="closed")

	return tpl
	
def term_data(data=None):
	"""
	Construct a template for a term event
	"""
	tpl = term()
	tpl.addKey(name='event', data="text")
	if data is not None:
		tpl.addKey(name='data', data=data)

	return tpl
