class CustomProtocol:

    def __init__(self, floor, room, id, devices, onChange, onOff, onOn):
        self.floor = floor
        self.room = room
        self.id = id
        self.devices = devices
        self.onChange = onChange
        self.onOff = onOff
        self.onOn = onOn

    def match(self, command):

        if command[0] != self.floor and command[0] != "*":
            print(command[0], self.floor)
            return False

        if command[1] != self.room and command[1] != "*":
            return False

        if command[2] != self.id and command[2] != "*":
            return False

        return True

    def execute(self, command):
        if command[3] == "*":
            for d in self.devices:
                self.operation(command, d)
        else:
            self.operation(command, command[3])

    def operation(self, command, device):
        if command[4] == "change":
            print("execute on with", device)
            self.onChange(device)
        if command[4] == "off":
            print("execute on with", device)
            self.onOff(device)
        if command[4] == "on":
            print("execute on with", device)
            self.onOn(device)
