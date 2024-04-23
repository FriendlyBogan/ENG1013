def pedPresence(pin,board,pedcount):
    board.set_pin_mode_digital_input(pin)
    try:
        value = board.digital_read(pin)
        if value[0] == 0:
            pedcount += 1
        return pedcount
    except KeyboardInterrupt:
            board.shutdown()