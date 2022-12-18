from src.status_warehouse.Simulate_Events.action import Action


class MoveDrawer(Action):
    # override
    def simulate_action(self):
        print("Test")
