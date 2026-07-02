const IssueCard = ({ issue }) => {
    // Dynamic styling based on priority
    const priorityColors = {
        High: 'bg-red-100 text-red-700 border-red-200',
        Medium: 'bg-yellow-100 text-yellow-700 border-yellow-200',
        Low: 'bg-blue-100 text-blue-700 border-blue-200',
    };

    const badgeStyle = priorityColors[issue.priority] || 'bg-gray-100 text-gray-700 border-gray-200';

    return (
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition cursor-pointer mb-3 text-left">
            <div className="flex justify-between items-start mb-2">
                <span className={`text-xs font-semibold px-2 py-1 rounded border ${badgeStyle}`}>
                    {issue.priority || 'Task'}
                </span>
                <span className="text-xs text-gray-400 font-mono">{issue.issue_key}</span>
            </div>
            
            <h4 className="font-bold text-gray-800 text-sm mb-2">{issue.title}</h4>
            
            <div className="flex justify-between items-center mt-4 border-t pt-2">
                <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs font-bold">
                        {issue.assignee ? issue.assignee.charAt(0).toUpperCase() : '?'}
                    </div>
                    <span className="text-xs text-gray-600">{issue.assignee || 'Unassigned'}</span>
                </div>
                <span className="text-xs text-gray-400">{issue.story_points} pts</span>
            </div>
        </div>
    );
};

export default IssueCard;