import * as React from 'react';
import PropTypes from 'prop-types';

UserMessage.propTypes = {
  msg: PropTypes.string,
  index: PropTypes.number,
};

export function Message(props) {
  const { username } = props.msg[2];
  const { index } = props.ind;
  if (username === '1337-BOT') {
    return <BotMessage msg={props.msg} ind={index} />;
  }

  return <UserMessage msg={props.msg} ind={index} />;
}
function UserMessage(props) {
  const { message } = props.msg;
  const { index } = props.ind;
  const { type } = message[0];
  const { profilePic } = message[1];
  const { username } = message[2];
  const { text } = message[3];

  if (type === 'image') {
    return (
      <li style={{ color: 'black' }} key={index}>
        <img id="profile_picture" alt="" src={profilePic} />
        <span id="username">{`${username} : `}</span>
        <img id="inline_image" src={text} />
      </li>
    );
  } if (type === 'url') {
    return (
      <li style={{ color: 'black' }} key={index}>
        <img id="profile_picture" alt="" src={profilePic} />
        <span id="username">{`${username} : `}</span>
        <a href={text}>{text}</a>
      </li>
    );
  }

  return (
    <li style={{ color: 'black' }} key={index}>
      <img id="profile_picture" alt="" src={profilePic} />
      <span id="username">{`${username} : `}</span>
      {text}
    </li>
  );
}

function BotMessage(props) {
  const message = props.msg;
  const index = props.ind;
  return (
    <li style={{ color: 'darkgreen' }} key={index}>
      <img id="profile_picture" alt="" src={message[1]} />
      <span id="username">{`${message[2]} : `}</span>
      <span dangerouslySetInnerHTML={{ __html: message[3] }} />
    </li>
  );
}
