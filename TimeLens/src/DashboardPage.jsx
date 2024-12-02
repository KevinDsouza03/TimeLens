import { useState, useEffect } from 'react';
import { 
  BarChart, Bar, PieChart, Pie, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, Cell
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

export default function DashboardPage() {
  const [programInsights, setProgramInsights] = useState([]);
  const [focusTimeline, setFocusTimeline] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [insightsRes, timelineRes] = await Promise.all([
          fetch('http://localhost:8000/api/program-insights'),
          fetch('http://localhost:8000/api/focus-logs/timeline')
        ]);
        
        const insights = await insightsRes.json();
        const timeline = await timelineRes.json();
        
        // Filter out entries where program is 'None'
        const filteredInsights = insights.filter(item => item.program !== 'None');
        setProgramInsights(filteredInsights);
        setFocusTimeline(timeline);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  return (
    <div className="flex flex-col gap-8 w-full max-w-7xl mx-auto p-6">
      <h1 className="font-bold text-4xl text-center">TimeLens Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Total Time Per Program */}
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-4">Total Time Per Program</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={programInsights}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="program" />
              <YAxis label={{ value: 'Minutes', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="total_time" fill="#8884d8" name="Total Time (min)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Context Switches Distribution */}
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-4">Context Switches Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={programInsights}
                dataKey="context_switch"
                nameKey="program"
                cx="50%"
                cy="50%"
                outerRadius={100}
                fill="#8884d8"
              >
                {programInsights.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Timeline View */}
        <div className="bg-white p-6 rounded-lg shadow-lg md:col-span-2">
          <h2 className="text-xl font-semibold mb-4">Daily Activity Timeline</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={focusTimeline}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="switches" 
                stroke="#8884d8" 
                name="Context Switches"
              />
              <Line 
                type="monotone" 
                dataKey="unique_programs" 
                stroke="#82ca9d" 
                name="Unique Programs"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}