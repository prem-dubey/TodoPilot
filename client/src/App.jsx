import { useEffect, useRef, useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [name, setName] = useState('');

  if (!name) {
    const userName = prompt("Please enter your name:");
    if (userName) {
      setName(userName);
      setChatHistory((prev) => [
        ...prev,
        { type: 'ai', text: `Hello ${userName}, how can I assist you today?` },
      ]);
    } else {
      setName('User');
    }
  }

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { type: 'user', text: input };
    setChatHistory((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
        }),
      });

      const data = await res.json();
      console.log("here", data);

      const aiResponse = {
        type: 'ai',
        text: data.response || 'No response from AI.',
      };
      setChatHistory((prev) => [...prev, aiResponse]);
      setInput('');
    } catch (err) {
      console.error(err);
      setChatHistory((prev) => [
        ...prev,
        { type: 'ai', text: '❌ Error: Could not reach server.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='flex items-center flex-col h-screen bg-gradient-to-r from-purple-300 to-blue-300 overflow-y-auto'>
      <h1 className='text-3xl font-bold text-center mt-10 bg-purple-200 px-7 py-2 rounded-full border-2 border-purple-400'>
        TodoPilot
      </h1>
      <p className='max-w-3xl mx-auto mt-5 text-xl text-center'>
        Just like a pilot navigates a plane, TodoPilot helps users navigate their
        day, steer their focus, and fly through tasks with smart AI support.
      </p>
      <p className='text-center mt-5 bg-purple-200 px-7 py-2 rounded-full border-2 border-purple-400'>
        Use AI to add, delete, and list your tasks
      </p>

      <form
        onSubmit={handleSubmit}
        className='flex items-center justify-between max-w-xl w-full md:h-13 h-12 mt-5'
      >
        <input
          className='border border-gray-300 rounded-md h-full border-r-0 outline-none w-full rounded-r-none px-3 text-gray-500 bg-white py-5'
          type='text'
          placeholder='Enter your text here'
          value={input}
          onChange={(e) => setInput(e.target.value)}
          required
        />
        <button
          type='submit'
          className='md:px-12 px-8 py-5 flex flex-col items-center justify-center h-full text-white bg-purple-500 hover:bg-purple-600 cursor-pointer transition-all rounded-md rounded-l-none'
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>

      <div className='bg-white max-w-3xl w-full mt-5 rounded-md shadow-lg overflow-y-auto max-h-96'>
        {chatHistory.map((msg, idx) => (
          <div
            key={idx}
            className={`my-3 mx-4 p-3 rounded-lg ${msg.type === 'user'
              ? 'bg-purple-100 text-right'
              : 'bg-gray-100 text-left'
              }`}
          >
            {Array.isArray(msg.text) ? (
              <ol className="text-gray-800 list-decimal ml-5">
                {msg.text.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ol>
            ) : (
              <p className="text-gray-800 whitespace-pre-line">{msg.text}</p>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

export default App;
