from src.mdrunner import Model
from enum import Enum, auto


class ModelType(Enum):
    S = auto()
    A = auto()
    B = auto()
    C = auto()
    F = auto()


class S1(Model):
    model_type = ModelType.S

    def init(self):
        """Expecting external input data from runner.add_input()"""
        pass

    def run(self):
        val = self.input.p1 * self.input.p2
        self.add_output(name='x', val=val)


class S2(Model):
    model_type = ModelType.S

    def init(self):
        """Expecting external input data from runner.add_input()"""
        pass

    def run(self):
        pass


class S3(Model):
    model_type = ModelType.S

    def init(self):
        """Expecting external input data from runner.add_input()"""
        self.notify(ModelType.F)

    def run(self):
        self.add_output(name='x', val=self.input.p2 + self.input.p3)


class A1(Model):
    model_type = ModelType.A

    def init(self):
        self.depend_on(ModelType.S)

    def run(self):
        self.add_output(name='x', val=self.S.input.p1 * self.S.input.p2)


class A2(Model):
    model_type = ModelType.A

    def init(self):
        self.depend_on(ModelType.S)
        self.notify(ModelType.F)

    def run(self):
        self.add_output(name='x', val=self.S.input.p2 * self.S.input.p3)


class B1(Model):
    model_type = ModelType.B

    def init(self):
        self.depend_on(ModelType.S)
        self.depend_on(ModelType.A)

    def run(self):
        self.add_output(name='x', val=self.A.output.x * self.S.input.p3)


class B2(Model):
    model_type = ModelType.B

    def init(self):
        self.depend_on(ModelType.S)
        self.depend_on(ModelType.A)
        self.notify(ModelType.F)

    def run(self):
        self.add_output(name='x', val=self.A.output.x * self.S.input.p3)


class B3(Model):
    model_type = ModelType.B

    def init(self):
        self.depend_on(ModelType.S)
        self.depend_on(ModelType.A)
        self.notify(ModelType.F)

    def run(self):
        self.add_output(name='x', val=self.S.output.x + self.A.output.x)


class C3(Model):
    model_type = ModelType.C

    def init(self):
        self.depend_on(ModelType.S)
        self.depend_on(ModelType.A)
        self.depend_on(ModelType.B)
        self.notify(ModelType.F)

    def run(self):
        self.add_output(name='x', val=self.S.input.p3 + self.A.output.x + self.B.output.x)


class F1(Model):
    model_type = ModelType.F

    def init(self):
        """Expecting to be notified by other models"""
        pass

    def run(self):
        # find the sum of all notifying models x values
        x = 0.0
        for model in self.notifying_models:
            if 'x' in model.output.params:
                x += model.output.x
        self.add_output(name='x', val=x)
