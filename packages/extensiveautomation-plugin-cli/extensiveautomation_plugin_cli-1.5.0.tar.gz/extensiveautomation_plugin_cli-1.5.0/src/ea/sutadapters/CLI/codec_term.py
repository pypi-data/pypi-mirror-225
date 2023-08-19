#!/usr/bin/env python
# -*- coding=utf-8 -*-

# -------------------------------------------------------------------
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
import re
import time
import codecs
import binascii

import pyte
import threading

from ea.sutadapters.CLI import templates_term

class Observer(threading.Thread):
	"""
	"""
	def __init__(self, parent, cycleSnap=1):
		"""
		"""
		threading.Thread.__init__(self)
		self.parent = parent
		self.watchEvery = cycleSnap
		self.stopEvent = threading.Event()
		self.watching = False
		
	def stop(self):
		"""
		"""
		self.watching = False
		self.stopEvent.set()
		
	def unwatch(self):
		"""
		"""
		self.watching = False
		
	def watch(self):
		"""
		"""
		self.watching = True
		
	def run(self):
		"""
		"""
		while not self.stopEvent.isSet():   
			time.sleep(self.watchEvery)
			if self.watching: self.onWatch()
			
	def onWatch(self):
		"""
		"""
		pass
		
class Codec(object):
	def __init__(self, parent, terminalWidth, terminalHeight, cycleSnap):
		"""
		"""
		self.parent = parent
		self.warning = self.parent.warning
		self.debug = self.parent.debug
		self.info = self.parent.info

		self.connected = False

		self.snapshot_screen = ""
		self.obs = Observer(parent=self, cycleSnap=cycleSnap)
		self.obs.onWatch = self.onWatchScreen
		self.obs.start()
		
		self.stream = pyte.ByteStream()
		self.screen = pyte.Screen(terminalWidth, terminalHeight)

		self.stream.attach(self.screen) 

	def reset(self):
		"""
		"""
		self.obs.stop()

	def unwatch(self):
		"""
		"""
		self.screen.reset()
		self.connected=False
		self.obs.unwatch()
		
	def onWatchScreen(self):
		"""
		"""
		current = "%s" % "\n".join(self.screen.display)

		if current != self.snapshot_screen:
			if not self.connected:
				self.connected=True
				self.handleScreen(screen=("opened", templates_term.term_opened(data="success")  ))
				self.handleScreen(screen=("screen", templates_term.term_data(data=current.strip() )  ))
			else:
				self.handleScreen(screen=("screen", templates_term.term_data(data=current.strip() )  ))
			self.snapshot_screen = current

	def handleScreen(self, screen):
		"""
		"""
		pass
		
	def encode(self, ssh_cmd):
		"""
		"""
		evt = ssh_cmd.get('event')
		data = ssh_cmd.get('data')
		return evt.title(), data

	def decode(self, data):
		"""
		"""
		if not self.connected: self.obs.watch()
		self.debug("%s" % data)
		self.stream.feed(data)
		
#		self.onWatchScreen()




