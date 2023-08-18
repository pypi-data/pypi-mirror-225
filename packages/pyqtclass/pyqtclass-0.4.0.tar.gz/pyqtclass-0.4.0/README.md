# PyQtClasses
PyQt 기반으로 동작하는 'Worker 객체' 들의 베이스클래스 제공.

WorkerSchedule 테이블 정보를 기반으로 MainApp, SubApp, Worker 의 동작시간을 제어할 수 있음.


### WorkerSchedule 테이블 예시

![Alt text](<Docs/files/WorkerSchedule 테이블 예시.png>)

#### 스키마 설명

    worker: Worker Class Name (string)
    stime: Start Time (string)
    etime: End Time (string)
    interval: Interval Time (seconds)
    env: Python Environment (string)
    batch: 배치 실행 여부 (boolean)
    desc: 상세설명 (string)

