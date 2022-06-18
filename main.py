#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.

## 走行体の設定
color_sensor= ColorSensor(Port.S3)          # カラーセンサー定義
ultra_sensor = UltrasonicSensor(Port.S1)    # 超音波センサー定義
left = Motor(Port.B)                        # ２輪走行体用左モーター定義
right = Motor(Port.C)                       # ２輪走行体用右モーター定義
robot = DriveBase(left, right, 55, 135)     # 長さの単位は mm
"""
DriveBase クラス
- 第１引数: 左モーター
- 第２引数: 右モーター
- 第３引数: タイヤの直径 [mm]
- 第４引数: 車幅 [mm] (車体の回転径)
"""

## 走行開始
ev3.speaker.beep()          # ビープ音を鳴らす

# robot.turn(360)             # その場で 360 度旋回（いわゆる小回り）


## 関数定義

def onoff_operation(middle, speed, turn_rate, stop_color):
    while not color_sensor.color() == Color.RED:    # 測った色が赤じゃない限りループ
        if middle < color_sensor.reflection():      # 目標値よりも反射光の大きさが大きいなら
            robot.drive(speed, turn_rate)           # DriveBase の drive() メソッドがステアリングオン
            """
            drive メソッド
            - 第１引数: スピード
            - 第２引数: 曲がる強さ
            """
        else:
            robot.drive(speed, -1*turn_rate)
    robot.stop()
    
def p_operation(middle, power, pgain, stop_distance):
    """
    Variables:
    - middle: ライントレースの目標値
    - power: 進む速さ
    - pgain: P gain
    - stop_distance: 超音波センサーを使って止まる距離
    """
    while stop_distance < ultra_sensor.distance():  # stop_distance より今の距離が遠いなら続ける
        turn_rate = ( color_sensor.reflection() - middle) * pgain   # 曲がる大きさを計算する
        robot.drive(power, turn_rate)
    robot.stop()                                    # while ループを抜けるとロボットを停止する
        
def p_operation_color(middle, power, pgain, stop_color):
    while not color_sensor.color() == Color.RED:
        turn_rate = ( color_sensor.reflection() - middle) * pgain
        robot.drive(power, turn_rate)
    robot.stop()

def p_operation_distance(middle, power, pgain, stop_length):
    while stop_length < ultra_sensor.distance():
        turn_rate = (color_sensor.reflection() - middle) * pgain
        robot.drive(power, turn_rate)
    robot.stop()

## 走行開始

onoff_operation(40, 100, 50, Color.RED)     # 定義した関数を実行する

robot.straight(200)                         # 単位: mm
robot.straight(-200)
robot.turn(180)

p_operation(40, 30, 1.0, 100)