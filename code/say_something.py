#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import argparse

from nao_controller import NaoController

def main(nc):

    print("Hello World")

    nc.speak_nao("hello world.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--ballsize", type=float, default=0.06,
                        help="Diameter of ball.")

    args = parser.parse_args()

    print("Connecting to: ", args.ip, ":", args.port)
    nc = NaoController(args.ip, args.port)
    main(nc)
