import Message from './Message';
import TaskProgress from './TaskProgress';

// This component now receives the list of messages as a prop.
export default function ChatLog({ messages }) {
  return (
    <div className="container-fluid p-3">
      {messages.map((msg, index) => {
        // If the message is a plan, render the TaskProgress component.
        if (msg.type === 'agent_plan') {
          return <TaskProgress key={index} tasks={msg.tasks} />;
        }
        
        // Otherwise, render a standard message bubble.
        return <Message key={index} type={msg.type} text={msg.text} />;
      })}
    </div>
  );
}
