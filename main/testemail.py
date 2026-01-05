from emailer import send_error_email, send_water_event_msg



if __name__ == "__main__":
    send_water_event_msg(isubject="Test Subject", ipt="Test Text")