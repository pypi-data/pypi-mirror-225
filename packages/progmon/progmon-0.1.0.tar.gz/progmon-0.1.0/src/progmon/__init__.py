#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright notice
# ----------------
#
# Copyright (C) 2011-2023 Daniel Jung
# Contact: proggy-contact@mailbox.org
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
#
"""progmon - a simple progress monitor

This module offers different methods for showing the current status of an
iterative algorithm, or to control its execution, for example to abort it as
soon as certain abort criterions are met."""

import calendar
import subprocess
import datetime
import numpy
import os
import select
import signal
import sys
import time

try:
    import termios  # only available on POSIX systems (Linux, Mac OS X, ...)
    import tty  # requires termios
except ModuleNotFoundError:
    termios = None
    tty = None

class Bar(object):
    """Display a progress bar when executing a loop with a fixed number of
    iterations.

    Usage:

    Instantiate this class before loop. Call the method *step()* at the end of
    each loop (do not forget to do the same before any occurence of
    *continue*). If the loop is left early (i.e., if *break* is called), or if
    you want to make sure the line break is done after the loop, call the
    method *end()*. To reset the counter, call the method *reset()*.

    On initialization, the number of iterations *nstep* must be specified.
    Additional keyword arguments include:

    *text*
        User-defined text message (instead of "Progress").
    *width*
        Width of the current shell window. Default: 80.
    *verbose*
        If set to *False*, the progress bar is not displayed.
    *etc*
        If set to *True*, show "Estimated Time to Complete". The remaining time
        the loop will need to finish is calculated by linear extrapolation of
        the time that already passed since the loop has been entered.

    This class is meant to be used in loops where the number of iteration steps
    is already known before entering the loop (i.e., for-loops). This excludes
    all iterative algorithms that leave the loop on some convergence criterions
    after a variable number of steps (e.g., while-loops). Of course, the number
    of loops that will probably be used could be estimated, but this is not the
    way this class is intended to be used. See the class *OpenBar* for that.
    """
    
    def __init__(self, nstep=1, text='progress', width=None, verbose=True,
                 etc=True):

        now = time.time()
        self._nstep = nstep
        self._step = 0
        self._jump = 0
        self._oldline = ''
        self._end = False
        self._text = text
        self._verbose = verbose
        self._etc = etc  # show estimated time of completion
        self._starttime = now  # starting time
        self._lastcall = now  # time when step or jump was last called
        self._jumptime = 0  # count time that was used only for jumping

        # do not show the error bar if number of steps is zero
        if self._nstep == 0:
            self._verbose = False

        # get width of the terminal window
        if width is not None:
            self._width = width
        else:
            self._width = get_columns()

        # print initial status to the screen
        if not self._verbose:
            return
        self.write()

    def step(self, howmany=1):
        """Move one or several steps forward."""
        if not self._verbose:
            return
        self._step += howmany
        if self._step > self._nstep:
            self._step = self._nstep

        # print new status
        self.write()

        # note time of this call
        now = time.time()
        self._lastcall = now

    def jump(self, howmany=1):
        """Skip one or several steps. Using this instead of *step()* is only
        important for the correct calculation of the estimated time to complete
        (ETC).
        """
        if not self._verbose:
            return
        self._step += howmany
        if self._step > self._nstep:
            self._step = self._nstep
        self._jump += howmany
        if self._jump > self._step:
            self._jump = self._step

        # add time difference since last call to the jump time counter
        now = time.time()
        self._jumptime += now-self._lastcall

        # print new status
        self.write()

        # remember time of this call
        self._lastcall = now

    def write(self):
        """Update the progress bar on the screen.
        """
        if not self._verbose:
            return

        now = time.time()

        if self._nstep == 1:
            # just say "done" when finished
            line = self._text+': '
            if self._step == 1:
                line += 'Done.'
        else:
            # calculate progress
            progress = float(self._step)/self._nstep

            # calculate estimated time to complete (ETC), use linear
            # extrapolation
            etcstring = ''
            if self._etc:
                if self._nstep-self._jump != 0:
                    jprogress = \
                        float(self._step-self._jump)/(self._nstep-self._jump)
                    jelapsed = now-self._starttime-self._jumptime
                    if jprogress > 0:
                        jestimate = jelapsed/jprogress
                        jdiff = jestimate-jelapsed
                        etcstring = ' ETC %s' % _nicetime(jdiff)

            # calculate length of the progress bar
            barlen = self._width - 9 - len(self._text) - len(etcstring) - 1

            # create the new line
            line = '%s:% 4i%%' % (self._text, progress*100)
            if barlen > 0:
                line += ' [%- *s]' % (barlen, '='*int(progress*barlen))
            line += etcstring

        # if line has changed, overwrite the old one
        if line != self._oldline:
            sys.stdout.write('\r'+line)
            sys.stdout.flush()

        # remember old line
        self._oldline = line

        # check if progress bar is complete
        if self._step == self._nstep:
            self.end()

    def end(self):
        """Leave the progress bar, insert a line break on the screen.
        """
        if not self._verbose:
            return
        if not self._end:
            sys.stdout.write('\n')
            self._end = True

    def reset(self):
        """Reset the counter, start over with the progress bar.
        """
        self.end()
        now = time.time()
        self._step = 0
        self._jump = 0
        self._oldline = ''
        self._end = False
        self._starttime = now
        self._lastcall = now
        self._jumptime = 0

    def __del__(self):
        self.end()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end()


