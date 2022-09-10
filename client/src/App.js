import React, { useCallback, useState } from "react";
import { CustomerServiceOutlined } from "@ant-design/icons";
import { Button } from "antd";
import "antd/dist/antd.less";
import axios from "axios"
import { useRegister } from "chatbot-antd";

function App() {
	const [modalOpen, setModalOpen] = useState(false);
	//使用useCllback避免用户输入时调用匹配！！！！！！！
	const callb = useCallback((v) => {
		setTimeout(async () => {
			//使用settimeout 更像机器人回话
			let returnValue = await axios.get("http://127.0.0.1:8000/dsl/" + v.text)
      console.log("rS: "+ returnValue.data)
			if (returnValue.data) {
				//排除null
				setList((prev) => [
					...prev,
					{ isUser: false, text: returnValue.data },
				]);
			}
		}, 500);
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	// 注册
	const [render, setList] = useRegister(
		modalOpen,
		callb,
		{
			onOk: () => setModalOpen(false),
			onCancel: () => setModalOpen(false),
			title: "DSL机器人客服",
		},
		{},
		<div>我是机器人初始欢迎语句！</div>
	);

	return (
		<div>
			<div
				style={{
					position: "fixed",
					right: "10px",
					top: "40%",
				}}
			>
				<Button type="primary" onClick={() => setModalOpen(!modalOpen)}>
					<CustomerServiceOutlined></CustomerServiceOutlined>
				</Button>
			</div>
			{render}
		</div>
	);
}

export default App;
