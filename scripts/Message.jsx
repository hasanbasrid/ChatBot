import * as React from 'react';

export function Message(props){
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
        const index = props.ind;
        const type = message[0];
        const profile_pic = message[1];
        const username = message[2];
        const text = message[3];
        
        if(type === "image"){
            return <li style={{color : 'black'}} key={index}>
            <img id="profile_picture" src={profile_pic}/>
            <span id="username">{username + " : "}</span>
            <img id="inline_image" src={text}/>
            </li>; 
        }
        
        else if(type ==="url"){
            return <li style={{color : 'black'}} key={index}>
            <img id="profile_picture" src={profile_pic}/>
            <span id="username">{username + " : "}</span>
            <a href={text}>{text}</a>
            </li>;
        }
        
        return <li style={{color : 'black'}} key={index}>
            <img id="profile_picture" src={profile_pic}/>
            <span id="username">{username + " : "}</span>
            {text}
            </li>;
    }
    
    function BotMessage(props){
        const message = props.msg;
        const index = props.ind;
        return <li style={{color : 'darkgreen'}} key={index}>
        <span id="username">{message[2] + " : "}</span>
        <span dangerouslySetInnerHTML={{ __html: message[3] }}/>
        </li>;
    }