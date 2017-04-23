class InstallationProgressStep(object):
    def __init__(self, target, start, approx_progress=None):
        assert isinstance(start, bool)
        assert approx_progress is None or isinstance(approx_progress, (int, float)) and 0 <= approx_progress <= 1
        self.target = target
        self.start = start
        self.approx_progress = approx_progress

    @property
    def percentage(self):
        assert self.approx_progress != None
        return int(self.approx_progress * 100)

    @property
    def message(self):
        msg = "Installing {}... ".format(self.target.name) if self.start else "done\n"
        return msg
