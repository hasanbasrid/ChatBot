import * as React from 'react';
import { Socket } from './Socket';
import { Message } from './Message';

export function MessageList() {
  const [messages, setMessages] = React.useState([]);

  function updateMessages(data) {
    console.log(`Received message from server: ${data.allMessages}`);
    setMessages(data.allMessages);
  }

  function getNewMessages() {
    React.useEffect(() => {
      Socket.on('messages received', updateMessages);
      return () => {
        Socket.off('messages received', updateMessages);
      };
    });
  }

  getNewMessages();

  return (
    <ol>
      {
                    messages.map(
                      (message, index) => <Message msg={message} ind={index} />,
                    )
                }
    </ol>
  );
}
