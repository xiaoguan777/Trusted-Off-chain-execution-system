<template>
    <div>
        <main class="table">
        <section class="header">
            <h1>去中心化投票系统</h1>
            <div class="input-group">
                <input type="test" placeholder="添加候选人" id="addCandidate">
                <img src="@/assets/images/add.png" @click="addCandidate()">
            </div>
        </section>
        <section class="shell">
            <table>
                <thead>
                    <tr>
                        <th> 序号🌙 </th>
                        <th> 姓名💗</th>
                        <th> 得票数💞</th>
                        <th> 点击投票🥰</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(info,index) in votesReceived" :key="info">
                        <td> {{ index+1 }} </td>
                        <td v-if="index%9==0"> <img src="@/assets/images/lisa.jpg">{{ info[0] }}</td>
                        <td v-else-if="index%9==1"> <img src="@/assets/images/ikun.jpg">{{ info[0] }}</td>
                        <td v-else-if="index%9==2"> <img src="@/assets/images/原神.jpg">{{ info[0] }}</td>
                        <td v-else-if="index%9==3"> <img src="@/assets/images/金珍妮.jpg">{{ info[0] }}</td>
                        <td v-else-if="index%9==4"> <img src="@/assets/images/金智秀.jpg">{{ info[0] }}</td>
                        <td v-else-if="index%9==5"> <img src="@/assets/images/美依礼芽.jpg">{{ info[0] }}</td>
                        <td v-else-if="index%9==6"> <img src="@/assets/images/朴彩英.jpg">{{ info[0] }}</td>
                        <td v-else-if="index%9==7"> <img src="@/assets/images/桥本环奈.jpg">{{ info[0] }}</td>
                        <td v-else-if="index%9==8"> <img src="@/assets/images/张娜英.jpg">{{ info[0] }}</td>
                        <td v-else> <img src="@/assets/images/ikun.jpg">{{ info[0] }}</td>
                        <td :id="getVotingId(info)"> {{ info[1] }} </td>
                        <td>
                            <p class="button" @click="voteForCandidate(info)">为{{ info[0] }}投票</p>
                        </td>
                    </tr>
                </tbody>
            </table>
        </section>
    </main>
    </div>
