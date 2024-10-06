import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const TimeManager = () => {
    const [activity, setActivity] = useState('');
    const [todoItem, setTodoItem] = useState('');
    const [message, setMessage] = useState('');
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
    // Simulating data fetch for the chart
    const mockData = [
        { program: 'Code.exe', timeSpent: 20 },
        { program: 'chrome.exe', timeSpent: 921 },
        { program: 'Discord.exe', timeSpent: 65 },
        { program: 'ONENOTE.EXE', timeSpent: 1509 },
    ];
    setChartData(mockData);
    }, []);

    const handleActivityChange = (event) => {
    setActivity(event.target.value);
    };

    const handleTodoItemChange = (event) => {
    setTodoItem(event.target.value);
    };

    const handleSubmit = () => {
    switch (activity) {
        case 'Track Usage':
        setMessage('Tracking usage... Press Stop when finished.');
        break;
        case 'Work Session':
        setMessage('Starting work session...');
        break;
        case 'Add Todo':
        if (todoItem) {
            setMessage(`Added "${todoItem}" to your todo list.`);
            setTodoItem('');
        } else {
            setMessage('Please enter a todo item.');
        }
        break;
        case 'Visualize':
        setMessage('Displaying visualization...');
        break;
        default:
        setMessage('Please select an activity.');
    }
    };

    return (
    <div className="p-4 max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Time Manager</h1>
        
        <div className="mb-4">
        <select 
            value={activity} 
            onChange={handleActivityChange}
            className="w-full p-2 border rounded"
        >
            <option value="">Select an activity</option>
            <option value="Track Usage">Track Usage</option>
            <option value="Work Session">Work Session</option>
            <option value="Add Todo">Add Todo</option>
            <option value="Visualize">Visualize</option>
        </select>
        </div>
        
        {activity === 'Add Todo' && (
        <div className="mb-4">
            <input
            type="text"
            value={todoItem}
            onChange={handleTodoItemChange}
            placeholder="Enter todo item"
            className="w-full p-2 border rounded"
            />
        </div>
        )}
        
        <button onClick={handleSubmit} className="w-full mb-4 p-2 bg-blue-500 text-white rounded">
        Submit
        </button>
        
        {message && (
        <div className="mb-4 p-4 bg-gray-100 border rounded">
            <h3 className="font-bold">Status</h3>
            <p>{message}</p>
        </div>
        )}
        
        {activity === 'Visualize' && chartData.length > 0 && (
        <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">Time Spent on Programs</h2>
            <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
                <XAxis dataKey="program" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="timeSpent" fill="#8884d8" />
            </BarChart>
            </ResponsiveContainer>
        </div>
        )}
    </div>
    );
};

export default TimeManager;