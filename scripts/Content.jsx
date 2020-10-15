    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [users, setUsers] = React.useState();
    const botText = {color:'darkgreen'};
    const userText = {color:'black'};
    
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
    
    return (
        <div id="container">
            <div id="components">
            <span id="users">Users = {users}</span>
                    <ol>
                        {
                            messages.map(
                           (message, index) => <li 
                           style={{color: message[0] === "1337-BOT" ? botText : userText}}
                           key={index}><span id="username">{message[0] + " : "}
                           </span>{message[1]}
                           </li>)
                        }
                    </ol>
            <Button />
            </div>
        </div>
    );
}