</template>
<script>
    import voting_artifacts from '../../../build/contracts/Voting.json';
    import poseManager_artifacts from '/home/guanfujun/毕业设计/ETH-Main/build/contracts/PoseManager.json';
    import $ from 'jquery';
    const { Web3 } = require('web3');

    const web3Main=new Web3("HTTP://127.0.0.1:7545");
    // const accountMain = web3Main.eth.accounts.wallet.add('0x09af77e79d7c54cc258016c1c7e1175962a55e65357c04612f5b8a1b6598c353');
    const addressMain = '0xa63c3Bc878DA4E78C989050A045801615a60348e';
    const abiMain=poseManager_artifacts.abi;
    const poseManagerContract = new web3Main.eth.Contract(abiMain, addressMain);
    var contractAddr=[];
    var excuteContractIp=[];
    var privateKey=[];
    var commandIp=[];
    var teeEncryptionKey=[]
    var web3;
    var account;
    const abi=voting_artifacts.abi;
    var votingContract;


    export default{
        name: "IndexView",
        mounted() {
            (async () => {
                    for(var i=5;i<=7;i++){
                        await poseManagerContract.methods.registeredOperators(i).call().then(resp =>{
                        if(Number(resp[0])!=0){
                            excuteContractIp.push(resp[1]);
                            privateKey.push(resp[2]);
                            commandIp.push(resp[3]);
                            teeEncryptionKey.push(resp[4]);
                            contractAddr.push(resp[5])
                        }
                    });
                    }
                    web3=new Web3(excuteContractIp[excuteContractIp.length-1]);
                    account=web3.eth.accounts.wallet.add(privateKey[privateKey.length-1]);
                    votingContract = new web3.eth.Contract(abi,contractAddr[contractAddr.length-1]);

                    await votingContract.methods.candidateNums().call().then(resp=>{
                    this.votingInfo.candidatenums=Number(resp);
                    for(var i=0;i<this.votingInfo.candidatenums;i++){
                        votingContract.methods.candidateList(i).call().then(resp=>{
                            var candidateName=resp;
                            votingContract.methods.totalVotesFor(candidateName).call().then(resp=>{
                                var votingNums=Number(resp);
                                this.votesReceived.set(candidateName,votingNums);
                            })
                        })
                    }
                });
            })();
        },
        data() {
            return{
                votingInfo:{candidatenums:0},
                votesReceived:{}

            }
        },
        created(){
            this.votesReceived=new Map()
        },
        methods: {
            getVotingId: function(info){
                return "voting"+info[0];
            },
            voteForCandidate: function(info){
                votingContract.methods.voteForCandidate(info[0]).send({from:account[0].address, gas:3000000,gasPrice: '20000000000'}).then(resp=>{
                    console.log(resp);
                    votingContract.methods.totalVotesFor(info[0]).call().then(resp=>{
                        var votingNums=Number(resp);
                        $("#"+"voting"+info[0]).html(votingNums);
                    })
                })
                for(var i=0;i<commandIp.length-1;i++){
                    console.log(commandIp[i]+"/check")
                    $.ajax({
                        url : commandIp[i]+"/check",
                        type : "GET",
                        data : {"name":"voteForCandidate"},
                        success : function(res){
                        console.log(res);
                        if(res=="wrong"){
                            alert("请刷新重试")
                        }
                        }
                    }
                    )
                }

            },
            addCandidate: function(){
                var candidateName=$("#addCandidate").val();
                votingContract.methods.addCandidate(candidateName).send({from:account[0].address, gas:3000000,gasPrice: '20000000000'}).then(resp=>{
                    console.log(resp);
                    location.reload();
                })


            }
        }
    }

</script>
<style>
 * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            background: url(@/assets/images/05.png) center / cover;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        main.table {
            width: 77vw;
            height: 80vh;
            background-color: #fff5;
            box-shadow: 0 8px 16px #0005;
            border-radius: 16px;
            overflow: hidden;
        }

        .header {
            width: 100%;
            height: 10%;
            background-color: #fff4;
            padding: 0 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header .input-group {
            width: 35%;
            height: 50%;
            background-color: #fff5;
            padding: 0 20px;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: .2s;
        }

        .header .input-group:hover {
            width: 45%;
            background-color: #fff8;
            box-shadow: 0 5px 40px #0002;
        }

        .header .input-group img {
            width: 20px;
            height: 20px;
        }

        .header .input-group input {
            width: 100%;
            background-color: transparent;
            border: none;
            outline: none;
        }

        .shell {
            width: 95%;
            max-height: calc(90% - 25px);
            background-color: #fffb;
            margin: 8px auto;
            border-radius: 10px;
            overflow: auto;
        }

        .shell::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        table {
            width: 100%;
        }

        td img {
            width: 36px;
            height: 36px;
            margin-right: 10px;
            border-radius: 50%;
            vertical-align: middle;
        }

        table,
        th,
        td {
            border-collapse: collapse;
            padding: 20px;
            text-align: left;
        }

        thead th {
            position: sticky;
            top: 0;
            left: 0;
            background-color: #d5d1defe;
            cursor: pointer;
        }

        /* 偶数行背景色 */
        tbody tr:nth-child(even) {
            background-color: #0000000b;
        }

        tbody tr:hover {
            background-color: #fff6 !important;
        }

        .button {
            padding: 5px 0;
            border-radius: 40px;
            text-align: center;
        }

        tr:nth-child(4n) .button {
            background-color: #86e49d;
            color: #006b21;
        }

        tr:nth-child(4n-1) .button {
            background-color: #ebc474;
        }

        tr:nth-child(4n+1) .button {
            background-color: #d893a3;
            color: #b30021;
        }

        tr:nth-child(4n+2) .button {
            background-color: #6fcaea;
        }
</style>