class OpenBar(object):
    """Display progress bar of an unlimited iteration process ("open-end"). Use
    this if the total number of iterations is unclear, i.e. the loop may be
    exited at any point (e.g., while loop). However, to display a progress bar,
    some measure of progress must still be defined (start and target values).
    If the start value is None, use the value given by the first call of step.

    Intended use: For example, an iterative averaging process will be aborted
    as soon as a certain accuracy has been reached. The progress measure will
    be this accuracy.
    """

    def __init__(self, target, start=None, text='progress', width=None,
                 verbose=True, etc=False):
        raise NotImplementedError


class Monitor(object):
    """Monitor the values of certain variables as they change within a loop
    (e.g., for iterative algorithms). Depends on the class *StatusLine*.

    Update the line by using carriage return each time the method *step()* is
    called. Do this until the method *end()* is called (then, a line break is
    issued).
    """

    def __init__(self, **kwargs):
        # define standard formats for some types
        self._stdformats = {int: '%i', str: '%s', float: '%.2f'}  # complex: '%.2f + %.2fi' ??

        # fetch special keyword arguments
        self._stdformats.update(**kwargs.pop('stdformats', {}))
        self._verbose = kwargs.pop('verbose', True)
        self._sep = kwargs.pop('sep', '  ')
        cols = kwargs.pop('cols', get_columns())
        delay = kwargs.pop('delay', 1.)
        self._formats = kwargs.pop('formats', {})  # formats dictionary
        self._order = kwargs.pop('order', [])  # force a certain display order

        # store remaining keyword arguments
        self._values = kwargs

        # define additional attributes
        self._lengths = {}  # lengths dictionary

        # initialize status line object
        self._line = StatusLine(delay=delay, cols=cols)

        # first output is already displayed at initialisation
        if not self._verbose:
            return
        self._write()

    def update(self, **values):
        """Update the values of one or more variables, or add new variables to
        the status line.
        """
        if not self._verbose:
            return
        self._values.update(**values)
        self._write()

    #def update_value(self, name, value):
        # """Update one value, or add a new variable to monitor. This is for
        # calls from other Cython modules only, as Cython cannot handle
        # variable argument lists. So, for each value to update, a separate
        # call of this method must be made.
        # """
        #if not self._verbose:
        #return
        #self._values[name] = value
        #self._write()

    def end(self):
        """Finish monitoring values, issue a line break (if not already done).
        Update the status line one last time."""
        if not self._verbose:
            return
        self._line.end()

    def reset(self):
        """Reset the status line. Empty the list of values and begin a new
        status line.
        """
        if not self._verbose:
            return
        self.end()
        self._values = {}
        self._write()

    def _write(self):
        """Write new line to stdout (overwrite existing line using carriage
        return). If *now* is *True*, tell the *StatusLine* instance to ignore
        the delay.
        """

        if not self._verbose:
            return

        # create list of keys. Begin with ordered keys, sort the rest by
        # alphabet
        keys = self._order[:]
        for key in keys[:]:
            if key not in self._values:
                keys.remove(key)
        restkeys = sorted(self._values.keys())
        for key in restkeys:
            if key not in keys:
                keys.append(key)

        # collect all string representations in a dictionary
        strings = {}
        for key in keys:
            value = self._values[key]
            valuetype = type(value)
            if value is not None and key in self._formats:
                strings[key] = '%s=%s' \
                    % (key, self._formats[key].__mod__(value))
            elif value is not None and valuetype in self._stdformats:
                strings[key] = '%s=%s' \
                    % (key, self._stdformats[valuetype].__mod__(value))
            else:
                strings[key] = '%s=%s' % (key, repr(value))

        # update maximal lengths of the strings
        for key in keys:
            if key not in self._lengths \
                    or len(strings[key]) > self._lengths[key]:
                self._lengths[key] = len(strings[key])

        # create resulting line and pass it to the status line object
        line = self._sep.join('%- *s' % (self._lengths[key], strings[key])
                              for key in keys)
        self._line.update(line)

    def __del__(self):
        return self.end()

    def remove(self, *names):
        """Stop monitoring the specified variables.
        """
        for name in names:
            del self._values[name]
            del self._lengths[name]
            del self._formats[name]
        self._write()

    # def remove_value(self, name):
    #     """Stop monitoring the specified variable."""
    #     del self._values[name]
    #     del self._lengths[name]
    #     del self._formats[name]
    #     self._write()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self.end()

    def set_delay(self, delay):
        """Set the delay of the StatusLine instance.
        """
        if delay < 0:
            raise ValueError('delay must be a non-negative float')
        self._line.delay = float(delay)


