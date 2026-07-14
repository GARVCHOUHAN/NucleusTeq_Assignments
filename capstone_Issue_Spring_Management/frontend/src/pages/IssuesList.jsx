import { useCallback, useEffect, useState } from "react";

import IssueCard from "../components/IssueCard";
import IssueForm from "../components/IssueForm";
import Navbar from "../components/project/common/navbar/Navbar";
import Sidebar from "../components/project/common/sidebar/Sidebar";
import { useProjects } from "../hooks/use-project";
import IssueService from "../services/issue-service";
import styles from "./IssuesList.module.css";


const statuses = [
    "",
    "BACKLOG",
    "TODO",
    "IN_PROGRESS",
    "REVIEW",
    "DONE"
];


function IssuesList(){
const {projects}=useProjects();
const [issues,setIssues]=useState([]);
const [meta,setMeta]=useState({page:1,limit:8,total:0,pages:0});
const [filters,setFilters]=useState({
search:"",
project_id:"",
status:"",
assignee:""
});
const [loading,setLoading]=useState(false);
const [error,setError]=useState("");
const [showForm,setShowForm]=useState(false);

const loadIssues=useCallback(async(page=1)=>{
setLoading(true);
setError("");

try{
const data=await IssueService.getIssues({
...filters,
page,
limit:meta.limit,
paginated:true
});
setIssues(data.items || []);
setMeta({
page:data.page,
limit:data.limit,
total:data.total,
pages:data.pages
});
}
catch(error){
setError(error.response?.data?.detail || "Unable to load issues");
}
finally{
setLoading(false);
}
},[filters,meta.limit]);

useEffect(()=>{
loadIssues(1);
},[filters,loadIssues]);

function updateFilter(event){
setFilters({
...filters,
[event.target.name]:event.target.value
});
}

const renderIssueTree = (parentId = null, depth = 0, parentIssue = null) => {
const children = issues.filter((issue) => {
const issueParentId = issue.parent_id ?? issue.parentId ?? null;
return issueParentId === parentId;
});

return children.map((issue) => (
<div key={issue.id || issue._id}>
<IssueCard
issue={issue}
onUpdated={() => loadIssues(meta.page)}
depth={depth}
parentIssueKey={parentIssue?.issue_key}
/>
{renderIssueTree(issue.id || issue._id, depth + 1, issue)}
</div>
));
};

return(
<div className={styles.layout}>
<Sidebar/>
<div className={styles.content}>
<Navbar/>
<main className={styles.page}>
<section className={styles.header}>
<div>
<p className={styles.kicker}>Issue Tracking</p>
<h1>Issues</h1>
<p>Search, filter, create, and move work through the workflow.</p>
</div>
<button type="button" onClick={()=>setShowForm(true)}>
Create Issue
</button>
</section>

<section className={styles.filters}>
<input
name="search"
placeholder="Search title or description"
value={filters.search}
onChange={updateFilter}
/>
<select name="project_id" value={filters.project_id} onChange={updateFilter}>
<option value="">All projects</option>
{projects.map((project)=>(
<option key={project._id} value={project._id}>{project.name}</option>
))}
</select>
<select name="status" value={filters.status} onChange={updateFilter}>
{statuses.map((status)=>(
<option key={status || "all"} value={status}>
{status ? status.replace("_"," ") : "All statuses"}
</option>
))}
</select>
<input
name="assignee"
placeholder="Assignee email"
value={filters.assignee}
onChange={updateFilter}
/>
</section>

{error && <p className={styles.error}>{error}</p>}

<section className={styles.summary}>
<span>{meta.total} issues</span>
<span>Page {meta.page} of {meta.pages || 1}</span>
</section>

<section className={styles.issueList}>
{!loading && issues.length>0 && (
<div className={styles.listHeader}>
<span>Key</span>
<span>Summary</span>
<span>Status</span>
<span>Assignee</span>
<span>Points</span>
<span>Actions</span>
</div>
)}
{loading?
<p className={styles.emptyState}>Loading issues...</p>
:
issues.length?
renderIssueTree()
:
<p className={styles.emptyState}>No issues found.</p>
}
</section>

<div className={styles.pagination}>
<button
type="button"
disabled={meta.page<=1}
onClick={()=>loadIssues(meta.page-1)}
>
Previous
</button>
<button
type="button"
disabled={meta.page>=meta.pages}
onClick={()=>loadIssues(meta.page+1)}
>
Next
</button>
</div>
</main>
</div>

{showForm && (
<IssueForm
projects={projects}
onClose={()=>setShowForm(false)}
onCreated={()=>loadIssues(1)}
/>
)}
</div>
);
}

export default IssuesList;
