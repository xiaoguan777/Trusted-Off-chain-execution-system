// SPDX-License-Identifier: MIT
pragma solidity^ 0.8.17;
contract Voting{
    mapping (string=>uint8)public votesReceived;
    string[] public candidateList;
    string[] public data;
    uint public sum=0;

    constructor(string[] memory candidateName) {
        candidateList=candidateName;
    }

    //查看某个候选人的票数
    function totalVotesFor(string  memory candidate)view public returns(uint8){
        return votesReceived[candidate];
    }

    //为某个候选人投票
    function  voteForCandidate(string memory candidate)public  {
        data.push(candidate);
        sum++;
        votesReceived[candidate]+=1;
    }

    //添加候选人
    function addCandidate(string memory candidate) public {
        candidateList.push(candidate);
    }
    function candidateNums() view public returns(uint256){
        return candidateList.length;

    }

}
