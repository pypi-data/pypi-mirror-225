import logging
from contextlib import contextmanager
from threading import Thread

import time_machine

from snsary import system
from snsary.outputs import MockOutput
from snsary.sources import MockSensor, MultiSource
from tests.conftest import retry


@contextmanager
def tmp_app(*, sensors=[], outputs=[]):
    try:
        MultiSource(*sensors).stream.into(*outputs)
        system.start()
        yield
        system.stop()
    finally:
        system.clear_services()


def test_system(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor(period_seconds=1)]
    outputs = [MockOutput(), MockOutput(index=1)]

    def first_assertions():
        assert "INFO - [snsary] Started." in caplog.text
        assert "INFO - [snsary.mocksensor-0] Collected 1 readings." in caplog.text
        assert "INFO - [snsary.mockoutput-0] Reading: <abc 1650885071 0>" in caplog.text
        assert "INFO - [snsary.mockoutput-1] Reading: <abc 1650885071 0>" in caplog.text

    def second_assertions():
        assert "INFO - [snsary.mockoutput-0] Reading: <abc 1650885072 1>" in caplog.text
        assert "INFO - [snsary.mockoutput-1] Reading: <abc 1650885072 1>" in caplog.text

    def end_assertions():
        assert "INFO - [snsary] Stopping." in caplog.text
        assert "INFO - [snsary] Bye." in caplog.text
        assert "ERROR" not in caplog.text

    with time_machine.travel("2022-04-25T12:11:11+01:00", tick=False) as frozen_time:
        with tmp_app(sensors=sensors, outputs=outputs):
            retry(first_assertions)
            frozen_time.shift(1)
            retry(second_assertions)

    retry(end_assertions)


def test_failing_sensor(caplog):
    sensors = [MockSensor(fail=True, period_seconds=1)]

    def assertions():
        assert "ERROR - [snsary.mocksensor-0] problem-1" in caplog.text
        assert "ERROR - [snsary.mocksensor-0] problem-2" in caplog.text

    with tmp_app(sensors=sensors):
        retry(assertions)


def test_failing_output(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor(period_seconds=1)]
    outputs = [MockOutput(fail=True)]

    def assertions():
        assert "INFO - [snsary.mocksensor-0] Collected 1 readings." in caplog.text
        assert "ERROR - [snsary.mockoutput-0] problem-1" in caplog.text
        assert "ERROR - [snsary.mockoutput-0] problem-2" in caplog.text

    with tmp_app(sensors=sensors, outputs=outputs):
        retry(assertions)


def test_stuck_sensor_service(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor(hang=True), MockSensor(index=1)]

    def assertions():
        assert "INFO - [snsary.mocksensor-1] Collected 1 readings." in caplog.text
        assert "INFO - [snsary.mocksensor-0] Collected 1 readings." not in caplog.text

    with tmp_app(sensors=sensors):
        retry(assertions)

    def end_assertions():
        assert "ERROR - [snsary.mocksensor-0] Failed to stop." in caplog.text

    retry(end_assertions)


def test_stuck_output_async(caplog):
    caplog.set_level(logging.INFO)
    sensors = [MockSensor()]
    outputs = [MockOutput(hang=True), MockOutput(index=1)]

    def assertions():
        assert "INFO - [snsary.mockoutput-1] Reading" in caplog.text
        assert "INFO - [snsary.mockoutput-0] Reading" not in caplog.text

    with tmp_app(sensors=sensors, outputs=outputs):
        retry(assertions)

    def end_assertions():
        assert "Bye." in caplog.text
        assert "ERROR" not in caplog.text

    retry(end_assertions)


def test_wait_stop():
    thread = Thread(
        target=lambda: system.wait(handle_signals=False),
        daemon=True,
    )

    thread.start()
    thread.join(timeout=0.1)
    assert thread.is_alive()

    system.stop()
    thread.join(timeout=0.1)
    assert not thread.is_alive()
