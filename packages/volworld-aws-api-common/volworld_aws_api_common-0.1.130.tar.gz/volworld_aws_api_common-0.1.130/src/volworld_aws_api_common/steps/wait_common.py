from behave import *
import time
from volworld_common.test.behave.BehaveUtil import BehaveUtil


def waiting_for_animation():
    time.sleep(0.5)


@when('waiting animation')
def when_waiting_animation(c):
    time.sleep(0.5)


@when('waiting animation for {sec} sec')
def when_waiting_animation_for_sec(c, sec: str):
    time.sleep(BehaveUtil.clear_float(sec))


@when('sleep for {sec} sec')
def when_sleep(c, sec: str):
    time.sleep(BehaveUtil.clear_float(sec))


@when('waiting server update for {sec} sec')
def when_waiting_server_update(c, sec: str):
    time.sleep(BehaveUtil.clear_float(sec))