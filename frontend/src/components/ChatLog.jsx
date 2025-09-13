import { useEffect, useRef } from 'react';
import Message from './Message';
import TaskProgress from './TaskProgress';

// This component now receives the list of messages as a prop.
export default function ChatLog({ messages }) {
  const chatLogRef = useRef(null);

  useEffect(() => {
    if (chatLogRef.current) {
      chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div ref={chatLogRef} className="container-fluid p-3 h-100 overflow-auto">
      {messages.map((msg, index) => {
        // If the message is a plan, render the TaskProgress component.
        if (msg.type === 'agent_plan') {
          return <TaskProgress key={index} tasks={msg.tasks} />;
        }
        
        // Otherwise, render a standard message bubble with metadata support.
        return <Message key={index} type={msg.type} text={msg.text} metadata={msg.metadata} />;
      })}
    </div>
  );
}
