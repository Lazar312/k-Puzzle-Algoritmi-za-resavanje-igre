import numpy

class Heuristic:
    def get_evaluation(self, state):
        pass


class ExampleHeuristic(Heuristic):
    def get_evaluation(self, state):
        return 0


class HammingHeuristic(Heuristic):
    def get_evaluation(self, state):
        j = 1
        sum = 0
        for i in range(len(state)):
            if state[i] == 0:
                j += 1
                continue
            if state[i] != j:
                sum += 1
            j += 1
        return sum


class ManhattanHeuristic(Heuristic):
    def get_evaluation(self, state):
        sum = 0
        lenght = len(state)
        n = int(numpy.sqrt(lenght))
        m = n - 1
        for i in range(0, lenght):
            if state[i] == 0:
                continue
            else :
                temp = (state[i] - 1)
                sum += abs(int(i / n) - int(temp / n)) + abs(i % n - (temp % n))

        return sum

