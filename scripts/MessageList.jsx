import * as React from 'react';
import { Socket } from './Socket';
import { Message } from './Message';

export function MessageList(props){
    const [messages, setMessages] = React.useState([]);
    
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('messages received', updateMessages);
            return () => {
                Socket.off('messages received', updateMessages);
            }
        });
    }
    
    function updateMessages(data) {
        console.log("Received message from server: " + data['allMessages']);
        setMessages(data['allMessages']);
    }
    
    getNewMessages();
    
    
    
    return <ol>
                {
                    messages.map(
                    (message, index) => <Message msg={message} ind={index}/>)
                }
            </ol>;
}                