class Abort(object):
    """Check keyboard buffer for a certain key to be pressed.

    Initialize before your loop (e.g., of an iterative algorithm). Check within
    the loop body (e.g., break the loop on positive check). Finalize (end)
    after the loop. Do not forget to finalize, so that your terminal is put
    back into normal mode! Or use it as context manager (use the *with*
    statement), then finalization is done automatically.

    Hint: This only works on POSIX systems right now (Linux, Mac OS X, ...).

    Example:

        >>> import time
        >>> with Abort() as a:
        >>>     for i in range(10):
        >>>         time.sleep(1)  # do something
        >>>         if a.check():
        >>>             break  # leave loop early, because "q" has been pressed
    """

    def __init__(self, key='q', timeout=0):
        """Initialize. Specify key and timeout. Put terminal into cbreak mode.
        """

        # get key
        if len(key) != 1:
            raise ValueError('invalid key')
        self.key = key
        ### how to use the ESC key?

        # enable this class
        self.disabled = False

        # initialize the "aborted" flag
        self.aborted = False

        # initialize other attributes
        try:
            self.oldattr = termios.tcgetattr(sys.stdin)
        except AttributeError:
            sys.stdout.write('Warning: Could not get tty attributes. Probably this is not a POSIX system. '
                             'Abort key will be disabled.\n')
            self.disabled = True  # disable, probably does not work with nohup
            return

        self.buff = ''  # collect all other pressed keys, in case needed
        self.timeout = timeout
        self.count = 0  # count the total number of checks made

        # enter cbreak mode
        try:
            tty.setcbreak(sys.stdin.fileno())  # only exists on POSIX systems
        except AttributeError:
            sys.stdout.write('Warning: Could not enter cbreak mode. Probably this is not a POSIX system. '
                             'Abort key will be disabled.\n')
            self.disabled = True
    
    def check(self):
        """Check if the key has been pressed by now. All other contents of the
        keyboard buffer are ignored.
        """

        if self.disabled:
            return
        if self.aborted:
            return True

        self.count += 1
        while len(select.select([sys.stdin], [], [], self.timeout)[0]) > 0:
            char = sys.stdin.read(1)
            if char == self.key:
                self.aborted = True
                return True
            self.buff += char
        return False

    def end(self):
        """Finalize. Put the terminal back into normal mode. Return string
        buffer.
        """
        if self.disabled:
            return

        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.oldattr)
        except:
            pass  # should a warning be issued?

        return  # self.buff  # creates a lot of output ("qqqqqqqqqqqqq")

    def __del__(self):
        self.end()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end()

    def reset(self):
        """Reset the abort handler.
        """
        self.aborted = False

    def report(self):
        """If the handler was triggered, display a message.
        """
        if self.aborted:
            print(f'Process has been aborted by key press ({self.key})')


