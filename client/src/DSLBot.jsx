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

    /**
     * @description: 处理页面上的客服按钮点击事件
     *               1. 请求到token
     *               2. 设置token
     *               3. 调用handleResponse处理message和wait
     * @return {*}
     */
    handleClick = () => {
        if (!this.state.token) {
            axios.get("http://127.0.0.1:8000/token").then(result => {
                if (result.data.message) {
                    this.setState({
                        token: result.data.token
                    })
                }
                this.handleResponse(result)
            })
        }
        this.setState({ modalOpen: true })
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
     * @description: 处理从后端得到的应答中的message字段和wait字段
     *               1. 在msgList中添加message
     *               2. 设定计时器
     *               3. 在计时器触发后向后端发送超时信息，并回调自身处理应答
     * @param {*} response 从后端得到的应答
     * @return {*}
     */
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


    /**
     * @description: 处理按下回车键发送消息之后的函数
                     1. 将输入框清空
                     2. 将用户消息添加到消息列表
                     3. 将用户消息发送到服务端请求回复
                     4. 得到非空回复后，将回复消息添加到消息列表
     * @return {*}
     */
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
                                onPressEnter={() => this.handleEnter()}
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