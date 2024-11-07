from py_trees.behaviour import Behaviour
from py_trees.common import Status
from py_trees.composites import Sequence
from py_trees import logging as log_tree
from  py_trees.display import render_dot_tree
import logging
import time
from pathlib import Path

logging.basicConfig(level=logging.DEBUG,
                    format = "[%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)")

class Action(Behaviour):
    def __init__(self, name:str):
        super(Action, self).__init__(name)

    def setup(self):
        self.logger.debug(f"Action setup {self.name}")
        
    def initialise(self) -> None:
        self.logger.debug(f"Action initialise {self.name}")

    def update(self):
        self.logger.debug(f"Action update {self.name}")
        time.sleep(1)
        return Status.SUCCESS # if random.random() > 0.5 else Status.FAILURE 
        
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
    open_gripper = Action(name="open_gripper")
    close_gripper = Action(name="close_gripper")
    move_to_object = Action(name="move_to_object")
    
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
    bt.tick_once()
    
    
if __name__ == '__main__':
    main()
