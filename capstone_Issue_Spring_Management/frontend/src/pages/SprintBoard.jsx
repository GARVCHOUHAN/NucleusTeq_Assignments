import { useCallback, useEffect, useState } from "react";

import Navbar from "../components/common/navbar/Navbar";
import Sidebar from "../components/common/sidebar/Sidebar";
import { useProjects } from "../hooks/use-project";
import IssueService from "../services/issue-service";
import SprintService from "../services/sprint-service";
import styles from "./SprintBoard.module.css";


const today = new Date().toISOString().slice(0, 10);


const initialForm = {
    name: "",
    project_id: "",
    start_date: today,
    end_date: today
};

function validateSprint(form, sprints) {
    const startDate = new Date(form.start_date);
    const endDate = new Date(form.end_date);

    if (startDate > endDate) {
        return "Sprint start date must be before end date.";
    }

    const duplicateSprint = sprints.some(
        (sprint) =>
            sprint.name.toLowerCase() === form.name.toLowerCase() &&
            sprint.project_id === form.project_id
    );

    if (duplicateSprint) {
        return "Sprint with this name already exists in this project.";
    }


    const overlappingSprint = sprints.some((sprint) => {
        if (sprint.project_id !== form.project_id) {
            return false;
        }

        const existingStart = new Date(sprint.start_date);
        const existingEnd = new Date(sprint.end_date);

        return startDate <= existingEnd && endDate >= existingStart;
    });

    if (overlappingSprint) {
        return "Sprint dates overlap with another sprint in this project.";
    }


    return "";
}

