import { useState, useEffect } from 'react';
import api from '../api/axiosConfig';
import Navbar from '../components/Navbar';
import IssueCard from '../components/IssueCard';

const SprintBoard = () => {
    const [issues, setIssues] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchIssues = async () => {
            try {
                // Adjust this route to match your FastAPI endpoint for fetching issues
                // E.g., /api/issues or /api/sprints/{sprint_id}/issues
                const response = await api.get('/issues'); 
                setIssues(response.data);
            } catch (err) {
                setError('Failed to load sprint data.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchIssues();
    }, []);

    // Group issues by status
    const todoIssues = issues.filter(issue => issue.status === 'To Do');
    const inProgressIssues = issues.filter(issue => issue.status === 'In Progress');
    const doneIssues = issues.filter(issue => issue.status === 'Done');

    const Column = ({ title, count, items }) => (
        <div className="flex flex-col bg-gray-50 rounded-lg h-full p-4 min-w-[300px]">
            <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold text-gray-700">{title}</h3>
                <span className="bg-gray-200 text-gray-600 rounded-full px-2 py-1 text-xs font-bold">
                    {count}
                </span>
            </div>
            <div className="flex-1 overflow-y-auto pr-1">
                {items.length === 0 ? (
                    <div className="text-sm text-gray-400 text-center mt-4 border-2 border-dashed border-gray-200 p-4 rounded">
                        No issues here
                    </div>
                ) : (
                    items.map(issue => <IssueCard key={issue.id} issue={issue} />)
                )}
            </div>
        </div>
    );

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col">
            <Navbar />
            
            <main className="flex-1 container mx-auto p-6 overflow-hidden flex flex-col">
                <header className="mb-6 flex justify-between items-end">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-800">Active Sprint</h1>
                        <p className="text-gray-500">Sprint 1: Authentication & Foundations</p>
                    </div>
                    <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded shadow transition font-semibold">
                        + Create Issue
                    </button>
                </header>

                {error && <div className="bg-red-100 text-red-600 p-3 rounded mb-4">{error}</div>}
                
                {loading ? (
                    <div className="flex-1 flex items-center justify-center text-gray-500">Loading board...</div>
                ) : (
                    <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6 overflow-hidden pb-4">
                        <Column title="TO DO" count={todoIssues.length} items={todoIssues} />
                        <Column title="IN PROGRESS" count={inProgressIssues.length} items={inProgressIssues} />
                        <Column title="DONE" count={doneIssues.length} items={doneIssues} />
                    </div>
                )}
            </main>
        </div>
    );
};

export default SprintBoard;