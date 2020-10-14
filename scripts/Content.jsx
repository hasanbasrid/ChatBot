    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';

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
            Socket.on('connected', updateUsers);
            return () => {
                Socket.off('connected', updateUsers);
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
        <div>
            <h1>Messages</h1>
                <ol>
                    {
                        messages.map(
                        (message, index) => <li key = {index}>{message[0] + " : " + message[1]}</li>)
                    }
                </ol>
            <Button />
            <h2>Users = {users}</h2>
        </div>
    );
}
