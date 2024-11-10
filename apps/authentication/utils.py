from threading import Thread

class EmailSendThread(Thread):
    def __init__(self, email_obj):
        Thread.__init__(self)
        self.email_obj = email_obj
    def run(self) -> None:
        self.email_obj.send()
        return super().run()    