class Until(object):
    """Check if a certain date/time has been reached. Can be used to
    conveniently confine the execution time of an iterative algorithm.

    You can specify either a maximum duration (execution time) or a specific
    datetime.

    Example:

    >>> import time
    >>> with Until('1m') as u:  # run at most for one minute
    >>>     for i in range(1000):
    >>>         time.sleep(1)  # do something
    >>>         if u.check():
    >>>             break  # leave loop early, because datetime/duration has been reached
    """

    MONTHS = [month.lower() for month in calendar.month_name[1:]]
    MONTHS_SHORT = [month.lower() for month in calendar.month_abbr[1:]]
    DAYS = [day.lower() for day in calendar.day_name]
    DAYS_SHORT = [day.lower() for day in calendar.day_abbr]
    DAYNUM = dict(zip(DAYS + DAYS_SHORT, list(range(7)) + list(range(7))))
    MONTHNUM = dict(zip(MONTHS + MONTHS_SHORT, list(range(1, 13)) + list(range(1, 13))))
    SPECIAL = ['tomorrow']

    def __init__(self, until=None):
        """Initialize. Specify datetime or duration.
        """

        # remember time when object was created
        self.created = time.time()  # [seconds since begin of epoch]

        # initialize timestamp which will be determined from "until"
        self.timestamp = self.created  # [seconds since begin of epoch]

        if until is None:
            self.timestamp = None
        elif isinstance(until, int) or isinstance(until, float):
            # assume that timestamp is directly given
            self.timestamp = float(until)
        elif isinstance(until, datetime.datetime):
            # support datetime.datetime objects
            self.timestamp = time.mktime(until.timetuple())
        elif isinstance(until, datetime.timedelta):
            # support datetime.timedelta objects
            self.timestamp = self.created+until.total_seconds()
        elif isinstance(until, str):
            # parse string
            # decide if a date-time combination or a duration is given
            # criterion: for a date/time, at least one character out of "/-:."
            # or some known phrases (for weekdays or months) must be given
            if until == '':
                # run indefinitely
                self.timestamp = None
            elif self.isdatetime(until):
                # parse datetime
                until = until.lower()
                for word in until.split(' '):
                    if self.one_eq(self.DAYS + self.DAYS_SHORT, word):
                        self.goto_day(word)
                    elif self.one_eq(self.MONTHS + self.MONTHS_SHORT, word):
                        self.goto_month(word)
                    elif word == 'tomorrow':
                        self.goto_tomorrow()
                    elif word.count(':') == 1:
                        hours, minutes = word.split(':')
                        self.goto_time(hours, minutes)
                    elif word.count(':') == 2:
                        hours, minutes, seconds = word.split(':')
                        self.goto_time(hours, minutes, seconds)
                    elif len(word) == 4 and self.only_digits(word):
                        self.goto_year(int(word))
                    elif len(word) in (1, 2) and self.only_digits(word):
                        self.goto_mday(int(word))
                    elif word.count('/') == 2:
                        ### also respect Korean/American dates here, e.g. 10/29/2012
                        year, month, mday = word.split('/')
                        self.goto_date(year, month, mday)
                    elif word.count('-') == 2:
                        year, month, mday = word.split('-')
                        self.goto_date(year, month, mday)
                    elif word.count('.') == 2:
                        mday, month, year = word.split('.')
                        #year = None if year == ''
                        self.goto_date(year, month, mday)
                    else:
                        raise ValueError('bad datetime word: %s' % word)
            else:
                # parse duration
                current = ''
                dur = 0  # duration in seconds
                for char in until:
                    if char == ' ':
                        continue
                    elif char in 'hmsayMwd':
                        # process current value
                        if char == 's':
                            dur += int(current)
                        elif char == 'm':
                            dur += int(current) * 60
                        elif char == 'h':
                            dur += int(current) * 3600
                        elif char == 'd':
                            dur += int(current) * 86400
                        elif char == 'w':
                            dur += int(current) * 604800
                        elif char == 'M':
                            dur += int(current) * 2592000  # 1 month == 30 days
                        elif char in 'ay':
                            dur += int(current) * 31104000  # 1 year == 360 days

                        # reset current word
                        current = ''
                    elif char in '0123456789':
                        current += char
                    else:
                        raise ValueError('bad character: %s' % char)

                if current != '':
                    raise ValueError('bad duration word (missing unit): %s'
                                     % current)

                # set timestamp
                self.timestamp += dur

        # check if timestamp is in the past
        if self.timestamp is not None and self.timestamp < self.created:
            raise ValueError('given timestamp is in the past: %s'
                             % time.ctime(self.timestamp))

    def goto_tomorrow(self):
        """Move timestamp forward to the next day.
        """
        tdict = time.localtime(self.timestamp)
        tlist = list(tdict)
        tlist[2] += 1
        self.timestamp = time.mktime(tlist)
        self.goback_midnight()

    def goto_date(self, year, month, mday):
        """Move timestamp to the given date.
        """

        # get timestamp
        tdict = time.localtime(self.timestamp)
        tlist = list(tdict)

        # force integer values
        month = int(month)
        mday = int(mday)

        if year != '':
            year = int(year)
            tlist[:3] = year, month, mday
        else:
            if month > tdict.tm_mon:
                tlist[1:3] = month, mday
            elif month < tdict.tm_mon:
                tlist[0] += 1  # go to next year
                tlist[1:3] = month, mday
            else:
                if mday > tdict.tm_mday:
                    tlist[2] = mday
                else:
                    tlist[0] += 1  # go to next year
                    tlist[2] = mday

        # overwrite timestamp
        self.timestamp = time.mktime(tlist)
        self.goback_midnight()

    def goto_year(self, year):
        """Move timestamp forward to the given year.
        """

        # get timestamp
        tdict = time.localtime(self.timestamp)
        tlist = list(tdict)

        year = int(year)
        if year > tdict.tm_year:
            tlist[0] = year
        elif year < tdict.tm_year:
            raise ValueError('given year is in the past: %s' % year)

        # overwrite timestamp
        self.timestamp = time.mktime(tlist)

    def goto_mday(self, mday):
        """Move timestamp forward to the given day of the month.
        """

        # get timestamp
        tdict = time.localtime(self.timestamp)
        tlist = list(tdict)

        mday = int(mday)
        if mday > tdict.tm_mday:
            tlist[2] = mday
        else:
            tlist[1] += 1  # go to next month
            tlist[2] = mday

        # overwrite timestamp
        self.timestamp = time.mktime(tlist)

    def goto_time(self, hours=0, minutes=0, seconds=None):
        """Move timestamp forward to the next given time.
        """

        # force integer values
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds) if seconds is not None else None

        # get timestamp
        tdict = time.localtime(self.timestamp)
        tlist = list(tdict)

        # case study: go to next day or not?
        if hours > tdict.tm_hour:
            tlist[3:6] = [hours, minutes, 0 if seconds is None else seconds]
        elif hours < tdict.tm_hour:
            tlist[2] += 1  # go to next day
            tlist[3:6] = [hours, minutes, 0 if seconds is None else seconds]
        else:
            if minutes > tdict.tm_min:
                tlist[4:6] = [minutes, 0 if seconds is None else seconds]
            elif minutes < tdict.tm_min:
                tlist[2] += 1  # go to next day
                tlist[4:6] = [minutes, 0 if seconds is None else seconds]
            else:
                if seconds is None:
                    tlist[2] += 1  # go to next day
                    tlist[5] = 0
                else:
                    if seconds > tdict.tm_sec:
                        tlist[5] = seconds
                    else:
                        tlist[2] += 1  # go to next day
                        tlist[5] = seconds

        # overwrite timestamp
        self.timestamp = time.mktime(tuple(tlist))

    def goto_day(self, day):
        """Move timestamp forward to the next given day of the week.
        """

        # move forward a certain number of days
        while time.localtime(self.timestamp).tm_wday != self.DAYNUM[day]:
            self.timestamp += 86400
        self.goback_midnight()

    def goback_midnight(self):
        """Move backward to the beginning of the day (midnight).
        """
        timetuple = list(time.localtime(self.timestamp))
        timetuple[3] = 0
        timetuple[4] = 0
        timetuple[5] = 0
        #timetuple[8] = -1 # because of summertime
        self.timestamp = time.mktime(timetuple)

    def goto_month(self, month):
        """Move timestamp forward to the next given month.
        """

        # move forward a certain number of months
        timetuple = list(time.localtime(self.timestamp))
        while timetuple[1] != self.MONTHNUM[month]:
            timetuple[1] += 1
            timetuple = list(time.localtime(time.mktime(timetuple)))
        self.timestamp = time.mktime(timetuple)
        self.goback_first()
        self.goback_midnight()

    def goback_first(self):
        """Move backward to the beginning of the first day of the month.
        """
        timetuple = list(time.localtime(self.timestamp))
        timetuple[2] = 1
        #timetuple[8] = -1 # because of summertime
        self.timestamp = time.mktime(timetuple)

    def check(self):
        """Check if the specified time has already been reached.
        """
        return False if self.timestamp is None \
            else time.time() > self.timestamp

    def isdatetime(self, string):
        """Decide if the given string contains a date-time combination. If so,
        return *True*. Otherwise (e.g. if it contains a duration), *False* is
        returned.
        """
        return self.one_in(['/', ':', '-', '.', 'tomorrow'] + self.MONTHS +
                           self.MONTHS_SHORT + self.DAYS + self.DAYS_SHORT,
                           string.lower())

    @staticmethod
    def one_in(seq, obj):
        """Return *True* if at least one element of the given sequence *seq* is
        contained in the given object *obj*. Otherwise, return *False*.
        """
        for elem in seq:
            if elem in obj:
                return True
        return False

    @staticmethod
    def one_is(seq, obj):
        """Return *True* if at least one element of the given sequence *seq* is
        identical to the object *obj*. Otherwise, return *False*.
        """
        for elem in seq:
            if elem is obj:
                return True
        return False

    @staticmethod
    def one_eq(seq, obj):
        """Return *True* if at least one element of the given sequence *seq* is
        equal to the object *obj*. Otherwise, return *False*.
        """
        for elem in seq:
            if elem == obj:
                return True
        return False

    @staticmethod
    def only_digits(string):
        """Return *True* if the given string contains only digits. Otherwise,
        return *False*.
        """
        for char in string:
            if char not in '0123456789':
                return False
        return True

    def __iter__(self):
        """Return iterator.
        """
        for element in list(time.localtime(self.timestamp)):
            yield element

    def __len__(self):
        return len(time.localtime(self.timestamp))

    def __repr__(self):
        if self.timestamp is None:
            return '%s()' % self.__class__.__name__
        else:
            return '%s("%s")' % (self.__class__.__name__,
                                 time.strftime('%a %b %d %X %Z %Y',
                                               time.localtime(self.timestamp)))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def report(self):
        """If this handler has been triggered, display a message.
        """
        if self.check():
            print(f'Timelimit has been reached ({time.ctime(self.timestamp)}).')


