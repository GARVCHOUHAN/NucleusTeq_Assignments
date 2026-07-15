from app.repositories.issue_repository import IssueRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.sprint_repository import SprintRepository


class DashboardService:
    @staticmethod
    def get_stats(current_user: dict):
        if current_user["role"] == "ADMIN":
            projects = ProjectRepository.get_all_projects()
            issues = IssueRepository.get_all_issues()
            sprints = SprintRepository.get_all_sprints()
        else:
            projects = ProjectRepository.get_projects_by_member(
                current_user["email"]
            )
            project_ids = [
                project["_id"]
                for project in projects
            ]
            issues = IssueRepository.get_issues_by_project_ids(project_ids)
            sprints = []

            for project_id in project_ids:
                sprints.extend(
                    SprintRepository.get_sprints_by_project(project_id)
                )

        open_issues = [
            issue
            for issue in issues
            if issue.get("status") != "DONE"
        ]
        completed_issues = [
            issue
            for issue in issues
            if issue.get("status") == "DONE"
        ]
        active_sprints = [
            sprint
            for sprint in sprints
            if sprint.get("status") == "active"
        ]
        completed_sprints = [
            sprint
            for sprint in sprints
            if sprint.get("status") == "completed"
        ]

        sprint_progress = 0

        if sprints:
            sprint_progress = round(
                len(completed_sprints) / len(sprints) * 100
            )

        issue_completion = 0

        if issues:
            issue_completion = round(
                len(completed_issues) / len(issues) * 100
            )

        return {
            "projects": len(projects),
            "issues": len(issues),
            "open_issues": len(open_issues),
            "completed_issues": len(completed_issues),
            "sprints": len(sprints),
            "active_sprints": len(active_sprints),
            "completed_sprints": len(completed_sprints),
            "sprint_progress": sprint_progress,
            "issue_completion": issue_completion
        }
