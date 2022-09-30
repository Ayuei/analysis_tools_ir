import tempfile


class DummyFile:
    def __init__(self):
        self.curr = 0
        self.internal = []
        self.tempfile = None

    def readlines(self):
        return self.internal

    def read(self):
        return "\n".join(self.internal)

    def write(self, line):
        self.internal.append(line)

    def __iter__(self):
        self.curr = 0
        return self

    def __next__(self):
        x = self.internal[self.curr]
        if self.curr >= len(self.internal):
            raise StopIteration

        self.curr += 1

        return x

    @classmethod
    def from_list(cls, lst) -> "DummyFile":
        obj = cls()
        obj.internal = lst

        return obj

    def serialize(self):
        if self.tempfile:
            self.tempfile.close()
            self.tempfile = None

        self.tempfile = tempfile.NamedTemporaryFile()

        for line in self.internal:
            self.tempfile.write(f"{line}\n")

        self.tempfile.flush()

        return self.tempfile.name
