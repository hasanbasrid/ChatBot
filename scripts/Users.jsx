import * as React from 'react';
import { Socket } from './Socket';

export function Users(props){
    const [users, setUsers] = React.useState();
    
    function getNewUsers(){
        React.useEffect(() => {
            Socket.on('user count changed',updateUsers);
            return () => {
                Socket.off('user count changed', updateUsers);
            }
        });
    }
    
    function updateUsers(data){
        console.log("Received user count from server: " + data['users']);
        setUsers(data['users']);
    }
    
    getNewUsers();
    
    return <span id="users">Online Users : {users}</span>;
}
