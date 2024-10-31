from robotComms.robotComms import robotComms as Comms


def main():
    r1 = Comms(console_logging=True, run_remote_url=True, remote_url="10.168.1.103")
    #    print(r1.system.get_capabilities())
    #    print(r1.system.get_power_status())
    #    print(r1.system.get_robot_info())
    #    print(r1.system.get_robot_health())
    #    print(r1.system.get_system_parameters("max_s"))
    #    print(r1.system.get_system_parameters("max_w"))
    #    print(r1.system.get_system_parameters("dock"))
    #    print(r1.system.set_robot_max_linear_speed(0.1))
    #    print(r1.system.set_robot_max_angular_velocity(0.1))
    #    print(r1.system.set_robot_emergency_brake(False))
    #    print(r1.system.set_robot_brake_release(False))
    #    print(r1.system.get_network_status())
    #    print(r1.system.get_raw_adc_imu_value())
    #    print(r1.system.get_raw_calculated_imu_value())
    #    print(
    #        r1.system.set_robot_lights(
    #            "Two", "Right", "AlwaysBright", (255, 0, 0), (0, 255, 0), 1, 1
    #        )
    #    )
    #    print(r1.system.set_power_status("hibernate"))
    print(r1.artifact.get_artifact("lines"))
    print(r1.artifact.get_artifact("lines", "track"))
    print(r1.artifact.get_artifact("lines", "tracks"))
    print(r1.artifact.get_artifact("lines", "walls"))
    print(r1.artifact.get_artifact("rect"))
    print(r1.artifact.get_artifact("rect", "forbidden_area"))
    print(r1.artifact.get_artifact("poi"))
    print(r1.artifact.get_artifact("poi", "update"))
    print(r1.artifact.get_artifact("laser"))
    print(r1.artifact.get_artifact("laser", "update"))


if __name__ == "__main__":
    main()
