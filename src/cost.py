class Cost:
    def __init__(self, input_token, input_cost, output_token, output_cost):
        self.input_token = input_token
        self.input_cost = input_cost
        self.output_token = output_token
        self.output_cost = output_cost
        self.total_cost = input_cost+output_cost
