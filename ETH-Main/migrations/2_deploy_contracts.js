const PoseManager = artifacts.require("PoseManager");


module.exports = function(deployer) {
  deployer.deploy(PoseManager)
};