const SprintBoard = () => {
    const { projects } = useProjects();
    const [sprints, setSprints] = useState([]);
    const [issues, setIssues] = useState([]);
    const [selectedProjectId, setSelectedProjectId] = useState("");
    const [form, setForm] = useState(initialForm);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const loadSprintData = useCallback(async () => {
        setLoading(true);
        setError("");

        try {
            const [sprintData, issueData] = await Promise.all([
                SprintService.getSprints(selectedProjectId),
                IssueService.getIssues({
                    project_id: selectedProjectId || undefined
                })
            ]);
            setSprints(sprintData);
            setIssues(Array.isArray(issueData) ? issueData : issueData.items || []);
        } catch (error) {
            setError(error.response?.data?.detail || "Unable to load sprint data.");
        } finally {
            setLoading(false);
        }
    }, [selectedProjectId]);

    useEffect(() => {
        loadSprintData();
    }, [loadSprintData]);

    useEffect(() => {
        if (!form.project_id && projects.length > 0) {
            setForm((current) => ({
                ...current,
                project_id: projects[0]._id
            }));
        }
    }, [projects, form.project_id]);

    function updateForm(event) {
        setForm({
            ...form,
            [event.target.name]: event.target.value
        });
    }

    async function createSprint(event) {
    event.preventDefault();
    setError("");


    const validationError = validateSprint(form, sprints);

    if (validationError) {
        setError(validationError);
        return;
    }


    try {
        await SprintService.createSprint(form);

        setForm({
            ...initialForm,
            project_id: form.project_id
        });

        await loadSprintData();

    } catch (error) {
        setError(
            error.response?.data?.detail ||
            "Unable to create sprint."
        );
    }
    }

    async function addIssue(sprintId, issueId) {
        setError("");

        try {
            await SprintService.addIssue(sprintId, issueId);
            await loadSprintData();
        } catch (error) {
            setError(error.response?.data?.detail || "Unable to add issue.");
        }
    }

    async function removeIssue(sprintId, issueId) {
        setError("");

        try {
            await SprintService.removeIssue(sprintId, issueId);
            await loadSprintData();
        } catch (error) {
            setError(error.response?.data?.detail || "Unable to remove issue.");
        }
    }

    async function startSprint(sprintId) {

    const sprint = sprints.find(
        (item) => item._id === sprintId
    );


    if(new Date(sprint.start_date) > new Date()) {
        setError(
            "Sprint cannot be started before start date."
        );
        return;
    }


    await SprintService.startSprint(sprintId);
    await loadSprintData();
    }

    async function completeSprint(sprintId) {

    const sprint = sprints.find(
        (item) => item._id === sprintId
    );


    if (sprint.status !== "active") {
        setError(
            "Only active sprint can be completed."
        );
        return;
    }


    await SprintService.completeSprint(sprintId);
    await loadSprintData();
    }

    const availableIssues = issues.filter((issue) => issue.status !== "DONE");

    return (
        <div className={styles.layout}>
            <Sidebar />
            <div className={styles.contentShell}>
                <Navbar />
                <main className={styles.content}>
                    <section className={styles.headerSection}>
                        <div>
                            <p className={styles.kicker}>Sprint Planning</p>
                            <h1>Sprints</h1>
                            <p>Create sprint cycles, add work, and manage lifecycle.</p>
                        </div>
                    </section>

                    {error && <div className={styles.errorBox}>{error}</div>}

                    <section className={styles.toolbar}>
                        <label>
                            Project filter
                            <select value={selectedProjectId} onChange={(event) => setSelectedProjectId(event.target.value)}>
                                <option value="">All projects</option>
                                {projects.map((project) => (
                                    <option key={project._id} value={project._id}>{project.name}</option>
                                ))}
                            </select>
                        </label>
                    </section>

                    <form className={styles.sprintForm} onSubmit={createSprint}>
                        <input name="name" placeholder="Sprint name" value={form.name} onChange={updateForm} required />
                        <select name="project_id" value={form.project_id} onChange={updateForm} required>
                            <option value="">Select project</option>
                            {projects.map((project) => (
                                <option key={project._id} value={project._id}>{project.name}</option>
                            ))}
                        </select>
                        <input type="date" name="start_date" value={form.start_date} min={today} onChange={updateForm} required />
                        <input type="date" name="end_date" value={form.end_date} min={form.start_date} onChange={updateForm} required />
                        <button type="submit">Create Sprint</button>
                    </form>

                    {loading ? (
                        <div className={styles.loading}>Loading sprints...</div>
                    ) : (
                        <section className={styles.sprintGrid}>
                            {sprints.length ? sprints.map((sprint) => (
                                <article key={sprint._id} className={styles.sprintCard}>
                                    <div className={styles.sprintHeader}>
                                        <div>
                                            <h3>{sprint.name}</h3>
                                            <p>{sprint.start_date} to {sprint.end_date}</p>
                                        </div>
                                        <span className={styles.status}>{sprint.status}</span>
                                    </div>

                                    <div className={styles.lifecycle}>
                                        <button type="button" disabled={sprint.status !== "planned"} onClick={() => startSprint(sprint._id)}>
                                            Start
                                        </button>
                                        <button type="button" disabled={sprint.status !== "active"} onClick={() => completeSprint(sprint._id)}>
                                            Complete
                                        </button>
                                    </div>

                                    <div className={styles.issuePicker}>
                                        <select onChange={(event) => event.target.value && addIssue(sprint._id, event.target.value)} defaultValue="">
                                            <option value="">Add issue</option>
                                            {availableIssues
                                                .filter((issue) => issue.project_id === sprint.project_id && !sprint.issue_ids?.includes(issue.id))
                                                .map((issue) => (
                                                    <option key={issue.id} value={issue.id}>{issue.issue_key} - {issue.title}</option>
                                                ))}
                                        </select>
                                    </div>

                                    <div className={styles.sprintIssues}>
                                        {(sprint.issue_ids || []).length ? sprint.issue_ids.map((issueId) => {
                                            const issue = issues.find((item) => item.id === issueId);
                                            return (
                                                <div key={issueId} className={styles.sprintIssue}>
                                                    <span>{issue ? `${issue.issue_key} - ${issue.title}` : issueId}</span>
                                                    <button type="button" onClick={() => removeIssue(sprint._id, issueId)}>Remove</button>
                                                </div>
                                            );
                                        }) : <p>No issues in this sprint.</p>}
                                    </div>
                                </article>
                            )) : <p>No sprints found.</p>}
                        </section>
                    )}
                </main>
            </div>
        </div>
    );
};

export default SprintBoard;
