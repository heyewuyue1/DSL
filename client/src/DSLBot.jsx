import React from "react";
import { List, Button, Modal, Input, Avatar} from "antd"
import axios from "axios"
import { CustomerServiceOutlined, EnterOutlined } from "@ant-design/icons";
import { RobotItem } from "./listItem";
import "antd/dist/antd.min.css";
export default class DSLBot extends React.Component {
    data = [
        {
            title: "aaa",
        },
        {
            title: "bbb",
        },
        {
            title: "ccc",
        },
    ]
    constructor(props) {
        super(props);
        this.state = {
            modalOpen: false,
            msgList: [{isUser: false, content: "欢迎使用DSL机器人客服"}],
            inputValue: ""
        };
    }

    handleEnter = async () => {
        let inputBox = document.getElementById("inputBox");
        if (!inputBox.value)
            return;

        let retStr = await axios.get("http://127.0.0.1:8000/dsl/"+inputBox.value);

        this.setState({
            msgList: [
                ...this.state.msgList,
                {isUser: true, content: inputBox.value}
            ],
            inputValue: ""
        });

        setTimeout(() => {
            if (retStr.data) {
                this.setState({
                    msgList: [
                        ...this.state.msgList,
                    {isUser: false, content: retStr.data}
                    ]
                });
            }
        }, 500);
        console.log(this.state.msgList);
    }

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
				<Button type="primary" onClick={() => this.setState({modalOpen: true})}>
					<CustomerServiceOutlined></CustomerServiceOutlined>
				</Button>
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
                    {/* TODO:  右对齐，滚动条*/}
                    <List id="msgBox"
                        split={false}
                        dataSource={this.state.msgList}
                        itemLayout="horizontal"
                        renderItem={item => (
                            <List.Item >
                                <RobotItem  isUser={item.isUser} text={item.content}></RobotItem>
                            </List.Item>
                        )}>
                    </List>
                </Modal>
			</div>
		</div>
        );
    }
}