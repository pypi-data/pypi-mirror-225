# TO DO

- write variant of Converge or extend Converge to use standard error as criterion


## Bar

- multiple progress bars at once, to show status of multiple subprocesses
- allow nested progress bars, passing and multiplying step numbers to the
  inner-next instance
- report elapsed time instead of printing "ETC 0 sec"
- save start and end times (and duration), to check them later"""


## Monitor

- support complex numbers


## OpenBar

- implement the class
- go beyond linear extrapolation


## Abort

- enable key combinations (e.g., CTRL+q)
- enable special keys (e.g., ESC)


## Until

- define word "next", excluding the present day, to allow something
  like "next tuesday" ==> even if it is tuesday right now, run until
  next tuesday
- document the syntax for specifying dates and durations


## Converge

- choose from various convergence criterions (also based on standard
  error)
- could choose from mean, gmean, min, max, max-min (peak-to-peak), ...
  (find more under http://en.wikipedia.org/wiki/Average)
- offer relative and absolute versions of each criterion
- let the user specify his own criterion (as a function object)
- use Cython, write version that is callable from C, support OpenMP
- add feature to remember several values (e.g., 5) and check that all the
  deltas are small enough (then, it is not enought that "by chance" the
  delta value drops below the tolerance)"""
