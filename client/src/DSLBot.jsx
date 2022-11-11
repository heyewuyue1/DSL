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
            token: "",  // 当前用户Token
            timerID: -1
        };
    }

    handleClick = () => {
        if (!this.state.token) {
            axios.get("http://127.0.0.1:8000/token").then(result => {
                if (result.data.message) {
                    this.setState({
                        token: result.data.token,
                        msgList: [
                            ...this.state.msgList,
                            { isUser: false, content: result.data.message }]
                    })
                }
                if (this.state.timerID !== -1) {
                    clearTimeout(this.state.timerID)
                }
                if (result.data.wait > 0) {
                    let _timerID = setTimeout(() => {
                        axios.post("http://127.0.0.1:8000/dsl", {
                            token: this.state.token,
                            message: "!!!timeout"
                        }).then(result => this.handleResponse(result))
                    }, result.data.wait * 1000)
                    this.setState({ timerID: _timerID })
                }
            })
        }
        this.setState({ modalOpen: true })
    }

    componentDidUpdate() {
        let msgBox = document.getElementById("msgBox");
        if (msgBox)
            msgBox.scrollTop = msgBox.scrollHeight - 400;
    }


    handleResponse = (response) => {
        setTimeout(() => {  // 设置500ms的延迟，让机器人回复自然一些
            if (response.data.message) {
                this.setState({
                    msgList: [
                        ...this.state.msgList,
                        { isUser: false, content: response.data.message }]
                })
            }
            if (this.state.timerID !== -1) {
                clearTimeout(this.state.timerID)
            }
            if (response.data.wait > 0) {
                let _timerID = setTimeout(() => {
                    axios.post("http://127.0.0.1:8000/dsl", {
                        token: this.state.token,
                        message: "!!!timeout"
                    }).then(result => this.handleResponse(result))
                }, response.data.wait * 1000)
                this.setState({ timerID: _timerID })
            }
        }, 500)
    }

    // 处理按下回车键发送消息之后的函数
    // 1. 将输入框清空
    // 2. 将用户消息添加到消息列表
    // 3. 将用户消息发送到服务端请求回复
    // 4. 得到非空回复后，将回复消息添加到消息列表
    handleEnter = () => {
        let inputBox = document.getElementById("inputBox");
        if (!inputBox.value)
            return;

        this.setState({
            msgList: [
                ...this.state.msgList,
                { isUser: true, content: inputBox.value }
            ],
            inputValue: ""
        })

        axios.post("http://127.0.0.1:8000/dsl", {
            token: this.state.token,
            message: inputBox.value
        }).then(result => this.handleResponse(result))

    }

    // 处理用户输入，更新inputValue
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
                        footer={
                            <Input id="inputBox" suffix={<EnterOutlined />}
                                onPressEnter={() => this.handleEnter()}
                                onChange={this.keyUp}
                                value={this.state.inputValue}
                            ></Input>
                        }
                        title="DSL机器人"
                        wrapClassName="dslMod"
                    >
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
                        </List>
                        <span id="msgEnd" style={{ overflow: "hidden" }}></span>
                    </Modal>
                </div>
            </div>
        );
    }
}