class Converge(object):
    """Check data for convergence criterion within an iterative algorithm.
    Specify a certain tolerance (accuracy) that should be reached. Increase
    the "smooth value" to average over the last few deltas.

    Example:

    >>> with Converge(tol=.1, smooth=1) as c:
    >>>     for x in range(1, 21):
    >>>         print(f'{1/x:.4f}  {c.check(1/x)}')
    
    Note that the class also works for Numpy 1D arrays. In this case, the mean
    delta is compared to the tolerance level.
    """

    def __init__(self, tol=None, smooth=1):  # active=True, criterion=None
                                             # dtype=None, shape=None
                                             # relative=False
        self.tol = tol             # requested tolerance
        self.smooth = int(smooth)  # smooth level (average over this number of
                                   # deltas)

        # initialize old-data buffer
        self._data_old = None

        # initialize delta list
        # the list will be filled with the number of delta values given by
        # smooth
        self._delta = []

    def check(self, data):
        """Check convergence criterion. Return *True* if the requested accuracy
        has been reached, otherwise *False*. If *data* is *None*, return
        *False*.
        """
        if data is None:
            return False

        # if requested tolerance is None or non-positive, do not check anything
        if self.tol is None or self.tol <= 0:
            return False

        # force numpy array
        data = numpy.array(data)  # force float datatype?

        # on first call, cannot yet check for convergence, return always False
        if self._data_old is None:
            # write to old-data buffer for the first time
            self._data_old = data
            return False

        # calculate new delta (use quadratic mean for now)
        #self._delta.append(numpy.linalg.norm((data-self._data_old)/data)/ \
                        #numpy.sqrt(data.size))
        self._delta.append(numpy.mean(numpy.abs((data - self._data_old) / data)))

        # only check the criterion if the number of deltas given by smooth is
        # already reached
        if len(self._delta) < self.smooth:
            return False

        # forget oldest delta
        if len(self._delta) > self.smooth:
            self._delta.pop(0)

        # check convergence criterion (average all available deltas)
        converged = numpy.isnan(self.tol) \
            or numpy.abs(numpy.mean(self._delta)) < self.tol

        # update old-data buffer
        self._data_old = data

        # return truth value
        return converged

    def delta(self):
        """Return the current mean delta (based on the last call of *check()*).
        Return -1 if the delta list is still empty.
        """
        if len(self._delta) > 0:
            mdelta = numpy.mean(self._delta)
            if not numpy.isnan(mdelta):
                return mdelta
            else:
                return -1
        else:
            return -1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        #if self._data_old is not None:
            #del self._data_old[:] ## difficult in Cython...
        pass

    def report(self):
        """If the handler was triggered, display a message.
        """
        if self.check():
            print('Data converged within a tolerance of {self.tol:g}.')


