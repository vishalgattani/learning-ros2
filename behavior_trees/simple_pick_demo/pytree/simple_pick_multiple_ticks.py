from py_trees.behaviour import Behaviour
from py_trees.common import Status
from py_trees.composites import Sequence
from py_trees import logging as log_tree
import logging
import time
from  py_trees.display import render_dot_tree
from pathlib import Path

logging.basicConfig(level=logging.DEBUG,
                    format = "[%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)")

class Action(Behaviour):
    def __init__(self, name:str,max_ticks:int=10):
        super(Action, self).__init__(name)
        self.max_ticks = max_ticks
        self.total_ticks_remaining = self.max_ticks

    def setup(self):
        self.logger.debug(f"Action setup {self.name}")
        
    def initialise(self) -> None:
        self.total_ticks_remaining = self.max_ticks
        self.logger.debug(f"Action initialise {self.name}")

    def update(self):
        self.total_ticks_remaining -= 1
        self.logger.debug(f"Action update {self.name}")
        time.sleep(1)
        return Status.SUCCESS if self.total_ticks_remaining == 0 else Status.RUNNING
        
    def terminate(self, new_status: Status) -> None:
        self.logger.debug(f"Action terminate {self.name} to {new_status.name}")
        
class Condition(Behaviour):
    def __init__(self, name:str):
        super(Condition, self).__init__(name)

    def setup(self):
        self.logger.debug(f"Condition setup {self.name}")

    def initialise(self) -> None:
        self.logger.debug(f"Condition initialise {self.name}")

    def update(self):
        self.logger.debug(f"Condition update {self.name}")
        time.sleep(1)
        return Status.SUCCESS 

    def terminate(self, new_status: Status) -> None:
        self.logger.debug(f"Condition terminate {self.name} to {new_status.name}")
        
def create_tree():
    logging.info("Creating behaviour tree")
    root = Sequence(name="sequence",memory=True)
    check_battery = Condition(name="check_battery")
    open_gripper = Action(name="open_gripper",max_ticks=2)
    close_gripper = Action(name="close_gripper",max_ticks=3)
    move_to_object = Action(name="move_to_object",max_ticks=5)
    
    root.add_children(
        [
            check_battery,
            open_gripper,
            move_to_object,
            close_gripper
        ]
    )
    return root


def main():
    log_tree.level = log_tree.level.DEBUG
    logging.info("Simple Pick Demo")
    bt = create_tree()
    render_dot_tree(root=bt,target_directory=Path(__file__).parent,name=Path(__file__).name)
    for _ in range(20):
        try:
            logging.debug(f"Ticking {bt.name} #{_}")
            bt.tick_once()
            time.sleep(0.1)
        except KeyboardInterrupt:
            logging.warning("Keyboard interrupt")
            break
    
    
if __name__ == '__main__':
    main()
