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
            msgList: [{isUser: false, content: "欢迎使用DSL机器人客服"}],  // 呈现在聊天框里的消息列表
            inputValue: "",  // 当前输入框中的内容
            token:""
        };
    }

    handleClick = async () => {
        if (!this.state.token) {
            let getToken = await axios.get("http://127.0.0.1:8000/token")
            this.setState({
                token: getToken.data,
            })
        }
        console.log(this.state.token)
        this.setState({
            modalOpen: true,
        })
    }

    // 处理按下回车键发送消息之后的函数
    // 1. 将输入框清空
    // 2. 将用户消息添加到消息列表
    // 3. 将用户消息发送到服务端请求回复
    // 4. 得到非空回复后，将回复消息添加到消息列表
    handleEnter = async () => {
        let inputBox = document.getElementById("inputBox");
        let msgBox = document.getElementById("msgBox");

        if (!inputBox.value)
            return;

        // let retStr = await axios.get("http://127.0.0.1:8000/dsl/" + inputBox.value);
        let retStr = await axios.post("http://127.0.0.1:8000/dsl",{
            token: this.state.token,
            message: inputBox.value
          })

        this.setState({
            msgList: [
                ...this.state.msgList,
                {isUser: true, content: inputBox.value}
            ],
            inputValue: ""
        });
        // msgBox.scrollTop = msgBox.scrollHeight
        // console.log(111)

        setTimeout(() => {  // 设置500ms的延迟，让机器人回复自然一些
            if (retStr.data) {
                this.setState({
                    msgList: [
                        ...this.state.msgList,
                    {isUser: false, content: retStr.data}
                    ]
                });
                // msgBox.scrollTop = msgBox.scrollHeight
                // console.log(222)
            }
        }, 500);
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
                <Modal open={this.state.modalOpen}
                    onCancel = {() => this.setState({modalOpen: false})}
                    footer = {
                        <Input id="inputBox" suffix={<EnterOutlined />}
                            onPressEnter={() => this.handleEnter()}
                            onChange={this.keyUp}
                            value={this.state.inputValue}
                            ></Input>
                    }
                    title = "DSL机器人"
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
                            <List.Item style={item.isUser?
                            {justifyContent:"flex-end", padding: "12px 10px"}:
                            {justifyContent:"flex-start", padding: "12px 10px"}}>
                                    <RobotItem isUser={item.isUser} text={item.content}></RobotItem>
                            </List.Item>
                        )}>
                    </List>
                </Modal>
			</div>
		</div>
        );
    }
}