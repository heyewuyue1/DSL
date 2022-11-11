# DSLBot

[TOC]



## 项目介绍

领域特定语言（DomainSpecificLanguage，DSL）可以提供一种相对简单的文法，用于特定领域的业务流程定制。本项目定义一个领域特定脚本语言，这个语言能够描述在线客服机器人的自动应答逻辑，并设计实现一个解释器解释执行这个脚本，可以根据用户的不同输入，根据脚本的逻辑设计给出相应的应答。

本项目采用了B/S架构，在后端设计了词法分析，语法分析功能用于解释执行DSL脚本文件，同时使用FastAPI封装了Restful API与前端进行交互；在前端设计了一个美观轻便的React组件，使用axios与后端进行通信。该组件常时作为一个客服按钮悬浮于页面顶部，用户点击后弹出对话框，开始执行自动应答逻辑，方便在不同的网站上复用。

## 用户指南

### 安装依赖

本项目对运行环境有以下要求:

- Python >= 3.10.6
- Node >= 16.17.0
- npm >= 8.15.0

如果您的操作系统尚不满足上述需求，请先到对应的官方网站寻求帮助。

[Python官方网站](https://www.python.org/)

[Node.js官方网站](https://nodejs.org/en/)（在安装完Node之后，安装器会自动安装配套的npm）

#### 安装后端依赖

将您的工作目录切换到DSLBot/server下后依次执行以下命令：

```bash
pip install fastapi
```

```bash
pip install "uvicorn[stantard]"
```

```bash
pip install python-jose
```

#### 安装前端依赖

将您的工作目录切换到DSLBot/client下后执行以下命令：

```bash
npm install
```

之后npm便会自动安装所有需要的依赖包。

### 运行DSLBot

将您的工作目录切换到DSL/server下后执行以下命令启动后端服务程序：

```bash
python3 main.py [filePath]
```

其中`filePath`参数是您已经编写好的`.bot`文件，如果您还不知道什么是`.bot`文件，请参见下一模块：编写一个.bot文件。不过在这一环节您可以不用担心这个参数，因为在不指定的情况下，程序会自动解析一个测试脚本文件，它足以让您测试是否可以正常运行DSLBot。

然后将您的工作目录切换到DSL/client下后执行以下命令启动前端组件：

```bash
npm start
```

启动完成后，您应该可以看到一个弹出的浏览器页面，上面只有一个客服按钮，如下图所示：

<img src="https://tva1.sinaimg.cn/large/008vxvgGly1h80m3u7909j30ek0a8a9w.jpg" alt="悬浮状态的DSLBot" style="zoom:50%;" />

点击该按钮，如果正常出现了对话框和一句机器人说的：“How can I help you?”，即为启动成功。

![image-20221111134850757](https://tva1.sinaimg.cn/large/008vxvgGly1h81535imrqj31gf0u03z9.jpg)

### 编写.bot文件

#### 状态与状态转移

在线客服机器人的应答逻辑被抽象为一个摩尔型自动机。DSL脚本即为描述这个自动机的脚本，它是由对一系列状态的描述组成的。下面我们先来看如何定义一个状态。

```
Status main
    Speak "What can I help you?"
    Wait 5
    Hear "a" aProc
    Hear "b" bProc
    Hear "quit" quitProc
    Default defaultProc
    Timeout quitProc
```

上述的代码段定义了一个叫做`main`的状态，可以看到它里面包含了一个Speak语句，一个Wait语句，若干个Hear语句，一个Default语句和一个Timeout语句，这也是几乎所有状态所包含的内容。下面将逐一介绍每个语句的含义：

- Speak语句：当刚刚转移到这个状态时机器人说的话；
- Wait语句：机器人在这个状态停留的时间；
- Hear语句：如果接收到用户所说的话可以匹配Hear语句之后的**正则表达式**，则转移到相应的状态。比如：`Hear "a" aProc`意味着接受到用户输入一个a之后转移到`aProc`状态；
- Default语句：如果接受到用户所说的话无法匹配任何Hear语句，则转移到相应的状态；
- Timeout语句：如果在状态停留的时间到达之前，没有接收到任何消息，则转移到相应的状态。

有了这些知识之后，您就已经可以开始编写一个不错的用于描述客服逻辑的`.bot`文件了。但是在您开始编写之前，还需要注意以下两点：

1. 每一个`.bot`文件都必须有一个名为`main`的状态作为起始状态；

2. 每一个状态的都**最好**有一对配套的Wait语句和Timeout语句。

   - 如果一个状态中没有任何的Wait语句和Timeout语句，那么这个用户的信息就会持续占用后端的内存资源；

   - 如果一个状态中只有Wait语句而没有Timeout语句，那么会产生语法错误，因为这个状态在超时之后没有别的状态可进行转移；
   - 如果一个状态只有Timeout语句而没有Wait语句，那么尽管程序不会报错，但是这条Timeout语句也并不会生效

#### 定义和使用变量

如果您并不满足让您的客服机器人仅仅使用固定的字符串与用户进行交流，DSLBot支持自定义变量。

在您编写完一个`.bot`文件之后，就可以通过上一部分所讲的方式加载并运行DSLBot了。以下是一份完整的`.bot`文件，在您不知道该如何编写的时候，可以参照该文件。

```
Status main
    Speak "What can I help you?"
    Wait 5
    Hear "a" aProc
    Hear "b" bProc
    Hear "quit" quitProc
    Default defaultProc
    Timeout quitProc

Status aProc
    Speak "This is status a."
    Wait 5
    Hear "a" quitProc
    Hear "b" bProc
    Default defaultProc
    Timeout quitProc

Status bProc
    Speak "This is status b."
    Hear "a" aProc
    Hear "b" quitProc
    Wait 5
    Default defaultProc
    Timeout quitProc

Status defaultProc
    Speak "I don't understand."
    Wait 5
    Hear "a" aProc
    Hear "b" bProc
    Default defaultProc
    Timeout quitProc

Status quitProc
    Speak "Bye!"
```

#### 脚本语言的形式化定义

为了更严谨全面地定义这个脚本语言，下面给出该语言的BNF定义：

```html
<DSL> ::= {<Status>}
<Status> ::= "Status" <StatusName> {<Action>}
<StatusName> ::= <alpha>{<alpha>}
<alpha> ::= a|b|...|z|A|B|..|Z
<Action> ::= <SpeakAction>|<WaitAction>|<HearAction>|<DefaultAction>|<TimeoutAction>
<SpeakAction> ::= "Speak" <String>
<String> ::= double_quote{*}double_quote
<WaitAction> ::= "Wait" <number>
<number> ::= <digit>{<digit>}
<digit> ::= 0|1|...|9
<HearActon> ::= "Hear" <String> <StatusName>
<DefaultAction> ::= "Default" <StatusName>
<TimeoutAction> ::= "Timeout" <StatusName>
```

*其中\*号代表任意字符*。

## 模块划分及功能描述

本项目共分为词法分析、语法分析、后端应答、前端GUI，共4个模块。前三个模块在后端实现，最后一个模块在前端实现。本项目后端采用Python语言编写，前端采用Javascript语言编写。下面将对4个模块进行逐一介绍。

### 词法分析模块

词法分析在`server/lex.py`中实现，

### 语法分析模块

### 后端应答模块

### 前端GUI模块

前端GUI是由一个React组件实现的，它的核心在`client/DSLbot.jsx`。在该文件中定义了一个React组件叫做DSLBot，这个组件在平常只是以一个客服标志普通的悬浮在页面上，如下图所示：





当用户单击这个按钮之后，便会打开一个与机器人的聊天窗口，如下图所示：

![image-20221111025348907](https://tva1.sinaimg.cn/large/008vxvgGly1h80m5l2kfyj31gp0u0t9f.jpg

用户便可以通过这个窗口与客服机器人进行对话。

下面详细阐述该组件的实现方式。

#### 渲染函数

在渲染函数中返回的jsx对象的大体结构如下所示，先将渲染函数呈现出来有助于了解前端的整体架构。

```jsx
<Button onclick={() => this.handleClick()}>
  {/*该部分是页面上的悬浮按钮*/}
</Button>
<Modal
  {/*该部分是对话框*/}
  open={this.state.modalOpen}
  onCancel = {() => this.setState({modalOpen: false})}
  footer={
    {/*对话框的脚部是一个输入框*/}
      <Input 
           onPressEnter={() => this.handleEnter()}
           onChange={this.keyUp}
           value={this.state.inputValue}
           ></Input>
    }>
  {/*对话框的内容是一个列表*/}
  <List>
    {/*实时呈现this.state.msgList中的内容，通过this.handleResponse()函数更新*/}
  </List>
</Modal>
```

#### state变量表

下面介绍需要实时渲染的state变量：

| 变量名     | 数据类型                                 | 功能                                                         |
| ---------- | ---------------------------------------- | ------------------------------------------------------------ |
| modalOpen  | boolean                                  | 用于记录当前对话框是否处于打开状态。                         |
| msgList    | list[{isUser: boolean, content: string}] | 用于记录对话框中的消息，isUser用于标注该消息是否为用户所发送的消息，content为消息内容。 |
| inputValue | string                                   | 用于实时记录输入框中的内容                                   |
| token      | string                                   | 当前用户与后端通信的凭证                                     |
| timerID    | int                                      | 当前超时计时器的编号                                         |

#### Button与handleClick()

在用户点击完页面上悬浮的按钮后，程序需要完成两个任务：

1. 将对话框呈现出来；
2. 建立与后端的链接。

其中第一个任务只需要将`modalOpen`的值设置为true即可；第二个任务需要用axios库与后端进行一次通信，请求到一个token和要显示在对话框中的第一条信息，如下所示：

```jsx
handleClick = () => {
        if (!this.state.token) {
            axios.get("http://127.0.0.1:8000/token").then(result => {
                this.setState({
                    token: result.data.token,
                    msgList: [
                        ...this.state.msgList,
                    {isUser: false, content: result.data.message}
                    ],
                })
            })
        }
```

