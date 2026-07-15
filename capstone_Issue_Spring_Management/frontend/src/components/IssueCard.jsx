import { useState } from "react";

import { useAuth } from "../hooks/use-auth";
import IssueService from "../services/issue-service";
import styles from "./IssueCard.module.css";


const priorityClass = {
    High: styles.high,
    Medium: styles.medium,
    Low: styles.low
};

const statusActions = {
    BACKLOG: [{ label: "Move to Todo", status: "TODO" }],
    TODO: [{ label: "Start Work", status: "IN_PROGRESS" }],
    IN_PROGRESS: [
        { label: "Review", status: "REVIEW" },
        { label: "Done", status: "DONE" },
        { label: "Back to Todo", status: "TODO" }
    ],
    REVIEW: [
        { label: "Complete", status: "DONE" },
        { label: "Changes", status: "IN_PROGRESS" }
    ],
    DONE: []
};


const IssueCard = ({ issue, onUpdated, depth = 0, parentIssueKey }) => {
    const { currentUser } = useAuth();
    const [saving, setSaving] = useState(false);
    const [commentsOpen, setCommentsOpen] = useState(false);
    const [comments, setComments] = useState([]);
    const [commentText, setCommentText] = useState("");
    const [commentError, setCommentError] = useState("");
    const [subtasks, setSubtasks] = useState([]);
    const [subtasksOpen, setSubtasksOpen] = useState(false);

    const canUpdate = currentUser?.role === "ADMIN" || issue.assignee === currentUser?.email || issue.reporter === currentUser?.email;
    const actions = statusActions[issue.status] || [];
    const isChild = depth > 0;
    const priorityStyle = priorityClass[issue.priority] || styles.low;
    const assigneeInitial = issue.assignee ? issue.assignee.charAt(0).toUpperCase() : "?";

    const handleStatusUpdate = async (nextStatus) => {
        setSaving(true);

        try {
            await IssueService.updateStatus(issue.id, nextStatus);
            onUpdated?.();
        } catch (error) {
            alert(error.response?.data?.detail || "Unable to update issue status.");
        } finally {
            setSaving(false);
        }
    };

    const loadComments = async () => {
        setCommentError("");

        try {
            const data = await IssueService.getComments(issue.id);
            setComments(data);
        } catch (error) {
            setCommentError(error.response?.data?.detail || "Unable to load comments.");
        }
    };

    const toggleComments = async () => {
        const nextOpen = !commentsOpen;
        setCommentsOpen(nextOpen);

        if (nextOpen) {
            await loadComments();
        }
    };

    const addComment = async () => {
        if (!commentText.trim()) {
            return;
        }

        try {
            await IssueService.addComment(issue.id, commentText.trim());
            setCommentText("");
            await loadComments();
        } catch (error) {
            setCommentError(error.response?.data?.detail || "Unable to add comment.");
        }
    };

    const deleteComment = async (commentId) => {
        try {
            await IssueService.deleteComment(commentId);
            await loadComments();
        } catch (error) {
            setCommentError(error.response?.data?.detail || "Unable to delete comment.");
        }
    };

    const loadSubtasks = async () => {
        try {
            const data = await IssueService.getSubtasks(issue.id);
            setSubtasks(data);
        } catch (error) {
            setSubtasks([]);
        }
    };

    const toggleSubtasks = async () => {
        const nextOpen = !subtasksOpen;
        setSubtasksOpen(nextOpen);

        if (nextOpen) {
            await loadSubtasks();
        }
    };

    const deleteIssue = async () => {
        if (!window.confirm("Delete this issue?")) {
            return;
        }

        try {
            await IssueService.deleteIssue(issue.id);
            onUpdated?.();
        } catch (error) {
            alert(error.response?.data?.detail || "Unable to delete issue.");
        }
    };

    return (
        <div className={`${styles.issueWrapper} ${isChild ? styles.childWrapper : ""}`}>
            <article className={styles.row}>
            <div className={styles.main}>
                <div className={styles.key}>
                    <span className={styles.issueKey}>{issue.issue_key}</span>
                    {isChild && parentIssueKey && (
                        <span className={styles.childBadge}>Child of {parentIssueKey}</span>
                    )}
                    <span className={`${styles.priority} ${priorityStyle}`}>{issue.priority || "Low"}</span>
                </div>

                <div className={styles.summary}>
                    <h3>{issue.title}</h3>
                    <p>{issue.description}</p>
                </div>

                <span className={styles.status}>{issue.status.replace("_", " ")}</span>

                <div className={styles.assignee}>
                    <span className={styles.avatar}>{assigneeInitial}</span>
                    <span title={issue.assignee || "Unassigned"}>{issue.assignee || "Unassigned"}</span>
                </div>

                <span className={styles.points}>{issue.story_points} pts</span>

                <div className={styles.actions}>
                    {canUpdate && actions.map((action) => (
                        <button
                            key={action.status}
                            type="button"
                            onClick={() => handleStatusUpdate(action.status)}
                            disabled={saving}
                        >
                            {saving ? "Updating..." : action.label}
                        </button>
                    ))}
                    {(currentUser?.role === "ADMIN" || issue.reporter === currentUser?.email) && (
                        <button type="button" className={styles.deleteComment} onClick={deleteIssue}>
                            Delete
                        </button>
                    )}
                </div>
            </div>

            <div className={styles.footer}>
                <button type="button" className={styles.commentToggle} onClick={toggleComments}>
                    {commentsOpen ? "Hide comments" : `Comments${comments.length ? ` (${comments.length})` : ""}`}
                </button>
                <button type="button" className={styles.commentToggle} onClick={toggleSubtasks}>
                    {subtasksOpen ? "Hide subtasks" : `Subtasks${subtasks.length ? ` (${subtasks.length})` : ""}`}
                </button>
            </div>

            {subtasksOpen && (
                <div className={styles.comments}>
                    {subtasks.length ? subtasks.map((subtask) => (
                        <div key={subtask.id} className={styles.comment}>
                            <p>{subtask.title}</p>
                            <small>{subtask.status}</small>
                        </div>
                    )) : <p className={styles.error}>No subtasks yet.</p>}
                </div>
            )}

            {commentsOpen && (
                <div className={styles.comments}>
                    {comments.length ? comments.map((comment) => (
                        <div key={comment._id} className={styles.comment}>
                            <p>{comment.body}</p>
                            <div className={styles.commentMeta}>
                                <small>{comment.author_email}</small>
                                {(currentUser?.role === "ADMIN" || comment.author_email === currentUser?.email) && (
                                    <button type="button" className={styles.deleteComment} onClick={() => deleteComment(comment._id)}>
                                        Delete
                                    </button>
                                )}
                            </div>
                        </div>
                    )) : <p className={styles.error}>No comments yet.</p>}

                    <div className={styles.commentForm}>
                        <input
                            placeholder="Add a comment"
                            value={commentText}
                            onChange={(event) => setCommentText(event.target.value)}
                        />
                        <button type="button" className={styles.addComment} onClick={addComment}>
                            Add Comment
                        </button>
                    </div>
                    {commentError && <p className={styles.error}>{commentError}</p>}
                </div>
            )}
            </article>
        </div>
    );
};

export default IssueCard;
