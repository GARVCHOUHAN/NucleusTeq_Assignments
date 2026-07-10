import { useEffect, useState } from "react";

import Navbar from "../../components/common/navbar/Navbar";
import Sidebar from "../../components/common/sidebar/Sidebar";
import { useAuth } from "../../hooks/use-auth";
import DashboardService from "../../services/dashboard-service";
import styles from "./Dashboard.module.css";


const emptyStats = {
    projects: 0,
    issues: 0,
    open_issues: 0,
    completed_issues: 0,
    sprints: 0,
    active_sprints: 0,
    sprint_progress: 0,
    issue_completion: 0
};


function Dashboard() {
    const { currentUser } = useAuth();
    const [stats, setStats] = useState(emptyStats);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadStats() {
            setLoading(true);
            setError("");

            try {
                const data = await DashboardService.getStats();
                setStats(data);
            } catch (error) {
                setError(error.response?.data?.detail || "Unable to load dashboard.");
            } finally {
                setLoading(false);
            }
        }

        loadStats();
    }, []);

    return (
        <div className={styles.layout}>
            <Sidebar />
            <div className={styles.content}>
                <Navbar />
                <main className={styles.body}>
                    <section className={styles.hero}>
                        <div>
                            <p className={styles.overline}>Overview</p>
                            <h1>Welcome back, {currentUser?.name}</h1>
                            <p className={styles.description}>
                                Track project progress, issue status, and sprint health from one workspace.
                            </p>
                        </div>
                        <span className={styles.badge}>Role: {currentUser?.role}</span>
                    </section>

                    {error && <p className={styles.error}>{error}</p>}

                    <section className={styles.stats}>
                        <div className={styles.statCard}>
                            <p className={styles.statTitle}>Projects</p>
                            <p className={styles.statValue}>{loading ? "..." : stats.projects}</p>
                        </div>
                        <div className={styles.statCard}>
                            <p className={styles.statTitle}>Open Issues</p>
                            <p className={styles.statValue}>{loading ? "..." : stats.open_issues}</p>
                        </div>
                        <div className={styles.statCard}>
                            <p className={styles.statTitle}>Active Sprints</p>
                            <p className={styles.statValue}>{loading ? "..." : stats.active_sprints}</p>
                        </div>
                        <div className={styles.statCard}>
                            <p className={styles.statTitle}>Issue Completion</p>
                            <p className={styles.statValue}>{loading ? "..." : `${stats.issue_completion}%`}</p>
                        </div>
                        <div className={styles.statCard}>
                            <p className={styles.statTitle}>Sprint Progress</p>
                            <p className={styles.statValue}>{loading ? "..." : `${stats.sprint_progress}%`}</p>
                        </div>
                        <div className={styles.statCard}>
                            <p className={styles.statTitle}>Total Issues</p>
                            <p className={styles.statValue}>{loading ? "..." : stats.issues}</p>
                        </div>
                    </section>
                </main>
            </div>
        </div>
    );
}

export default Dashboard;
