import React from "react";
import { List, Button, Modal, Input } from "antd"
import axios from "axios"
import { CustomerServiceOutlined, EnterOutlined } from "@ant-design/icons";
import { RobotItem } from "chatbot-antd/dist/listItem"
import "antd/dist/antd.min.css";
export default class DSLBot extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            modalOpen: false,  // 客服机器人窗口是否打开
            msgList: [],  // 呈现在聊天框里的消息列表
            inputValue: "",  // 当前输入框中的内容
            status: "_START_", // 客户端当前状态
            varList: {},  // 客户端变量表
            timerID: -1  // 客户端当前计时器ID
        };
    }

    /**
     * @description: 处理页面上的客服按钮点击事件，本质是一次特殊的getDslResp
     * @return {*}
     */
    handleClick = () => {
        if (this.state.status === "_START_") {
            axios.get("http://127.0.0.1:8000/dsl",{
                params: {
                    status: this.state.status,
                    message: "Hello server!"
                },
            }).then(result => this.handleResponse(result))
        }
        this.setState({ modalOpen: true })
    }

    /**
     * @description: 处理按下回车键发送消息之后的函数
                     1. 将输入框清空
                     2. 将"_text_"的值赋为输入框的字符串
                     3. 将用户消息添加到消息列表
                     4. 将用户消息发送到服务端请求回复
                     5. 调用handleResponse函数处理回复
     * @return {*}
     */
    getDslResp = () => {
        let inputBox = document.getElementById("inputBox");
        if (!inputBox.value)
            return;
        let tmpList = this.state.varList
        for (let v in tmpList)
            if (tmpList[v] === "_text_")
                tmpList[v] = inputBox.value
        this.setState({
            varList: tmpList
        })

        axios.get("http://127.0.0.1:8000/dsl", {
            params: {
                status: this.state.status,
                message: inputBox.value
            }
        }).then(result => this.handleResponse(result))

        this.setState({
            msgList: [
                ...this.state.msgList,
                { isUser: true, content: inputBox.value }
            ],
            inputValue: ""
        })

    }

    /**
     * @description: 处理从后端得到的应答
     *               1. 更新this.state.varList中变量的值
     *               2. 用变量表里的值替换回复的字符串中的占位符
     *               3. 将处理完毕的字符串添加到消息列表中
     *               4. 设定计时器
     *               5. 在计时器触发后向后端发送超时信息，并回调自身处理应答
     * @param {*} response 从后端得到的应答
     * @return {*}
     */
     handleResponse = (response) => {
        setTimeout(() => {  // 设置500ms的延迟，让机器人回复自然一些
            let newVarList = this.state.varList
            for (let k in response.data.var){
                newVarList[k] = response.data.var[k]
            }
            this.setState({
                status: response.data.status,
                varList: newVarList
            })
            if (response.data.message) {
                let mes = response.data.message
                for (let v in this.state.varList)
                    mes = mes.replace(v, this.state.varList[v])
                this.setState({
                    msgList: [
                        ...this.state.msgList,
                        { isUser: false, content: mes }
                    ]
                })
            }
            if (this.state.timerID !== -1)
                clearTimeout(this.state.timerID)
            if (response.data.wait >= 0) {
                let _timerID = setTimeout(() => {
                    axios.get("http://127.0.0.1:8000/dsl", {
                        params:{
                            status: this.state.status,
                            message: "!!!timeout"
                        }
                    }).then(result => this.handleResponse(result))
                }, response.data.wait * 1000)
                this.setState({ timerID: _timerID })
            }
        }, 500)
    }

    /**
     * @description: 每次消息列表更新时，把滚动条移动到最下方
     * @return {*}
     */
    componentDidUpdate() {
        let msgBox = document.getElementById("msgBox");
        if (msgBox)
            msgBox.scrollTop = msgBox.scrollHeight - 400;
    }

    /**
     * @description: 每次用户更新输入框的内容时，更新inputValue
     * @param {*} event 用户输入事件
     * @return {*}
     */
    keyUp = (event) => {
        this.setState({
            inputValue: event.target.value
        })
    }

    render() {
        return (
            <div>
                <div
                    style={{
                        position: "fixed",
                        right: "10px",
                        top: "40%",
                    }}
                >
                    {/* 显示在网页上的按钮 */}
                    <Button type="primary" onClick={() => this.handleClick()}>
                        <CustomerServiceOutlined></CustomerServiceOutlined>
                    </Button>

                    {/* 客服窗口 */}
                    <Modal
                        id="modalWin"
                        open={this.state.modalOpen}
                        onCancel={() => this.setState({ modalOpen: false })}
                        // 对话框的脚部是一个输入框
                        footer={
                            <Input id="inputBox" suffix={<EnterOutlined />}
                                onPressEnter={() => this.getDslResp()}
                                onChange={this.keyUp}
                                value={this.state.inputValue}
                            ></Input>
                        }
                        title="DSL机器人"
                        wrapClassName="dslMod"
                    >
                        {/*对话框的内容是一个列表*/}
                        <List id="msgBox"
                            split={false}
                            dataSource={this.state.msgList}
                            itemLayout="horizontal"
                            style={{
                                height: 400,
                                overflow: 'scroll',
                            }}
                            renderItem={item => (
                                <List.Item style={item.isUser ?
                                    { justifyContent: "flex-end", padding: "12px 10px" } :
                                    { justifyContent: "flex-start", padding: "12px 10px" }}>
                                    <RobotItem isUser={item.isUser} text={item.content}></RobotItem>
                                </List.Item>
                            )}>
                            {/*实时呈现this.state.msgList中的内容，通过this.handleResponse()函数更新*/}
                        </List>
                        <span id="msgEnd" style={{ overflow: "hidden" }}></span>
                    </Modal>
                </div>
            </div>
        );
    }
}