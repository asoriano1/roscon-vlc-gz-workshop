#!/usr/bin/env python3
"""Un slider para girar el mástil del mast_bot, como los de joint_state_publisher_gui.

Publica el ángulo en mast_controller/commands (std_msgs/Float64MultiArray), el topic del
JointGroupPositionController del ejercicio 3: hace lo mismo que el `ros2 topic pub`, cada vez
que se mueve el slider.

  ros2 run mini_bot mast_slider.py
  ros2 run mini_bot mast_slider.py --ros-args -r __ns:=/robot_b     # un robot con namespace
"""
import tkinter as tk

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

LIMIT = 1.57  # los límites de mast_joint en el xacro (±90°)


class MastSlider(Node):

    def __init__(self):
        super().__init__('mast_slider')
        # Sin barra: relativo al namespace, como el resto de nodos del robot.
        self.pub = self.create_publisher(Float64MultiArray, 'mast_controller/commands', 10)

    def send(self, angle):
        self.pub.publish(Float64MultiArray(data=[angle]))


def main():
    rclpy.init()
    node = MastSlider()

    root = tk.Tk()
    root.title('mast_joint')
    topic = node.pub.topic_name
    tk.Label(root, text=f'Publica en {topic}').pack(padx=10, pady=(10, 0))
    angle = tk.DoubleVar(value=0.0)
    tk.Scale(root, variable=angle, from_=-LIMIT, to=LIMIT, resolution=0.01, orient='horizontal',
             length=400, label='mast_joint (rad)',
             command=lambda value: node.send(float(value))).pack(padx=10)
    tk.Button(root, text='Centrar', command=lambda: (angle.set(0.0), node.send(0.0))).pack(pady=10)

    # El nodo solo publica: no necesita spin. Se cierra con la ventana o con Ctrl+C en la
    # terminal; cada 200 ms se mira si ROS 2 sigue vivo, por si lo ha apagado otro.
    def watch():
        if rclpy.ok():
            root.after(200, watch)
        else:
            root.destroy()

    watch()
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
