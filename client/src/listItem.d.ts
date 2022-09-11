import { AvatarProps } from "antd/lib/avatar/avatar";
import { CSSProperties, ReactNode } from "react";
export declare const robotAvatarOptions: AvatarProps;
export declare const userAvatarOptions: AvatarProps;
export declare const RobotWrapperStyle: CSSProperties;
export declare const robotAvatarWrapperStyle: CSSProperties;
export declare const popWrapperStyle: CSSProperties;
export declare const robotArrowStyle: CSSProperties;
export declare const userArrowStyle: CSSProperties;
export declare type ItemProps = {
    isUser?: boolean;
    text: ReactNode;
};
export declare function RobotItem(props: ItemProps): JSX.Element;
