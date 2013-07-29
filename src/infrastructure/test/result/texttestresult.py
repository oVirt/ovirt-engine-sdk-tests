'''
Created on May 26, 2013

@author: mpastern
'''

# from src.test.testresult import TestResult
#
# class TextTestResult(TestResult):
#     def __init__(self, *args, **kwargs):
#         result.TextTestResult.__init__(self, *args, **kwargs)
#         self._last_case = None
#
#     def getDescription(self, test):
#         return str(test)
#
#     def _writeResult(self, test, long_result, color, short_result, success):
#         if self.showAll:
#             colorWrite(self.stream, long_result, color)
#             self.stream.writeln()
#         elif self.dots:
#             self.stream.write(short_result)
#             self.stream.flush()
#
#     def addSuccess(self, test):
#         unittest.TestResult.addSuccess(self, test)
#         self._writeResult(test, 'OK', TermColor.green, '.', True)
#
#     def addFailure(self, test, err):
#         unittest.TestResult.addFailure(self, test, err)
#         self._writeResult(test, 'FAIL', TermColor.red, 'F', False)
#
#     def addSkip(self, test, reason):
#         # 2.7 skip compat
#         from nose.plugins.skip import SkipTest
#         if SkipTest in self.errorClasses:
#             storage, label, isfail = self.errorClasses[SkipTest]
#             storage.append((test, reason))
#             self._writeResult(test, 'SKIP : %s' % reason, TermColor.blue, 'S',
#                               True)
#
#     def addError(self, test, err):
#         stream = getattr(self, 'stream', None)
#         ec, ev, tb = err
#         try:
#             exc_info = self._exc_info_to_string(err, test)
#         except TypeError:
#             # 2.3 compat
#             exc_info = self._exc_info_to_string(err)
#         for cls, (storage, label, isfail) in self.errorClasses.items():
#             if result.isclass(ec) and issubclass(ec, cls):
#                 if isfail:
#                     test.passed = False
#                 storage.append((test, exc_info))
#                 # Might get patched into a streamless result
#                 if stream is not None:
#                     if self.showAll:
#                         message = [label]
#                         detail = result._exception_detail(err[1])
#                         if detail:
#                             message.append(detail)
#                         stream.writeln(": ".join(message))
#                     elif self.dots:
#                         stream.write(label[:1])
#                 return
#         self.errors.append((test, exc_info))
#         test.passed = False
#         if stream is not None:
#             self._writeResult(test, 'ERROR', TermColor.red, 'E', False)
#
#     def startTest(self, test):
#         unittest.TestResult.startTest(self, test)
#         current_case = test.test.__class__.__name__
#
#         if self.showAll:
#             if current_case != self._last_case:
#                 self.stream.writeln(current_case)
#                 self._last_case = current_case
#
#             self.stream.write(
#                 '    %s' % str(test.test._testMethodName).ljust(60))
#             self.stream.flush()
