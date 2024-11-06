#include <iostream>
#include <chrono>
#include "behaviortree_cpp/action_node.h"
#include "behaviortree_cpp/bt_factory.h"

using namespace std::chrono_literals;

// find ball

BT::NodeStatus FoundBall(){
    std::cout << "Not found Ball" << std::endl;
    return BT::NodeStatus::FAILURE;
}

class FindBall : public BT::SyncActionNode
{
public:
    explicit FindBall(const std::string &name) : BT::SyncActionNode(name, {})
    {
    }

    BT::NodeStatus tick() override
    {
        std::cout << "Finding Ball: " << this->name() << std::endl;
        std::this_thread::sleep_for(5s);
        std::cout << "Found Ball: " << this->name() << std::endl;
        return BT::NodeStatus::SUCCESS;
    }
};

// move to ball

BT::NodeStatus isBallClose(){
    std::cout << "Ball is not close" << std::endl;
    return BT::NodeStatus::FAILURE;
}

class MoveToBall : public BT::SyncActionNode
{
public:
    explicit MoveToBall(const std::string &name) : BT::SyncActionNode(name, {})
    {
    }

    BT::NodeStatus tick() override
    {
        std::cout << "Moving to Ball: " << this->name() << std::endl;
        std::this_thread::sleep_for(5s);
        std::cout << "Ball is close: " << this->name() << std::endl;
        return BT::NodeStatus::SUCCESS;
    }
};

// grasp ball

BT::NodeStatus isBallGrasped(){
    std::cout << "Ball is not grasped" << std::endl;
    return BT::NodeStatus::FAILURE;
}

class GraspBall : public BT::SyncActionNode
{
public:
    explicit GraspBall(const std::string &name) : BT::SyncActionNode(name, {})
    {
    }

    BT::NodeStatus tick() override
    {
        std::cout << "Grasping Ball: " << this->name() << std::endl;
        std::this_thread::sleep_for(5s);
        std::cout << "Grasped Ball: " << this->name() << std::endl;
        return BT::NodeStatus::SUCCESS;
    }
};

// move to bin

BT::NodeStatus isBinClose(){
    std::cout << "Bin is not close" << std::endl;
    return BT::NodeStatus::FAILURE;
}

class MoveToBin : public BT::SyncActionNode
{
public:
    explicit MoveToBin(const std::string &name) : BT::SyncActionNode(name, {})
    {
    }

    BT::NodeStatus tick() override
    {
        std::cout << "Moving to Bin: " << this->name() << std::endl;
        std::this_thread::sleep_for(5s);
        std::cout << "Bin is close: " << this->name() << std::endl;
        return BT::NodeStatus::SUCCESS;
    }
};

// place ball

BT::NodeStatus isBallPlaced(){
    std::cout << "Ball is not placed" << std::endl;
    return BT::NodeStatus::FAILURE;
}

class PlaceBall : public BT::SyncActionNode
{
public:
    explicit PlaceBall(const std::string &name) : BT::SyncActionNode(name, {})
    {
    }

    BT::NodeStatus tick() override
    {
        std::cout << "Placing Ball: " << this->name() << std::endl;
        std::this_thread::sleep_for(5s);
        std::cout << "Placed Ball: " << this->name() << std::endl;
        return BT::NodeStatus::SUCCESS;
    }
};

// help

class NeedHelp : public BT::SyncActionNode
{
public:
    explicit NeedHelp(const std::string &name) : BT::SyncActionNode(name, {})
    {
    }

    BT::NodeStatus tick() override
    {
        std::cout << "Need Help so waiting for 5 seconds: " << this->name() << std::endl;
        std::this_thread::sleep_for(5s);
        return BT::NodeStatus::SUCCESS;
    }
};

int main(){

    BT::BehaviorTreeFactory factory;

    factory.registerSimpleCondition("FoundBall",std::bind(FoundBall));
    factory.registerNodeType<FindBall>("FindBall");

    factory.registerSimpleCondition("isBallClose",std::bind(isBallClose));
    factory.registerNodeType<MoveToBall>("MoveToBall");

    factory.registerSimpleCondition("isBallGrasped",std::bind(isBallGrasped));
    factory.registerNodeType<GraspBall>("GraspBall");

    factory.registerSimpleCondition("isBinClose",std::bind(isBinClose));
    factory.registerNodeType<MoveToBin>("MoveToBin");

    factory.registerSimpleCondition("isBallPlaced",std::bind(isBallPlaced));
    factory.registerNodeType<PlaceBall>("PlaceBall");

    factory.registerNodeType<NeedHelp>("NeedHelp");
    
    auto tree = factory.createTreeFromFile("./../tree.xml");
    tree.tickWhileRunning();

    return 0;
}
