# -*- coding: utf-8 -*-
import re
from time import sleep
from datetime import datetime, timedelta


from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, QThread


from ipylib.idebug import *
from ipylib import idatetime



__all__ = [
    'QBaseObject',
    'QBaseWorker',
    'ThreadGenerator',
    'ThreadMDB',
]



class QBaseObject(QObject):
    # 용어정의
    # - 객체 생성: __init__() --> None
    # - 객체 종료/파괴: 파이썬이 알아서 해준다
    # - 작업시작: start/run() --> started.emit [작업(시작시퀀스)완료]
    # - 작업종료: close/stop/quit/exit() --> closed/stopped/finished
    # - 작업중지: pause() --> paused.emit
    # 서브작업완료의 경우 보다 상세한 시그널명을 사용하라

    finished = pyqtSignal()
    closed = pyqtSignal() # finished 로 통일하라
    stopped = pyqtSignal() # finished 로 통일하라
    started = pyqtSignal() # 가끔 필요한 경우도 있다
    completed = pyqtSignal() # 보다 작은 작업 수준에서 작업완료시 사용하라
    initiated = pyqtSignal() # 초기화 작업 완료
    """이하 기본함수들은 '복붙'해서 사용해야 로깅이 정확하게 된다"""

    def __init__(self):
        super().__init__()
        self._finish_called = False
        self._timerList = []
    
    def finish(self, *args): 
        self.stop_alltimers()
        self.finished.emit()

    # @ctracer
    def start_timer(self, key, func, sec):
        try:
            timer = getattr(self, key)
        except Exception as e:
            timer = QTimer()
            timer.timeout.connect(func)
            setattr(self, key, timer)
        finally:
            timer.start(1000 * sec)
            if key not in self._timerList: 
                self._timerList.append(key)
            self._timerList = list(set(self._timerList))
            logger.debug(['타이머리스트(등록)', self._timerList])
    
    # @ctracer
    def stop_timer(self, key):
        try: 
            timer = getattr(self, key)
        except Exception as e: 
            pass
        else:
            while timer.isActive():
                timer.stop()
                sleep(0.1)
            self._timerList = list(set(self._timerList))
            if key in self._timerList: 
                self._timerList.remove(key)
            logger.debug(['타이머리스트(해제)', self._timerList])
    
    # @ctracer
    def stop_alltimers(self):
        for k in self._timerList: 
            self.stop_timer(k)

"""스케쥴로 움직이는 단독스레드형 객체"""
class QBaseWorker(QBaseObject):

    # @ctracer
    def __init__(self, func, stime=None, etime=None, interval=60):
        super().__init__()
        self._isRunning = False
        self.__exec_func__ = func
        self.stime = stime
        self.etime = etime
        self.sdt = idatetime.DatetimeParser(stime)
        self.edt = idatetime.DatetimeParser(etime)
        self._interval = interval
    
    # @ctracer
    def finish(self, *args):
        self.stop_alltimers()
        super().finish()
    
    # @ctracer
    def run(self):
        if self.stime is None:
            self.__exec_run__()
        else:
            self.start_timer('__WorkerRuntimeCheckTimer', self.__check_runtime__, self._interval)
            self.__check_runtime__()
    
    # @ctracer
    def __check_runtime__(self):
        t = datetime.now().astimezone()
        if t < self.sdt: 
            pass
        elif self.sdt <= t <= self.edt:
            if self._isRunning: 
                pass
            else: 
                self.__exec_run__()
        else: 
            self.finish('동작시간종료', {'stime':self.stime, 'etime':self.etime})
    
    # @ctracer
    def __exec_run__(self):
        self._isRunning = True
        self.__exec_func__()


class ThreadGenerator(QBaseObject):

    terminated = pyqtSignal(str)

    # @ctracer
    def __init__(self, qobject, func='run', *args, **kwargs):
        super().__init__()

        self.obj = qobject(*args, **kwargs) if callable(qobject) else qobject
        self.__exec__ = getattr(self.obj, func)
        self.name = self.obj.__class__.__name__

        """ 
        [중요!]
        시작시: Generator.start() -> thread.start() -> 객체시작
        종료시: 객체종료 -> thread.quit() -> Generator.finish() -> Generator._terminate()
        """
        self.thread = QThread()
        self.obj.moveToThread(self.thread)
        self.thread.started.connect(self.__exec__)
        self.obj.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.finish)

        """
        아래코드를 사용하지 말고, 직접 삭제처리하라
        사용시 에러발생확률이 커진다
        
        self.thread.finished.connect(self.thread.deleteLater)
        self.obj.finished.connect(self.obj.deleteLater)
        """
    
    # @ctracer
    def finish(self, *args):
        super().finish()
        self._terminate()

    # @ctracer
    def start(self): 
        self.thread.start()
    
    def set_workerId(self, id): 
        self.wid = str(id)
    
    # @ctracer
    def _terminate(self):
        # logger.info([self.thread.isRunning(), self.thread.isFinished()])
        try: 
            self.terminated.emit(self.wid)
        except Exception as e: 
            pass


"""스레드워커를 관리하는 메모리DB"""
class ThreadMDB(QBaseObject):
    def __init__(self, datanm=None):
        super().__init__()
        self.__datanm__ = '스레드관리MDB' if datanm is None else datanm
        self.keys = []
    
    @ctracer
    def set_n_run(self, k, o):
        if k in self.keys: 
            pass
        else:
            worker = o if isinstance(o, ThreadGenerator) else ThreadGenerator(o)
            worker.set_workerId(k)
            worker.terminated.connect(self._unset_terminated_worker)
            self.keys.append(k)
            setattr(self, k, worker)
            self._report({'등록':k})
            worker.start()
    
    @ctracer
    @pyqtSlot(str)
    def _unset_terminated_worker(self, k):
        try: 
            w = getattr(self, k)
        except Exception as e: 
            pass
        else:
            self.keys.remove(k)
            delattr(self, k)
            self._report({'제거':k})
    
    def _report(self, *args):
        logger.debug([self.__datanm__, args, len(self.keys), self.keys])