def get_columns():
    """Try to get the number of columns of the current terminal window. If
    failing, return standard width (80 columns).
    """
    try:
        # then try environment variable
        columns = int(os.environ['COLUMNS'])
    except (KeyError, ValueError):
        # try tput
        try:
            columns = int(subprocess.getoutput('tput cols'))
        except:
            # otherwise, assume standard width
            columns = 80
    return columns


class StatusLine(object):
    """Show a status line that is updated by the user every once in a while
    using "carriage return".

    Example:

    >>> import time
    >>> with progmon.StatusLine('initial content') as sl:
    >>>     time.sleep(1)
    >>>     sl.update('new content')
    >>>     time.sleep(1)
    >>>     sl.update('new content 2')
    >>> print('done')
    """

    def __init__(self, line='', delay=0., cols=None):
        """Initialize status line object. Can be given an initial line, a
        minimum delay time and a custom number of columns (terminal width, will
        be obtained automatically on Unix systems).
        """

        # set delay
        self.delay = float(delay)

        # get number of columns (terminal width)
        if cols is None:
            self.cols = get_columns()
        else:
            self.cols = cols

        # initialize old line buffer
        self._oldline = ''
        self._oldtime = time.time()

        # remember if line break already occured
        self._ended = False

        # only reset status line if it was already used
        self._started = False

        # print line for the first time
        self._write(line)

    def _write(self, line):
        """Write the given line, replacing the old one.
        """

        if line != '':
            self._started = True
        oldlen = len(self._oldline)
        newlen = len(line)
        spaces_needed = oldlen-newlen if oldlen > newlen else 0
        sys.stdout.write('\r'+line[:(self.cols - 1)] + ' ' * spaces_needed)
        sys.stdout.flush()

        # update old line buffer
        self._oldline = line
        self._oldtime = time.time()

    def update(self, line, now=False):
        """Update the line by the given string, replacing the old line.
        The line only gets printed if the line has changed, and if the given
        delay time has been passed. If *now* is *True*, ignore the delay.
        """

        # respect delay time
        if now is False and time.time() - self._oldtime < self.delay:
            return

        # check if line has changed
        if line == self._oldline:
            return

        # ok, then replace the old line by the new one
        self._write(line)

    def end(self):
        """End status line, issue a line break (only if the status line has
        already been used).
        """
        if self._started and not self._ended:
            sys.stdout.write('\n')
            sys.stdout.flush()
        self._ended = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self.end()

    def __del__(self):
        return self.end()

    def reset(self):
        """Reset the status line (make a line break if neccessary and begin a
        new status line).
        """
        self.end()
        self._oldline = ''
        self._started = False
        self._ended = False


