import { useState, useEffect } from 'react';
import api from '../api/axios';
import styles from './IssueForm.module.css';

const ASSIGNEE_SEARCH_DEBOUNCE = 250;

const ISSUE_TYPES = [
    { value: 'TASK', label: 'Task' },
    { value: 'BUG', label: 'Bug' },
    { value: 'STORY', label: 'Feature' }
];
const PRIORITIES = ['Low', 'Medium', 'High'];

const IssueForm = ({ projectId, projects = [], onClose, onCreated }) => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [assigneeEmail, setAssigneeEmail] = useState('');
    const [issueType, setIssueType] = useState('TASK');
    const [priority, setPriority] = useState('Medium');
    const [storyPoints, setStoryPoints] = useState(1);
    const [parentIssueId, setParentIssueId] = useState('');
    const [availableIssues, setAvailableIssues] = useState([]);
    const [selectedProjectId, setSelectedProjectId] = useState(projectId || projects[0]?._id || '');
    const [assigneeSuggestions, setAssigneeSuggestions] = useState([]);
    const [error, setError] = useState(null);
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        if (!selectedProjectId && (projectId || projects.length > 0)) {
            setSelectedProjectId(projectId || projects[0]._id);
        }
    }, [projectId, projects, selectedProjectId]);

    useEffect(() => {
        const loadParentOptions = async () => {
            if (!selectedProjectId) {
                setAvailableIssues([]);
                return;
            }

            try {
                const data = await api.get(`/issues?project_id=${selectedProjectId}`);
                setAvailableIssues(Array.isArray(data.data) ? data.data : []);
            } catch (error) {
                setAvailableIssues([]);
            }
        };

        loadParentOptions();
    }, [selectedProjectId]);

    useEffect(() => {
        const searchAssignees = async () => {
            const query = assigneeEmail.trim();
            if (!query || query.length < 2) {
                setAssigneeSuggestions([]);
                return;
            }

            try {
                const response = await api.get(`/auth/users?search=${encodeURIComponent(query)}`);
                const users = Array.isArray(response.data) ? response.data : [];
                setAssigneeSuggestions(users.map((user) => user.email));
            } catch (error) {
                setAssigneeSuggestions([]);
            }
        };

        const timeoutId = setTimeout(searchAssignees, ASSIGNEE_SEARCH_DEBOUNCE);
        return () => clearTimeout(timeoutId);
    }, [assigneeEmail]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        setSaving(true);

        try {
            if (!selectedProjectId) {
                setError('Please select a project before creating an issue.');
                return;
            }

            const payload = {
                title,
                description,
                project_id: selectedProjectId,
                parent_id: parentIssueId || null,
                assignee_email: assigneeEmail || null,
                issue_type: issueType,
                status: 'TODO',
                priority,
                story_points: storyPoints
            };

            await api.post('/issues', payload);
            onCreated();
            onClose();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to create issue.');
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className={styles.overlay}>
            <div className={styles.modal}>
                <div className={styles.header}>
                    <h2>Create Issue</h2>
                    <button className={styles.closeButton} onClick={onClose}>×</button>
                </div>

                <form className={styles.form} onSubmit={handleSubmit}>
                    <label>
                        Title
                        <input
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                            placeholder="Issue title"
                        />
                    </label>

                    <label>
                        Description
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Describe the issue"
                            rows={4}
                        />
                    </label>

                    <label>
                        Project
                        <select
                            value={selectedProjectId}
                            onChange={(e) => setSelectedProjectId(e.target.value)}
                            required
                        >
                            <option value="" disabled>
                                Select a project
                            </option>
                            {projects.map((project) => (
                                <option key={project._id} value={project._id}>
                                    {project.name}
                                </option>
                            ))}
                        </select>
                    </label>

                    <label>
                        Assignee Email
                        <input
                            value={assigneeEmail}
                            onChange={(e) => setAssigneeEmail(e.target.value)}
                            placeholder="member@example.com"
                        />
                        {assigneeSuggestions.length > 0 && (
                            <div className={styles.suggestions}>
                                {assigneeSuggestions.map((email) => (
                                    <button
                                        key={email}
                                        type="button"
                                        className={styles.suggestionButton}
                                        onClick={() => setAssigneeEmail(email)}
                                    >
                                        {email}
                                    </button>
                                ))}
                            </div>
                        )}
                    </label>

                    <label>
                        Parent Issue (optional)
                        <select value={parentIssueId} onChange={(e) => setParentIssueId(e.target.value)}>
                            <option value="">No parent issue</option>
                            {availableIssues.map((issue) => (
                                <option key={issue.id} value={issue.id}>{issue.issue_key} - {issue.title}</option>
                            ))}
                        </select>
                    </label>

                    <div className={styles.row}>
                        <label>
                            Issue Type
                            <select value={issueType} onChange={(e) => setIssueType(e.target.value)}>
                                {ISSUE_TYPES.map((type) => (
                                    <option key={type.value} value={type.value}>{type.label}</option>
                                ))}
                            </select>
                        </label>

                        <label>
                            Priority
                            <select value={priority} onChange={(e) => setPriority(e.target.value)}>
                                {PRIORITIES.map((level) => (
                                    <option key={level} value={level}>{level}</option>
                                ))}
                            </select>
                        </label>
                    </div>

                    <label>
                        Story Points
                        <input
                            type="number"
                            min="1"
                            max="20"
                            value={storyPoints}
                            onChange={(e) => setStoryPoints(Number(e.target.value))}
                        />
                    </label>

                    <div className={styles.actions}>
                        <button type="button" className={styles.cancelButton} onClick={onClose} disabled={saving}>
                            Cancel
                        </button>
                        <button type="submit" className={styles.submitButton} disabled={saving}>
                            {saving ? 'Creating...' : 'Create'}
                        </button>
                    </div>

                    {error && <p className={styles.error}>{error}</p>}
                </form>
            </div>
        </div>
    );
};

export default IssueForm;
