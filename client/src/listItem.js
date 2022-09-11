import Avatar from "antd/lib/avatar/avatar";
import React from "react";
import { RobotOutlined, UserOutlined } from "@ant-design/icons";
export const robotAvatarOptions = {
    style: { color: "#f56a00", backgroundColor: "#fde3cf" },
    icon: React.createElement(RobotOutlined, null),
};
export const userAvatarOptions = {
    style: { color: "white", backgroundColor: "#87d068" },
    icon: React.createElement(UserOutlined, null),
};
export const RobotWrapperStyle = {
    display: "flex",
    position: "relative",
};
export const robotAvatarWrapperStyle = {
    width: "32px",
};
export const popWrapperStyle = {
    width: "calc(100% - 20px - 64px)",
    margin: "10px",
    padding: "10px",
};
export const robotArrowStyle = {
    left: "40px",
    top: "15px",
    color: "white",
};
export const userArrowStyle = {
    right: "40px",
    top: "15px",
    color: "white",
};
export function RobotItem(props) {
    const { isUser, text } = props;
    return (React.createElement("div", { style: RobotWrapperStyle },
        React.createElement("div", { style: robotAvatarWrapperStyle }, !isUser && React.createElement(Avatar, Object.assign({}, robotAvatarOptions))),
        React.createElement("div", { className: "ant-popover-arrow", style: isUser ? userArrowStyle : robotArrowStyle }),
        React.createElement("div", { className: "ant-popover-inner", style: popWrapperStyle },
            React.createElement("span", null, text)),
        React.createElement("div", { style: robotAvatarWrapperStyle }, isUser && React.createElement(Avatar, Object.assign({}, userAvatarOptions)))));
}