class Terminate(object):
    """Trap the TERM signal (15). For example, you can stop an iterative
    algorithm in a controlled way, leaving the loop after the next iteration
    and still saving the results. This is done by sending the TERM signal to
    the process (also possible remotely), i.e. in a Unix shell you can do
    `kill`, followed by the process number, or you can use the program *top*
    to kill the process.

    Note: Works only on Unix-based systems (Linux etc.).
    """

    def __init__(self):
        """Initialize the terminate handler.
        """

        # initialize the flag
        self.terminated = False

        # set up the signal trap
        signal.signal(signal.SIGTERM, self.terminate)

    def terminate(self, signal, frame):
        """If the TERM signal has been received, this method is executed,
        setting the flag to *True*.
        """
        self.terminated = True

    def check(self):
        """Return *True* if a TERM signal has been received, otherwise
        *False*.
        """
        return self.terminated

    def reset(self):
        """Reset the terminate handler, setting the flag back to *False* and
        waiting for a new TERM signal.
        """
        self.terminated = False
        signal.signal(signal.SIGTERM, self.terminate)

    def end(self):
        """Remove the trap. Set the action for the TERM signal back to system
        standard.
        """
        if signal.getsignal(signal.SIGTERM) != signal.SIG_DFL:
            signal.signal(signal.SIGTERM, signal.SIG_DFL)

    def __del__(self):
        """Remove the trap, set action back to system defaults before the
        handler is deleted.
        """
        self.end()

    def __enter__(self):
        """Enable context manager functionality, enter context.
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Leave context.
        """
        self.end()

    def report(self):
        """If this handler was triggered, display a message.
        """
        if self.terminated:
            print('Process has been terminated')


def _nicetime(seconds):
    """Return nice string representation of the given number of seconds in a
    human-readable format (approximated). Example: 3634 s --> 1 h.
    """

    # create list of time units (must be sorted from small to large units)
    units = [{'factor': 1,  'name': 'sec'},
             {'factor': 60, 'name': 'min'},
             {'factor': 60, 'name': 'hrs'},
             {'factor': 24, 'name': 'dys'},
             {'factor': 7,  'name': 'wks'},
             {'factor': 4,  'name': 'mns'},
             {'factor': 12, 'name': 'yrs'}]

    value = int(seconds)
    for unit1, unit2 in zip(units[:-1], units[1:]):
        if value // unit2['factor'] == 0:
            return '%i %s' % (value, unit1['name'])
        else:
            value //= unit2['factor']
    return '%i %s' % (value, unit2['name'])
