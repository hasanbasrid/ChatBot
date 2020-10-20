    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';
import { GoogleButton } from './GoogleButton';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [users, setUsers] = React.useState();
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('messages received', updateMessages);
            return () => {
                Socket.off('messages received', updateMessages);
            }
        });
    }
    
    function getNewUsers(){
        React.useEffect(() => {
            Socket.on('user count changed',updateUsers);
            return () => {
                Socket.off('user count changed', updateUsers);
            }
        });
    }
    
    function updateMessages(data) {
        console.log("Received message from server: " + data['allMessages']);
        setMessages(data['allMessages']);
    }
    
    getNewMessages();
    
    function updateUsers(data){
        console.log("Received user count from server: " + data['users']);
        setUsers(data['users']);
    }
    
    getNewUsers();
    
    function Message(props){
        const username = props.msg[2];
        const index = props.ind;
        if(username === "1337-BOT"){
            return <BotMessage msg ={props.msg} ind={index} />;
        }
        else{
            return <UserMessage msg ={props.msg} ind={index}/>;
        }
    }
    function UserMessage(props){
        const message = props.msg;
        const index = props.index;
        return <li style={{color : 'black'}}
            key={index}><span id="username">{message[2] + " : "}
            </span>{message[3]}
        </li>;
    }
    function BotMessage(props){
        const message = props.msg;
        const index = props.ind;
        return <li style={{color : 'darkgreen'}}
            key={index}><span id="username">{message[2] + " : "}
            </span><span dangerouslySetInnerHTML={{ __html: message[3] }}/>
        </li>;
    }
    
    return (
        <div id="container">
            <GoogleButton/>
            <div id="components">
            <span id="users">Online Users : {users}</span>
                    <ol>
                        {
                            messages.map(
                           (message, index) => <Message msg={message} ind={index}/>)
                        }
                    </ol>
            <Button />
            </div>
        </div>
    );
}
