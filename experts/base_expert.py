


class BaseExpert(object):

    def __init__(self, name, description, model):
        self.name = name
        self.description = description
        self.model = model

    def forward(self):
        pass

    def backward(self):
        pass

    def __str__(self):
        return f'{self.name}: {self.description}'
