def pedPresense(pin,board,pedcount):
    board.set_pin_mode_digital_input(8)
    pedcount = 0
    try:
        time.sleep(0.75)
        while True:
            value = board.digital_read(8)
            if value[0] == 0:
                pedcount += 1
                time.sleep(0.25)
                return pedcount
    except KeyboardInterrupt:
            board.shutdown()
